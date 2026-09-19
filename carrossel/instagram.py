"""Publicação de carrossel via API de conteúdo do Instagram.

Fluxo oficial (3 chamadas + polling):

    1. um container por imagem   POST /{ig_user_id}/media  (is_carousel_item=true)
    2. um container do carrossel POST /{ig_user_id}/media  (media_type=CAROUSEL)
    3. publicar                  POST /{ig_user_id}/media_publish

Requisitos do lado da conta:
  * conta Instagram Profissional (Empresa ou Criador de conteúdo);
  * app na Meta for Developers com a permissão de publicação de conteúdo;
  * as imagens precisam estar em URLs HTTPS públicas — a API baixa por URL,
    não aceita upload de bytes para imagem. Ver carrossel/hospedagem.py.

Ver docs/publicacao-automatica-instagram.md para o passo a passo da configuração.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

import requests

# A Meta descontinua versões da Graph API (~2 anos de vida). Confira a versão
# corrente no changelog e ajuste via GRAPH_API_VERSION.
VERSAO_PADRAO = os.environ.get("GRAPH_API_VERSION", "v21.0")

# Dois caminhos de autenticação, mesma sequência de chamadas:
#   facebook  -> Facebook Login, exige Página do Facebook vinculada
#   instagram -> Instagram Login (mais simples, sem Página)
HOSTS = {
    "facebook": "https://graph.facebook.com",
    "instagram": "https://graph.instagram.com",
}

MAX_ITENS = 10
MIN_ITENS = 2


class ErroInstagram(RuntimeError):
    """Falha reportada pela API ou por um container que não ficou pronto."""


@dataclass
class Publicador:
    ig_user_id: str
    access_token: str
    login: str = "facebook"
    versao: str = VERSAO_PADRAO
    timeout: int = 60

    @classmethod
    def do_ambiente(cls) -> "Publicador":
        """Monta o publicador a partir das variáveis de ambiente / .env."""
        faltando = [v for v in ("IG_USER_ID", "IG_ACCESS_TOKEN") if not os.environ.get(v)]
        if faltando:
            raise ErroInstagram(
                f"Variáveis ausentes: {', '.join(faltando)}. "
                "Copie .env.exemplo para .env e preencha."
            )
        return cls(
            ig_user_id=os.environ["IG_USER_ID"],
            access_token=os.environ["IG_ACCESS_TOKEN"],
            login=os.environ.get("IG_LOGIN", "facebook"),
            versao=os.environ.get("GRAPH_API_VERSION", VERSAO_PADRAO),
        )

    # ------------------------------------------------------------ transporte

    @property
    def _base(self) -> str:
        try:
            return f"{HOSTS[self.login]}/{self.versao}"
        except KeyError:
            raise ErroInstagram(f"IG_LOGIN inválido: {self.login!r} (use {list(HOSTS)})")

    def _chamar(self, metodo: str, caminho: str, **params) -> dict:
        params["access_token"] = self.access_token
        url = f"{self._base}/{caminho.lstrip('/')}"
        resposta = requests.request(metodo, url, params=params, timeout=self.timeout)
        try:
            corpo = resposta.json()
        except ValueError:
            raise ErroInstagram(f"HTTP {resposta.status_code}: resposta não-JSON")

        if "error" in corpo:
            erro = corpo["error"]
            raise ErroInstagram(
                f"[{erro.get('code')}/{erro.get('error_subcode', '-')}] "
                f"{erro.get('message')} — {erro.get('error_user_msg', '')}".strip(" —")
            )
        resposta.raise_for_status()
        return corpo

    # --------------------------------------------------------------- passos

    def criar_item(self, image_url: str) -> str:
        """Passo 1: container de uma imagem do carrossel."""
        r = self._chamar("POST", f"{self.ig_user_id}/media",
                         image_url=image_url, is_carousel_item="true")
        return r["id"]

    def criar_carrossel(self, filhos: list[str], legenda: str = "") -> str:
        """Passo 2: container do carrossel, amarrando os itens na ordem dada."""
        if not MIN_ITENS <= len(filhos) <= MAX_ITENS:
            raise ErroInstagram(
                f"Carrossel aceita de {MIN_ITENS} a {MAX_ITENS} itens, recebi {len(filhos)}."
            )
        return self._chamar("POST", f"{self.ig_user_id}/media",
                            media_type="CAROUSEL",
                            children=",".join(filhos),
                            caption=legenda)["id"]

    def aguardar(self, container_id: str, tentativas: int = 30, intervalo: int = 5) -> None:
        """Espera o container sair de IN_PROGRESS. Publicar antes disso falha."""
        for _ in range(tentativas):
            estado = self._chamar("GET", container_id, fields="status_code,status")
            codigo = estado.get("status_code")
            if codigo == "FINISHED":
                return
            if codigo in ("ERROR", "EXPIRED"):
                raise ErroInstagram(f"Container {container_id}: {codigo} — {estado.get('status')}")
            time.sleep(intervalo)
        raise ErroInstagram(
            f"Container {container_id} seguiu IN_PROGRESS após "
            f"{tentativas * intervalo}s. Imagens muito pesadas ou host lento."
        )

    def publicar_container(self, creation_id: str) -> str:
        """Passo 3: publica de fato. Devolve o ID da mídia no feed."""
        return self._chamar("POST", f"{self.ig_user_id}/media_publish",
                            creation_id=creation_id)["id"]

    def limite_restante(self) -> dict:
        """Quota de publicação nas últimas 24h (o teto da conta é 50 posts)."""
        dados = self._chamar("GET", f"{self.ig_user_id}/content_publishing_limit",
                             fields="config,quota_usage")
        return (dados.get("data") or [{}])[0]

    # ------------------------------------------------------------ orquestra

    def publicar_carrossel(self, urls: list[str], legenda: str = "",
                           on_log=print) -> str:
        """Fluxo completo. Devolve o ID da publicação."""
        uso = self.limite_restante()
        if uso:
            teto = (uso.get("config") or {}).get("quota_total", 50)
            on_log(f"  quota 24h: {uso.get('quota_usage', 0)}/{teto}")

        filhos = []
        for i, url in enumerate(urls, 1):
            filhos.append(self.criar_item(url))
            on_log(f"  item {i}/{len(urls)} → container {filhos[-1]}")

        carrossel = self.criar_carrossel(filhos, legenda)
        on_log(f"  carrossel → container {carrossel}")

        self.aguardar(carrossel)
        media_id = self.publicar_container(carrossel)
        on_log(f"  publicado → media {media_id}")
        return media_id


# ---------------------------------------------------------------- tokens

def renovar_token_instagram(token: str, versao: str = VERSAO_PADRAO) -> dict:
    """Estende um token de longa duração do Instagram Login por mais 60 dias.

    Só funciona com tokens que já sejam de longa duração e tenham pelo menos
    24h de vida. Rode a cada ~50 dias.
    """
    r = requests.get(f"{HOSTS['instagram']}/refresh_access_token",
                     params={"grant_type": "ig_refresh_token", "access_token": token},
                     timeout=30)
    r.raise_for_status()
    return r.json()


def trocar_por_token_longo(token_curto: str, app_id: str, app_secret: str,
                           versao: str = VERSAO_PADRAO) -> dict:
    """Troca um token curto do Facebook Login por um de 60 dias."""
    r = requests.get(f"{HOSTS['facebook']}/{versao}/oauth/access_token",
                     params={
                         "grant_type": "fb_exchange_token",
                         "client_id": app_id,
                         "client_secret": app_secret,
                         "fb_exchange_token": token_curto,
                     }, timeout=30)
    r.raise_for_status()
    return r.json()
