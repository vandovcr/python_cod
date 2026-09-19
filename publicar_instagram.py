#!/usr/bin/env python3
"""Publica um carrossel já renderizado no Instagram.

    # 1. confere o que vai subir, sem publicar
    python3 publicar_instagram.py saida/meu-post --simular

    # 2. publica de verdade (hospedagem S3/R2 vinda do .env)
    python3 publicar_instagram.py saida/meu-post

    # 3. publica com imagens que você mesmo hospedou
    python3 publicar_instagram.py saida/meu-post --base-url https://cdn.seudominio.com

Leia docs/publicacao-automatica-instagram.md antes do primeiro uso.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from PIL import Image

from carrossel.ambiente import carregar_env
from carrossel.hospedagem import S3Compativel, URLsManuais
from carrossel.instagram import ErroInstagram, Publicador

LIMITE_LEGENDA = 2200


def coletar_slides(pasta: Path, dir_temp: Path) -> list[Path]:
    """Slides em ordem, já em JPEG — que é o formato que a API aceita."""
    arquivos = sorted(p for p in pasta.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhuma imagem em {pasta}/ — rode gerar_carrossel.py antes.")

    prontos: list[Path] = []
    for arquivo in arquivos:
        if arquivo.suffix.lower() == ".png":
            convertido = dir_temp / f"{arquivo.stem}.jpg"
            with Image.open(arquivo) as img:
                img.convert("RGB").save(convertido, "JPEG", quality=92,
                                        subsampling=0, optimize=True)
            prontos.append(convertido)
        else:
            prontos.append(arquivo)
    return prontos


def ler_legenda(pasta: Path, explicita: Path | None) -> str:
    caminho = explicita or (pasta / "legenda.txt")
    if not caminho.exists():
        return ""
    texto = caminho.read_text(encoding="utf-8").strip()
    if len(texto) > LIMITE_LEGENDA:
        raise ValueError(
            f"Legenda com {len(texto)} caracteres; o Instagram corta em {LIMITE_LEGENDA}."
        )
    return texto


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Publica um carrossel no Instagram.")
    p.add_argument("pasta", type=Path, help="pasta com os PNGs (ex.: saida/meu-post)")
    p.add_argument("--legenda", type=Path, help="arquivo de legenda (padrão: <pasta>/legenda.txt)")
    p.add_argument("--base-url", help="URL base se você já hospedou as imagens")
    p.add_argument("--simular", action="store_true",
                   help="mostra o que seria publicado e para antes de postar")
    p.add_argument("--manter", action="store_true",
                   help="não apaga as imagens da hospedagem depois de publicar")
    args = p.parse_args(argv)

    carregar_env()
    temp = tempfile.TemporaryDirectory(prefix="carrossel-")

    try:
        slides = coletar_slides(args.pasta, Path(temp.name))
        legenda = ler_legenda(args.pasta, args.legenda)
    except (FileNotFoundError, ValueError, OSError) as erro:
        print(f"✗ {erro}", file=sys.stderr)
        return 1

    prefixo = args.pasta.name
    print(f"carrossel: {prefixo}")
    print(f"  {len(slides)} slides: {', '.join(a.name for a in slides)}")
    print(f"  legenda: {len(legenda)} caracteres" if legenda else "  legenda: (vazia)")

    if args.simular:
        print("\n[simulação] nada foi enviado nem publicado.")
        return 0

    try:
        hospedagem = URLsManuais(args.base_url) if args.base_url else S3Compativel.do_ambiente()
        publicador = Publicador.do_ambiente()
    except (RuntimeError, ErroInstagram) as erro:
        print(f"✗ configuração: {erro}", file=sys.stderr)
        return 1

    try:
        urls = hospedagem.enviar(slides, prefixo)
        print(f"  hospedado em {urls[0].rsplit('/', 1)[0]}/")
        media_id = publicador.publicar_carrossel(urls, legenda)
    except ErroInstagram as erro:
        print(f"✗ Instagram: {erro}", file=sys.stderr)
        return 1
    except Exception as erro:  # rede, credencial de bucket, etc.
        print(f"✗ {type(erro).__name__}: {erro}", file=sys.stderr)
        return 1

    if not args.manter:
        # O Instagram já copiou as imagens; manter o bucket limpo é de graça.
        try:
            hospedagem.remover(prefixo)
            print("  hospedagem temporária limpa")
        except Exception as erro:
            print(f"  aviso: não consegui limpar a hospedagem ({erro})", file=sys.stderr)

    print(f"\n✓ publicado — media ID {media_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
