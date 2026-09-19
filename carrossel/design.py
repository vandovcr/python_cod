"""Design system dos carrosséis.

Valores espelham a seção 4 de docs/plano-carrossel-instagram.md. Mudou aqui,
mudou em todos os slides gerados — é esse o ponto de ter o design system em código.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache

from PIL import ImageFont

# ---------------------------------------------------------------- dimensões

LARGURA = 1080
ALTURA = 1350          # 4:5 — ocupa mais tela no feed que o quadrado
MARGEM = 100           # área de segurança: o preview do grid corta as bordas
ENTRELINHA = 1.35

# ------------------------------------------------------------------- cores

FUNDO = "#0B1020"
SUPERFICIE = "#151B31"
TEXTO = "#F2F5FF"
TEXTO_SUAVE = "#9AA6C4"
DESTAQUE = "#4DE1C1"
ALERTA = "#FF6B6B"

CORES_PILAR = {
    "redes": "#4DA3FF",
    "seguranca": "#FF6B6B",
    "segurança": "#FF6B6B",
    "cloud": "#9B8CFF",
    "ia": "#4DE1C1",
    "carreira": "#FFC65C",
}

def cor_do_pilar(pilar: str | None) -> str:
    return CORES_PILAR.get((pilar or "").strip().lower(), DESTAQUE)

# ---------------------------------------------------------------- tipografia
#
# Ordem de busca: fontes/ do projeto -> fontes do sistema -> fallback DejaVu.
# Baixe Inter e JetBrains Mono em fontes/ para o resultado do plano; sem elas o
# script continua funcionando com Liberation/DejaVu.

_DIR_FONTES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fontes")

_CANDIDATAS = {
    "titulo": [
        "Inter-Bold.ttf", "SpaceGrotesk-Bold.ttf", "Inter_28pt-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "corpo": [
        "Inter-Regular.ttf", "Inter_28pt-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "corpo_medio": [
        "Inter-Medium.ttf", "Inter_28pt-Medium.ttf", "Inter-SemiBold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "mono": [
        "JetBrainsMono-Regular.ttf", "FiraCode-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ],
}


def _resolver(familia: str) -> str:
    for nome in _CANDIDATAS[familia]:
        caminho = nome if os.path.isabs(nome) else os.path.join(_DIR_FONTES, nome)
        if os.path.exists(caminho):
            return caminho
    raise FileNotFoundError(
        f"Nenhuma fonte encontrada para '{familia}'. "
        f"Coloque um .ttf em {_DIR_FONTES}/ ou instale as fontes DejaVu."
    )


@lru_cache(maxsize=128)
def fonte(familia: str, tamanho: int) -> ImageFont.FreeTypeFont:
    """Carrega (com cache) uma fonte da família pedida no tamanho dado."""
    return ImageFont.truetype(_resolver(familia), tamanho)


# ------------------------------------------------------------- escalas de texto

@dataclass(frozen=True)
class Escala:
    """Tamanhos em px por tipo de slide."""
    capa_max: int = 96
    capa_min: int = 56
    titulo: int = 54
    corpo: int = 40
    corpo_min: int = 32
    mono: int = 32
    legenda: int = 28
    cta_max: int = 72
    cta_min: int = 44


ESCALA = Escala()


@dataclass
class Tema:
    """Agrupa tudo que a renderização precisa saber sobre aparência."""
    pilar: str = ""
    fundo: str = FUNDO
    superficie: str = SUPERFICIE
    texto: str = TEXTO
    texto_suave: str = TEXTO_SUAVE
    alerta: str = ALERTA
    escala: Escala = field(default_factory=lambda: ESCALA)

    @property
    def destaque(self) -> str:
        return cor_do_pilar(self.pilar)
