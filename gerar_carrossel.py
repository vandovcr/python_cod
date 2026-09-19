#!/usr/bin/env python3
"""Gera os PNGs de um carrossel a partir de um roteiro em Markdown.

    python3 gerar_carrossel.py roteiros/meu-post.md
    python3 gerar_carrossel.py roteiros/*.md --saida saida/
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from carrossel.render import render_roteiro
from carrossel.roteiro import carregar


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Gera os slides de um carrossel para Instagram.")
    p.add_argument("roteiros", nargs="+", type=Path, help="arquivo(s) .md de roteiro")
    p.add_argument("--saida", type=Path, default=Path("saida"),
                   help="diretório de saída (padrão: saida/)")
    p.add_argument("--formato", choices=["jpg", "png"], default="jpg",
                   help="jpg é o que a API do Instagram aceita (padrão)")
    args = p.parse_args(argv)

    falhas = 0
    for caminho in args.roteiros:
        avisos: list[str] = []
        try:
            roteiro = carregar(caminho)
            arquivos = render_roteiro(roteiro, args.saida, avisos, args.formato)
        except (ValueError, FileNotFoundError, OSError) as erro:
            print(f"✗ {caminho}: {erro}", file=sys.stderr)
            falhas += 1
            continue

        print(f"✓ {roteiro.titulo}")
        print(f"  pilar: {roteiro.pilar or '—'} · {len(arquivos)} slides")
        print(f"  {arquivos[0].parent}/")
        for aviso in avisos:
            print(f"  ⚠ {aviso}")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())
