"""Carregador mínimo de .env — evita mais uma dependência só para isso."""

from __future__ import annotations

import os
from pathlib import Path


def carregar_env(caminho: str | Path = ".env") -> int:
    """Lê KEY=VALOR do arquivo para os.environ. Não sobrescreve o que já existe."""
    caminho = Path(caminho)
    if not caminho.exists():
        return 0
    lidas = 0
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        chave = chave.strip()
        valor = valor.strip().strip("\"'")
        if chave and chave not in os.environ:
            os.environ[chave] = valor
            lidas += 1
    return lidas
