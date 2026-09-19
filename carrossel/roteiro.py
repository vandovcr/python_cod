"""Parser dos roteiros em Markdown.

Formato de um roteiro (ver roteiros/ para exemplos):

    ---
    titulo: O que acontece quando você digita um site
    pilar: redes
    handle: "@seuperfil"
    ---

    ## VOCÊ DIGITA UM SITE E APERTA ENTER
    O que acontece nos próximos 200 ms?

    ## DNS — achar o endereço
    O navegador pergunta: "qual o IP de exemplo.com?"

    - cache do browser
    - cache do sistema operacional

    ```
    $ dig exemplo.com +trace
    ```

    ## Salva esse post
    Você vai querer revisar antes da próxima entrevista.

Regras:
  * cada `##` abre um slide;
  * o primeiro slide vira capa e o último vira CTA automaticamente;
  * para forçar, ponha `tipo: capa|conteudo|cta` como primeira linha do corpo;
  * `- ` vira bullet, cerca de crase vira bloco de código, `!` no início da
    linha marca o parágrafo como alerta (renderizado em vermelho).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

TIPOS = {"capa", "conteudo", "cta"}


@dataclass
class Bloco:
    """Um pedaço de conteúdo dentro de um slide."""
    tipo: str            # "paragrafo" | "bullets" | "codigo" | "alerta"
    conteudo: str | list[str]


@dataclass
class Slide:
    titulo: str
    blocos: list[Bloco] = field(default_factory=list)
    tipo: str = "conteudo"


@dataclass
class Roteiro:
    titulo: str
    pilar: str
    handle: str
    slides: list[Slide]
    legenda: str = ""
    origem: Path | None = None

    @property
    def slug(self) -> str:
        base = self.origem.stem if self.origem else self.titulo
        texto = re.sub(r"[^\w\s-]", "", base.lower())
        return re.sub(r"[-\s]+", "-", texto).strip("-") or "carrossel"


def _parse_frontmatter(linhas: list[str]) -> tuple[dict[str, str], list[str]]:
    if not linhas or linhas[0].strip() != "---":
        return {}, linhas
    try:
        fim = next(i for i in range(1, len(linhas)) if linhas[i].strip() == "---")
    except StopIteration:
        raise ValueError("Front matter aberto com '---' e nunca fechado.")
    meta: dict[str, str] = {}
    for linha in linhas[1:fim]:
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        if ":" not in linha:
            raise ValueError(f"Linha inválida no front matter: {linha!r}")
        chave, valor = linha.split(":", 1)
        meta[chave.strip().lower()] = valor.strip().strip("\"'")
    return meta, linhas[fim + 1:]


def _parse_corpo(linhas: list[str]) -> tuple[list[Bloco], str | None]:
    """Converte as linhas de um slide em blocos. Devolve (blocos, tipo_forcado)."""
    blocos: list[Bloco] = []
    tipo_forcado: str | None = None
    paragrafo: list[str] = []
    bullets: list[str] = []
    codigo: list[str] = []
    em_codigo = False

    def fechar_paragrafo() -> None:
        nonlocal paragrafo
        if paragrafo:
            texto = " ".join(paragrafo).strip()
            eh_alerta = texto.startswith("!")
            blocos.append(Bloco("alerta" if eh_alerta else "paragrafo",
                                texto.lstrip("!").strip()))
            paragrafo = []

    def fechar_bullets() -> None:
        nonlocal bullets
        if bullets:
            blocos.append(Bloco("bullets", bullets))
            bullets = []

    for linha in linhas:
        crua = linha.rstrip()
        nua = crua.strip()

        if nua.startswith("```"):
            if em_codigo:
                blocos.append(Bloco("codigo", "\n".join(codigo)))
                codigo, em_codigo = [], False
            else:
                fechar_paragrafo()
                fechar_bullets()
                em_codigo = True
            continue

        if em_codigo:
            codigo.append(crua)
            continue

        if not nua:
            fechar_paragrafo()
            fechar_bullets()
            continue

        m = re.match(r"^tipo:\s*(\w+)$", nua, re.IGNORECASE)
        if m and not blocos and not paragrafo:
            candidato = m.group(1).lower()
            if candidato not in TIPOS:
                raise ValueError(f"tipo desconhecido: {candidato!r} (use {sorted(TIPOS)})")
            tipo_forcado = candidato
            continue

        if nua.startswith(("- ", "* ")):
            fechar_paragrafo()
            bullets.append(nua[2:].strip())
            continue

        fechar_bullets()
        paragrafo.append(nua)

    if em_codigo:
        raise ValueError("Bloco de código aberto com ``` e nunca fechado.")
    fechar_paragrafo()
    fechar_bullets()
    return blocos, tipo_forcado


def carregar(caminho: str | Path) -> Roteiro:
    caminho = Path(caminho)
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    meta, resto = _parse_frontmatter(linhas)

    # Quebra o corpo em seções de `##`
    secoes: list[tuple[str, list[str]]] = []
    atual: list[str] = []
    titulo_atual: str | None = None
    for linha in resto:
        m = re.match(r"^##\s+(.*)$", linha)
        if m:
            if titulo_atual is not None:
                secoes.append((titulo_atual, atual))
            titulo_atual, atual = m.group(1).strip(), []
        elif titulo_atual is not None:
            atual.append(linha)
    if titulo_atual is not None:
        secoes.append((titulo_atual, atual))

    # Uma seção "## LEGENDA" não é slide: é o texto do post.
    legenda = ""
    restantes: list[tuple[str, list[str]]] = []
    for titulo, corpo in secoes:
        if titulo.strip().lower() == "legenda":
            legenda = "\n".join(corpo).strip()
        else:
            restantes.append((titulo, corpo))
    secoes = restantes

    if not secoes:
        raise ValueError(f"{caminho}: nenhum slide encontrado (use '## Título do slide').")

    slides: list[Slide] = []
    for i, (titulo, corpo) in enumerate(secoes):
        blocos, forcado = _parse_corpo(corpo)
        if forcado:
            tipo = forcado
        elif i == 0:
            tipo = "capa"
        elif i == len(secoes) - 1:
            tipo = "cta"
        else:
            tipo = "conteudo"
        slides.append(Slide(titulo=titulo, blocos=blocos, tipo=tipo))

    if not 2 <= len(slides) <= 10:
        raise ValueError(
            f"{caminho}: {len(slides)} slides. O carrossel do Instagram aceita de 2 a 10 "
            "(o plano recomenda 8)."
        )

    return Roteiro(
        titulo=meta.get("titulo", slides[0].titulo),
        pilar=meta.get("pilar", ""),
        handle=meta.get("handle", ""),
        slides=slides,
        legenda=legenda,
        origem=caminho,
    )
