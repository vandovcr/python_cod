# Carrosséis de tecnologia para Instagram

Pipeline para produzir carrosséis sobre **redes, segurança, cloud, IA e carreira**:
o roteiro é um Markdown, os slides são gerados por script e a publicação é
automatizada pela API da Meta.

```
roteiros/*.md  ──>  gerar_carrossel.py  ──>  saida/<post>/*.jpg + legenda.txt
                                                        │
                                              publicar_instagram.py
                                                        │
                                                   post no feed
```

## Uso

```bash
pip install -r requirements.txt

# gera os slides a partir do roteiro
python3 gerar_carrossel.py roteiros/2026-w40-o-que-acontece-ao-digitar-um-site.md

# confere o que seria publicado, sem publicar
python3 publicar_instagram.py saida/2026-w40-o-que-acontece-ao-digitar-um-site --simular

# publica (exige .env configurado)
python3 publicar_instagram.py saida/2026-w40-o-que-acontece-ao-digitar-um-site
```

## Escrevendo um roteiro

Um arquivo por post, em `roteiros/`. Cada `##` vira um slide — o primeiro é a
capa, o último é o CTA.

````markdown
---
titulo: O que acontece quando você digita um site
pilar: redes          # redes | seguranca | cloud | ia | carreira
handle: "@seuperfil"
---

## O QUE ACONTECE DEPOIS QUE VOCÊ APERTA ENTER?
Os 200 ms entre o clique e a página na tela.

## 1. DNS — achar o endereço
O navegador pergunta: "qual é o IP de exemplo.com?"

- cache do browser
- resolver do provedor

```
$ dig exemplo.com +trace
```

## Salva esse post
Qual dessas camadas você trava na hora de explicar?

## LEGENDA
Texto do post, com as hashtags no fim. Não vira slide.
````

Sintaxe disponível dentro de um slide:

| Escreva | Vira |
|---|---|
| texto normal | parágrafo |
| `- item` | bullet |
| cerca de crase | bloco de código em fonte mono |
| `! texto` | destaque em vermelho (alerta) |
| `tipo: capa\|conteudo\|cta` | força o tipo do slide |
| `## LEGENDA` | legenda do post (vai para `legenda.txt`) |

O gerador avisa quando o roteiro quebra as regras do plano — capa com mais de
7 palavras, texto que não cabe no slide.

## Estrutura

| Caminho | O que é |
|---|---|
| `roteiros/` | Os 12 roteiros do primeiro mês, prontos para gerar |
| `docs/plano-carrossel-instagram.md` | Estratégia: pilares, calendário, métricas, backlog de temas |
| `docs/publicacao-automatica-instagram.md` | Como configurar a publicação automática |
| `carrossel/design.py` | Design system (cores, fontes, grid) — mude aqui, muda em tudo |
| `carrossel/roteiro.py` | Parser do Markdown |
| `carrossel/render.py` | Renderização dos slides com Pillow |
| `carrossel/instagram.py` | Cliente da API de publicação da Meta |
| `carrossel/hospedagem.py` | Upload das imagens (S3/R2) — a API baixa por URL |

## Fontes

Sem configuração, o script usa as fontes do sistema (Liberation/DejaVu). Para o
resultado do plano, baixe em `fontes/`:

- [Inter](https://fonts.google.com/specimen/Inter) → `Inter-Bold.ttf`, `Inter-Regular.ttf`, `Inter-Medium.ttf`
- [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) → `JetBrainsMono-Regular.ttf`

## Antes de automatizar a publicação

A API só funciona com **conta Profissional** do Instagram e tem custo de
manutenção (token expira a cada 60 dias, imagens precisam de hospedagem pública).
Se você posta 3x por semana, agendar à mão no Meta Business Suite pode ser mais
sensato — o gerador de slides continua valendo sozinho.
Detalhes em [`docs/publicacao-automatica-instagram.md`](docs/publicacao-automatica-instagram.md).
