# Publicação automática no Instagram

Como sair de um roteiro em Markdown para um carrossel publicado, sem abrir o app.

> **Antes de tudo:** não existe API oficial do Instagram para conta pessoal.
> Automação só funciona com **conta Profissional** (Empresa ou Criador de
> conteúdo) e passa pela API de publicação de conteúdo da Meta. Ferramentas que
> prometem postar de conta pessoal usam automação de navegador — é violação dos
> termos de uso e o caminho mais rápido para tomar bloqueio.

---

## Como o fluxo funciona

A API não recebe o arquivo: ela **baixa a imagem de uma URL pública**. Por isso o
pipeline tem uma etapa de hospedagem no meio.

```
roteiro.md ──> gerar_carrossel.py ──> 8 JPEGs
                                         │
                                         ▼
                              hospedagem (R2/S3) ──> URLs https públicas
                                         │
                                         ▼
     POST /media (1 por imagem) ──> POST /media (CAROUSEL) ──> POST /media_publish
                                         │
                                         ▼
                                    post no feed
```

Três detalhes que derrubam quem tenta pela primeira vez:

1. **JPEG, não PNG.** O container costuma falhar com PNG (erro `2207052`).
   O gerador já produz `.jpg` por padrão.
2. **URL pública de verdade.** Precisa ser HTTPS e acessível sem login. Link do
   Google Drive, do Dropbox ou de repositório privado **não funciona** — a Meta
   recebe HTML de redirecionamento em vez da imagem.
3. **Espere o container ficar `FINISHED`.** Publicar enquanto está `IN_PROGRESS`
   retorna erro. O `publicar_instagram.py` já faz esse polling.

---

## Passo 1 — Preparar a conta

1. No app do Instagram: **Configurações → Tipo de conta → Mudar para conta
   profissional**. Escolha Criador de conteúdo ou Empresa.
2. Guarde o `@` do perfil. Você vai precisar do **ID numérico**, não do @ — ele
   sai no passo 3.

---

## Passo 2 — Criar o app na Meta

Acesse [developers.facebook.com/apps](https://developers.facebook.com/apps) →
**Criar app**. Há dois caminhos; escolha um.

### Caminho A — Instagram Login (recomendado para perfil solo)

Não exige Página do Facebook. Menos etapas, menos coisa para quebrar.

1. Tipo do app: **Empresa** (Business).
2. Adicione o produto **Instagram** → *Configuração da API com login do Instagram*.
3. Permissões: `instagram_business_basic` e `instagram_business_content_publish`.
4. Vincule sua conta do Instagram e clique em **Gerar token**.
5. Copie o token (60 dias de validade) e o **ID de usuário** exibido na mesma tela.

No `.env`: `IG_LOGIN=instagram`

### Caminho B — Facebook Login (Instagram Graph API)

Exige uma Página do Facebook vinculada ao Instagram. Use se você já tem essa
estrutura ou precisa de outras APIs da Meta.

1. Tipo do app: **Empresa**. Adicione o produto **Instagram Graph API**.
2. Permissões: `instagram_basic`, `instagram_content_publish`,
   `pages_show_list`, `pages_read_engagement`.
3. Abra o [Graph API Explorer](https://developers.facebook.com/tools/explorer/),
   selecione o app, marque as permissões e gere um **token de usuário**.

No `.env`: `IG_LOGIN=facebook`

---

## Passo 3 — Descobrir seu `IG_USER_ID`

**Caminho A:**

```bash
curl -s "https://graph.instagram.com/v21.0/me?fields=user_id,username&access_token=$TOKEN"
```

**Caminho B** (duas chamadas — Página primeiro, conta do Instagram depois):

```bash
# 1) o ID da sua Página
curl -s "https://graph.facebook.com/v21.0/me/accounts?access_token=$TOKEN"

# 2) a conta do Instagram vinculada a ela
curl -s "https://graph.facebook.com/v21.0/<PAGE_ID>?fields=instagram_business_account&access_token=$TOKEN"
```

O `instagram_business_account.id` é o seu `IG_USER_ID`.

---

## Passo 4 — Token de longa duração

O token do Explorer dura ~1 hora. Troque por um de **60 dias**.

**Caminho B (Facebook):**

```bash
curl -s "https://graph.facebook.com/v21.0/oauth/access_token\
?grant_type=fb_exchange_token\
&client_id=<APP_ID>\
&client_secret=<APP_SECRET>\
&fb_exchange_token=<TOKEN_CURTO>"
```

Ou em Python: `carrossel.instagram.trocar_por_token_longo(...)`.

**Caminho A (Instagram):** o token do painel já é de 60 dias. Renove a cada
~50 dias, antes de expirar:

```python
from carrossel.instagram import renovar_token_instagram
print(renovar_token_instagram(meu_token))
```

> Coloque um lembrete no calendário a cada 50 dias. Token expirado é a causa
> nº 1 de automação de Instagram que "parou de funcionar sozinha".

---

## Passo 5 — Hospedagem das imagens

A opção mais barata e confiável é **Cloudflare R2**: camada gratuita de 10 GB e
**sem cobrança de egresso** (S3 cobra a transferência que a Meta faz ao baixar).

1. Painel Cloudflare → **R2** → criar bucket (ex.: `carrosseis`).
2. Em *Settings* do bucket → **Public access** → ative o domínio `r2.dev`.
   Anote a URL (`https://pub-xxxxxxxx.r2.dev`).
3. **Manage R2 API Tokens** → criar token com permissão de *Object Read & Write*.

Preencha no `.env`:

```bash
S3_BUCKET=carrosseis
S3_BASE_PUBLICA=https://pub-xxxxxxxx.r2.dev
S3_ENDPOINT=https://<ACCOUNT_ID>.r2.cloudflarestorage.com
S3_REGION=auto
S3_ACCESS_KEY_ID=...
S3_SECRET_ACCESS_KEY=...
```

Funciona igual com AWS S3, Backblaze B2 ou MinIO — só muda o `S3_ENDPOINT`.

**Não quer bucket?** Hospede os JPEGs onde preferir (GitHub Pages, Netlify,
servidor próprio) e publique com `--base-url`:

```bash
python3 publicar_instagram.py saida/meu-post --base-url https://cdn.seudominio.com
```

O script apaga as imagens da hospedagem depois de publicar — o Instagram já fez
a cópia dele. Use `--manter` se quiser guardar.

---

## Passo 6 — Publicar

```bash
pip install -r requirements.txt
cp .env.exemplo .env      # preencha com os valores dos passos 3 a 5

# 1. gera os slides
python3 gerar_carrossel.py roteiros/2026-w40-o-que-acontece-ao-digitar-um-site.md

# 2. confere sem publicar
python3 publicar_instagram.py saida/2026-w40-o-que-acontece-ao-digitar-um-site --simular

# 3. publica
python3 publicar_instagram.py saida/2026-w40-o-que-acontece-ao-digitar-um-site
```

Saída esperada:

```
carrossel: 2026-w40-o-que-acontece-ao-digitar-um-site
  8 slides: 01.jpg, ... 08.jpg
  legenda: 533 caracteres
  hospedado em https://pub-xxxx.r2.dev/2026-w40-.../
  quota 24h: 3/50
  item 1/8 → container 17998...
  ...
  carrossel → container 17999...
  publicado → media 18000...
  hospedagem temporária limpa

✓ publicado — media ID 18000...
```

---

## Passo 7 — Agendar

### Opção 1 — cron na sua máquina ou VPS

```cron
# Ter, Qui e Sáb às 12h (BRT). O servidor precisa estar ligado.
0 12 * * 2,4,6  cd /caminho/python_cod && /usr/bin/python3 publicar_instagram.py saida/proximo >> ~/carrossel.log 2>&1
```

### Opção 2 — GitHub Actions (não precisa de máquina ligada)

`.github/workflows/publicar.yml`:

```yaml
name: Publicar carrossel
on:
  schedule:
    - cron: "0 15 * * 2,4,6"   # 15h UTC = 12h BRT
  workflow_dispatch:
    inputs:
      pasta:
        description: "Pasta do carrossel em saida/"
        required: true

jobs:
  publicar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python3 gerar_carrossel.py roteiros/${{ inputs.pasta }}.md
      - run: python3 publicar_instagram.py saida/${{ inputs.pasta }}
        env:
          IG_USER_ID: ${{ secrets.IG_USER_ID }}
          IG_ACCESS_TOKEN: ${{ secrets.IG_ACCESS_TOKEN }}
          IG_LOGIN: ${{ secrets.IG_LOGIN }}
          S3_BUCKET: ${{ secrets.S3_BUCKET }}
          S3_BASE_PUBLICA: ${{ secrets.S3_BASE_PUBLICA }}
          S3_ENDPOINT: ${{ secrets.S3_ENDPOINT }}
          S3_ACCESS_KEY_ID: ${{ secrets.S3_ACCESS_KEY_ID }}
          S3_SECRET_ACCESS_KEY: ${{ secrets.S3_SECRET_ACCESS_KEY }}
```

Guarde tudo em **Settings → Secrets and variables → Actions**. Nunca comite o `.env`.

### Opção 3 — Meta Business Suite (sem código)

Para quem não quer manter automação: gere os JPEGs com o script e agende à mão
em [business.facebook.com](https://business.facebook.com) → Planejador. Leva 2
minutos por post e não tem token para renovar.

> **Recomendação honesta:** comece pela opção 3. Migre para a 1 ou 2 quando o
> volume justificar. Automação de publicação tem um custo de manutenção real
> (token, mudança de versão da API, hospedagem) que só compensa com frequência alta.

---

## Limites da API

| Limite | Valor |
|---|---|
| Publicações por conta | 50 por 24h (carrossel conta como 1) |
| Itens por carrossel | 2 a 10 |
| Tamanho da imagem | até 8 MB, JPEG |
| Proporção aceita | 0.8 (4:5) a 1.91:1 |
| Legenda | 2.200 caracteres |
| Hashtags | 30 por post |
| Validade do container | 24h após criado |

Consultar a quota gastada:

```bash
curl -s "https://graph.facebook.com/v21.0/<IG_USER_ID>/content_publishing_limit\
?fields=config,quota_usage&access_token=$TOKEN"
```

**Não dá para automatizar pela API:** marcar pessoas em carrossel de imagem,
adicionar música, publicar em conta pessoal, editar um post já publicado.

---

## Erros comuns

| Erro | Causa provável | O que fazer |
|---|---|---|
| `(#190) Access token has expired` | Passaram-se os 60 dias | Renove (passo 4) |
| `(#200) Permissions error` | Falta `instagram_content_publish` | Revise as permissões e gere o token de novo |
| `(#100) media_type` inválido | `children` vazio ou mal formado | Confira os IDs dos containers |
| `2207052` / mídia não processada | PNG, arquivo grande ou URL lenta | Use JPEG; confira a URL no navegador anônimo |
| `2207003` não consegui baixar | URL não é pública | Abra a URL numa aba anônima — tem que baixar direto |
| Container preso em `IN_PROGRESS` | Hospedagem lenta | Aumente `tentativas` em `Publicador.aguardar` |
| `The app is in development mode` | App não publicado | Em modo dev só funciona com contas de teste; publique o app |

**Dica de depuração:** antes de culpar a API, cole a URL da imagem numa janela
anônima. Se não baixar o JPEG direto, o problema é hospedagem, não Instagram.

---

## Segurança

- `.env` está no `.gitignore`. Confirme com `git check-ignore -v .env` antes do
  primeiro commit.
- Token do Instagram dá acesso de publicação ao seu perfil — trate como senha.
- Em CI, use apenas secrets. Nunca `echo` do token em log.
- Se vazar: Meta for Developers → app → **Invalidar token** e gere outro.
