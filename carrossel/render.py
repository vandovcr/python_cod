"""Renderização dos slides com Pillow.

A mesma função de layout roda em dois modos: sem `draw` ela só mede a altura
(usado para escolher o corpo de fonte que cabe), com `draw` ela desenha. Medir e
desenhar pelo mesmo caminho é o que impede o texto de vazar do slide.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from . import design as d
from .roteiro import Bloco, Roteiro, Slide

RAIO_CAIXA = 24
ESPACO_ENTRE_BLOCOS = 34
LARGURA_UTIL = d.LARGURA - 2 * d.MARGEM


# ------------------------------------------------------------------ utilidades

def quebrar(texto: str, fonte, largura_max: int) -> list[str]:
    """Quebra o texto em linhas que cabem em `largura_max` pixels."""
    linhas: list[str] = []
    for paragrafo in texto.split("\n"):
        if not paragrafo.strip():
            linhas.append("")
            continue
        atual = ""
        for palavra in paragrafo.split():
            teste = f"{atual} {palavra}".strip()
            if fonte.getlength(teste) <= largura_max or not atual:
                atual = teste
            else:
                linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


def _altura_linha(tamanho: int) -> int:
    return int(tamanho * d.ENTRELINHA)


def _desenhar_linhas(draw, linhas, fonte, x, y, cor, tamanho, ancora="la") -> int:
    for linha in linhas:
        if draw is not None and linha:
            draw.text((x, y), linha, font=fonte, fill=cor, anchor=ancora)
        y += _altura_linha(tamanho)
    return y


# --------------------------------------------------------------- blocos

def _layout_blocos(blocos: list[Bloco], tema: d.Tema, tamanho: int,
                   x: int, y: int, largura: int, draw=None) -> int:
    """Desenha (ou só mede) a lista de blocos. Devolve o y final."""
    f_corpo = d.fonte("corpo", tamanho)
    f_mono = d.fonte("mono", max(26, tamanho - 8))
    mono_tam = max(26, tamanho - 8)

    for i, bloco in enumerate(blocos):
        if i:
            y += ESPACO_ENTRE_BLOCOS

        if bloco.tipo == "paragrafo":
            linhas = quebrar(bloco.conteudo, f_corpo, largura)
            y = _desenhar_linhas(draw, linhas, f_corpo, x, y, tema.texto, tamanho)

        elif bloco.tipo == "alerta":
            linhas = quebrar(bloco.conteudo, f_corpo, largura - 32)
            altura = len(linhas) * _altura_linha(tamanho)
            if draw is not None:
                draw.rounded_rectangle(
                    [x, y - 8, x + 6, y + altura - 4], radius=3, fill=tema.alerta
                )
            y = _desenhar_linhas(draw, linhas, f_corpo, x + 32, y, tema.alerta, tamanho)

        elif bloco.tipo == "bullets":
            # Marcador desenhado, não glifo: nem toda fonte tem "▸" e o
            # fallback do Pillow vira um retângulo vazio.
            recuo = 44
            raio = max(5, tamanho // 8)
            for item in bloco.conteudo:
                linhas = quebrar(item, f_corpo, largura - recuo)
                if draw is not None:
                    cy = y + int(tamanho * 0.52)
                    draw.ellipse([x + 4, cy - raio, x + 4 + 2 * raio, cy + raio],
                                 fill=tema.destaque)
                y = _desenhar_linhas(draw, linhas, f_corpo, x + recuo, y, tema.texto, tamanho)

        elif bloco.tipo == "codigo":
            linhas: list[str] = []
            for bruta in bloco.conteudo.split("\n"):
                linhas.extend(quebrar(bruta, f_mono, largura - 64) if bruta.strip() else [""])
            altura = len(linhas) * _altura_linha(mono_tam)
            if draw is not None:
                draw.rounded_rectangle(
                    [x, y - 24, x + largura, y + altura + 16],
                    radius=RAIO_CAIXA, fill=tema.superficie,
                )
            y = _desenhar_linhas(draw, linhas, f_mono, x + 32, y, tema.destaque, mono_tam)
            y += 16

        else:  # pragma: no cover - o parser só produz os tipos acima
            raise ValueError(f"Bloco desconhecido: {bloco.tipo}")

    return y


def _corpo_que_cabe(blocos: list[Bloco], tema: d.Tema, y_inicial: int,
                    y_limite: int, largura: int) -> tuple[int, bool]:
    """Maior corpo de fonte em que os blocos cabem. Devolve (tamanho, coube)."""
    for tamanho in range(tema.escala.corpo, tema.escala.corpo_min - 1, -2):
        fim = _layout_blocos(blocos, tema, tamanho, d.MARGEM, y_inicial, largura)
        if fim <= y_limite:
            return tamanho, True
    return tema.escala.corpo_min, False


def _titulo_que_cabe(texto: str, tema: d.Tema, maior: int, menor: int,
                     largura: int, altura_max: int) -> tuple[int, list[str]]:
    for tamanho in range(maior, menor - 1, -4):
        f = d.fonte("titulo", tamanho)
        linhas = quebrar(texto, f, largura)
        if len(linhas) * _altura_linha(tamanho) <= altura_max:
            return tamanho, linhas
    f = d.fonte("titulo", menor)
    return menor, quebrar(texto, f, largura)


# ----------------------------------------------------------------- cromo

def _moldura(draw, tema: d.Tema, indice: int, total: int, handle: str) -> None:
    """Faixa do pilar, numeração, handle e seta de continuidade."""
    draw.rectangle([0, 0, d.LARGURA, 10], fill=tema.destaque)

    f_legenda = d.fonte("corpo", tema.escala.legenda)
    if handle:
        draw.text((d.MARGEM, 52), handle, font=f_legenda, fill=tema.texto_suave, anchor="la")
    draw.text((d.LARGURA - d.MARGEM, 52), f"{indice:02d}/{total:02d}",
              font=f_legenda, fill=tema.texto_suave, anchor="ra")

    if indice < total:
        draw.text((d.LARGURA - d.MARGEM, d.ALTURA - d.MARGEM),
                  "→", font=d.fonte("titulo", 52), fill=tema.destaque, anchor="rs")


# ----------------------------------------------------------------- slides

def _render_capa(draw, slide: Slide, tema: d.Tema, avisar=None) -> None:
    # Regra do plano: nada de texto nos 15% de baixo do slide 1.
    limite = int(d.ALTURA * 0.85)
    tamanho, linhas = _titulo_que_cabe(
        slide.titulo, tema, tema.escala.capa_max, tema.escala.capa_min,
        LARGURA_UTIL, altura_max=560,
    )
    if avisar and len(slide.titulo.split()) > 12:
        avisar(f"capa com {len(slide.titulo.split())} palavras — o plano pede no máximo 7")
    altura = len(linhas) * _altura_linha(tamanho)
    y = max(260, (limite - altura) // 2)

    draw.rounded_rectangle([d.MARGEM, y - 40, d.MARGEM + 90, y - 28],
                           radius=6, fill=tema.destaque)
    y = _desenhar_linhas(draw, linhas, d.fonte("titulo", tamanho),
                         d.MARGEM, y, tema.texto, tamanho)

    if slide.blocos:
        y += ESPACO_ENTRE_BLOCOS
        y = _layout_blocos(slide.blocos, tema, tema.escala.corpo,
                           d.MARGEM, y, LARGURA_UTIL, draw=draw)

    draw.text((d.MARGEM, max(y + 40, limite - 60)), "arrasta →",
              font=d.fonte("corpo_medio", 32), fill=tema.destaque, anchor="la")


def _render_conteudo(draw, slide: Slide, tema: d.Tema, avisar=None) -> None:
    tam_titulo, linhas = _titulo_que_cabe(
        slide.titulo, tema, tema.escala.titulo, 40, LARGURA_UTIL, altura_max=260,
    )
    y = _desenhar_linhas(draw, linhas, d.fonte("titulo", tam_titulo),
                         d.MARGEM, 220, tema.destaque, tam_titulo)
    y += 46

    limite = d.ALTURA - d.MARGEM - 90
    tamanho, coube = _corpo_que_cabe(slide.blocos, tema, y, limite, LARGURA_UTIL)
    if not coube and avisar:
        avisar(f"texto vaza do slide mesmo no corpo mínimo ({tema.escala.corpo_min}px) — corte conteúdo")

    # Empurra o bloco para baixo em parte da sobra: slides curtos ficam
    # equilibrados sem que o título saia do lugar entre um slide e outro.
    fim = _layout_blocos(slide.blocos, tema, tamanho, d.MARGEM, y, LARGURA_UTIL)
    y += int(max(0, limite - fim) * 0.35)

    _layout_blocos(slide.blocos, tema, tamanho, d.MARGEM, y, LARGURA_UTIL, draw=draw)


def _render_cta(draw, slide: Slide, tema: d.Tema, avisar=None) -> None:
    tam_titulo, linhas = _titulo_que_cabe(
        slide.titulo, tema, tema.escala.cta_max, tema.escala.cta_min,
        LARGURA_UTIL, altura_max=340,
    )
    y = 380
    y = _desenhar_linhas(draw, linhas, d.fonte("titulo", tam_titulo),
                         d.MARGEM, y, tema.texto, tam_titulo)
    y += 40

    if slide.blocos:
        limite = d.ALTURA - d.MARGEM - 120
        tamanho, coube = _corpo_que_cabe(slide.blocos, tema, y, limite, LARGURA_UTIL)
        if not coube and avisar:
            avisar("CTA longo demais — deixe uma chamada só")
        _layout_blocos(slide.blocos, tema, tamanho, d.MARGEM, y, LARGURA_UTIL, draw=draw)


_RENDERIZADORES = {"capa": _render_capa, "conteudo": _render_conteudo, "cta": _render_cta}


def render_slide(slide: Slide, tema: d.Tema, indice: int, total: int,
                 handle: str = "", avisar=None) -> Image.Image:
    img = Image.new("RGB", (d.LARGURA, d.ALTURA), tema.fundo)
    draw = ImageDraw.Draw(img)
    _moldura(draw, tema, indice, total, handle)
    _RENDERIZADORES[slide.tipo](draw, slide, tema, avisar)
    return img


# A API de publicação do Instagram baixa e aceita JPEG. PNG costuma ser
# rejeitado no container (erro 2207052), então JPEG é o padrão daqui.
FORMATOS = {"jpg": ("JPEG", ".jpg"), "png": ("PNG", ".png")}


def render_roteiro(roteiro: Roteiro, destino: str | Path,
                   avisos: list[str] | None = None,
                   formato: str = "jpg") -> list[Path]:
    """Renderiza o carrossel inteiro. Devolve os caminhos dos PNGs, em ordem.

    Problemas de layout que não impedem a geração (texto vazando, capa longa
    demais) são anexados a `avisos` em vez de virarem exceção.
    """
    if formato not in FORMATOS:
        raise ValueError(f"formato {formato!r} inválido (use {sorted(FORMATOS)})")
    driver, extensao = FORMATOS[formato]

    destino = Path(destino) / roteiro.slug
    destino.mkdir(parents=True, exist_ok=True)
    tema = d.Tema(pilar=roteiro.pilar)
    total = len(roteiro.slides)

    caminhos: list[Path] = []
    for i, slide in enumerate(roteiro.slides, start=1):
        anotar = (lambda msg, n=i: avisos.append(f"slide {n:02d}: {msg}")) if avisos is not None else None
        img = render_slide(slide, tema, i, total, roteiro.handle, anotar)
        caminho = destino / f"{i:02d}{extensao}"
        if driver == "JPEG":
            # subsampling=0 preserva o texto fino; o Instagram recomprime depois.
            img.save(caminho, "JPEG", quality=92, subsampling=0, optimize=True)
        else:
            img.save(caminho, "PNG", optimize=True)
        caminhos.append(caminho)

    if roteiro.legenda:
        (destino / "legenda.txt").write_text(roteiro.legenda + "\n", encoding="utf-8")

    return caminhos
