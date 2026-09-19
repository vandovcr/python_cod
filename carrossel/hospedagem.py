"""Hospedagem das imagens.

A API do Instagram não aceita upload de bytes para imagem: ela baixa o arquivo
de uma URL HTTPS pública. Então todo slide precisa estar na web (nem que seja
por 5 minutos) antes de virar post.

Duas estratégias:

  S3Compativel  — sobe para qualquer bucket S3-compatible (Cloudflare R2, AWS
                  S3, Backblaze B2, MinIO). É o caminho recomendado: R2 tem
                  camada gratuita e não cobra egresso.
  URLsManuais   — você já hospedou em outro lugar e só informa a URL base.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol


class Hospedagem(Protocol):
    def enviar(self, arquivos: list[Path], prefixo: str) -> list[str]:
        """Publica os arquivos e devolve as URLs, na mesma ordem."""
        ...

    def remover(self, prefixo: str) -> None:
        """Apaga o que foi enviado (opcional — o Instagram já copiou a imagem)."""
        ...


class URLsManuais:
    """Para quem já hospeda os PNGs (GitHub Pages, Netlify, servidor próprio)."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def enviar(self, arquivos: list[Path], prefixo: str) -> list[str]:
        return [f"{self.base_url}/{prefixo}/{a.name}" for a in arquivos]

    def remover(self, prefixo: str) -> None:
        return None


class S3Compativel:
    """Bucket S3-compatible com leitura pública (ou domínio público do R2)."""

    def __init__(self, bucket: str, base_publica: str, endpoint_url: str | None = None,
                 region: str = "auto"):
        try:
            import boto3  # import tardio: só quem usa S3 precisa da dependência
        except ImportError:
            raise RuntimeError(
                "boto3 não instalado. Rode: pip install boto3 — "
                "ou use --base-url para hospedar por conta própria."
            )
        self.bucket = bucket
        self.base_publica = base_publica.rstrip("/")
        self._s3 = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            region_name=region,
            aws_access_key_id=os.environ.get("S3_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY"),
        )

    @classmethod
    def do_ambiente(cls) -> "S3Compativel":
        faltando = [v for v in ("S3_BUCKET", "S3_BASE_PUBLICA",
                                "S3_ACCESS_KEY_ID", "S3_SECRET_ACCESS_KEY")
                    if not os.environ.get(v)]
        if faltando:
            raise RuntimeError(f"Variáveis de hospedagem ausentes: {', '.join(faltando)}")
        return cls(
            bucket=os.environ["S3_BUCKET"],
            base_publica=os.environ["S3_BASE_PUBLICA"],
            endpoint_url=os.environ.get("S3_ENDPOINT") or None,
            region=os.environ.get("S3_REGION", "auto"),
        )

    def enviar(self, arquivos: list[Path], prefixo: str) -> list[str]:
        urls = []
        for arquivo in arquivos:
            chave = f"{prefixo}/{arquivo.name}"
            self._s3.upload_file(
                str(arquivo), self.bucket, chave,
                ExtraArgs={"ContentType": "image/png", "CacheControl": "public, max-age=3600"},
            )
            urls.append(f"{self.base_publica}/{chave}")
        return urls

    def remover(self, prefixo: str) -> None:
        resposta = self._s3.list_objects_v2(Bucket=self.bucket, Prefix=f"{prefixo}/")
        objetos = [{"Key": o["Key"]} for o in resposta.get("Contents", [])]
        if objetos:
            self._s3.delete_objects(Bucket=self.bucket, Delete={"Objects": objetos})
