# Plano de Carrosséis para Instagram — Tecnologia, Redes, Segurança, IA e Cloud

Documento operacional: do posicionamento ao post publicado. Feito para ser executado
por uma pessoa só, com ~4h/semana de produção.

---

## 1. Posicionamento

**Promessa do perfil:** explicar infraestrutura moderna (redes, cloud, segurança e IA)
em linguagem de quem trabalha com isso — sem jargão vazio e sem "5 dicas de produtividade".

**Público-alvo (ICP):**

| Segmento | Dor principal | O que ele salva/compartilha |
|---|---|---|
| Estudante / transição de carreira | "Por onde começo?" | Roadmaps, glossários, comparativos |
| Analista Jr/Pleno (suporte, NOC, infra) | Quer subir para cloud/segurança | Comandos, troubleshooting, certificações |
| Dev que virou "dono do deploy" | Não domina rede nem IAM | Diagramas, erros comuns, boas práticas |
| Gestor técnico | Precisa de argumento para decidir | Custo, risco, comparativos de arquitetura |

**Tom de voz:** direto, técnico-acessível, primeira pessoa. Sempre um exemplo concreto
(comando, número, incidente real) por carrossel. Zero hype de IA.

---

## 2. Pilares de conteúdo

Cinco pilares, rodízio fixo. Isso evita o "não sei o que postar hoje" e treina o
algoritmo a entender o nicho.

| # | Pilar | Peso | Ângulos que funcionam |
|---|---|---|---|
| 1 | **Redes** | 25% | TCP/IP na prática, DNS, subnetting, troubleshooting, Wireshark |
| 2 | **Segurança** | 25% | OWASP, phishing, hardening, LGPD, análise de incidente |
| 3 | **Cloud** | 20% | AWS/Azure/GCP, IaC, FinOps, arquitetura de referência |
| 4 | **IA** | 20% | LLM na prática, RAG, prompt para infra, riscos e limites |
| 5 | **Carreira/Tech geral** | 10% | Certificações, portfólio, salários, ferramentas |

**Formatos que se repetem (escolha 1 por post):**

- `LISTA` — "7 portas que todo analista precisa saber de cor"
- `ERRO/ACERTO` — "Você está fazendo X. Faça Y."
- `PASSO A PASSO` — "Como investigar lentidão de rede em 6 passos"
- `COMPARATIVO` — "VPN vs. Zero Trust: quando usar cada um"
- `GLOSSÁRIO` — "10 termos de cloud explicados como se você tivesse 12 anos"
- `ESTUDO DE CASO` — "O que derrubou a Cloudflare em 2019 (e a lição)"
- `MITO x VERDADE` — "IA vai substituir o time de segurança?"

---

## 3. Anatomia do carrossel (template de 8 slides)

Formato **1080 × 1350 px (4:5)** — ocupa mais tela no feed que o quadrado.
8 a 10 slides é o ponto ótimo: longo o bastante para gerar tempo de tela,
curto o bastante para a pessoa chegar no fim.

| Slide | Função | Regra |
|---|---|---|
| **1 — Capa** | Parar o scroll | Máx. 7 palavras. Fonte gigante. Promessa clara. Nada de "Olá, pessoal!" |
| **2 — Contexto/dor** | "Isso é sobre você" | 1 frase + por que importa agora |
| **3 a 7 — Conteúdo** | Entregar | 1 ideia por slide. Máx. 40 palavras. Sempre um exemplo/número |
| **8 — CTA** | Converter | Salvar > comentar > seguir. Nunca os três juntos |

**Regras rígidas de layout:**

- Margem de segurança: **100 px** em todos os lados (o Instagram corta as bordas no preview).
- Número do slide no canto (`03/08`) — aumenta a conclusão do carrossel.
- Seta "→" nos slides 1 a 7. Some no último.
- Contraste mínimo **4.5:1** entre texto e fundo (a maioria lê no celular, no sol).
- Nada de texto nos 15% inferiores do slide 1 (a legenda cobre visualmente).

**Gancho da capa — use uma destas 6 fórmulas:**

1. Número + dor: *"3 erros de firewall que eu vi custarem caro"*
2. Contra-intuitivo: *"Seu backup provavelmente não funciona"*
3. Pergunta fechada: *"Você sabe o que acontece ao digitar um site?"*
4. Antes/depois: *"De R$ 8k para R$ 2k na fatura da AWS"*
5. Autoridade emprestada: *"O checklist de hardening que a CIS recomenda"*
6. Alerta: *"Pare de usar senha em chave SSH"*

---

## 4. Identidade visual (design system)

Defina **uma vez** e nunca mude — consistência é o que constrói reconhecimento no feed.

```
Paleta (escura, "terminal", combina com o nicho)
  Fundo         #0B1020   (azul quase preto)
  Superfície    #151B31
  Texto         #F2F5FF
  Texto suave   #9AA6C4
  Destaque      #4DE1C1   (ciano — títulos, números, setas)
  Alerta        #FF6B6B   (só para "erro/nunca faça")

Tipografia
  Títulos   Inter / Space Grotesk — Bold, 64–96 px
  Corpo     Inter — Regular/Medium, 36–44 px
  Código    JetBrains Mono — 32–36 px

Grid
  Canvas 1080 × 1350 · margem 100 px · entrelinha 1.35
  Um bloco de destaque por slide (caixa #151B31, raio 24 px)
```

**Cor por pilar** (faixa fina no topo do slide, ajuda o seguidor a reconhecer o assunto):
Redes `#4DA3FF` · Segurança `#FF6B6B` · Cloud `#9B8CFF` · IA `#4DE1C1` · Carreira `#FFC65C`.

---

## 5. Pipeline de produção (2h para 3 posts)

```
[1] IDEIA        Backlog no Notion/planilha. Nunca comece da folha em branco.
       ↓
[2] ROTEIRO      Escreva os 8 slides em texto puro primeiro. 15 min/post.
       ↓         Regra: se não couber em texto puro, não cabe no slide.
[3] REVISÃO      Checagem técnica: o comando roda? o número está certo? fonte?
       ↓
[4] DESIGN       Canva (template travado) ou script Python + Pillow. 20 min/post.
       ↓
[5] LEGENDA      Gancho repetido + desenvolvimento + CTA + hashtags.
       ↓
[6] AGENDAMENTO  Meta Business Suite. Ter/Qui/Sáb.
       ↓
[7] ENGAJAMENTO  Responder TODO comentário na 1ª hora. É o que mais move alcance.
```

**Lote semanal sugerido (domingo, 2h):** 30 min roteiros → 60 min design → 30 min legendas
e agendamento. Durante a semana só resta responder comentários.

---

## 6. Ferramentas

| Etapa | Opção rápida | Opção "dev" |
|---|---|---|
| Roteiro | Notion / Google Docs | Markdown no repo |
| Design | Canva (template 4:5 travado) | Python + Pillow, ou HTML/CSS + Playwright → PNG |
| Diagramas | Excalidraw | Mermaid → SVG |
| Código bonito | carbon.now.sh | `rich` / `pygments` |
| Agendamento | Meta Business Suite (grátis) | Instagram Graph API |
| Métricas | Insights nativo | Planilha semanal |

> Vantagem do caminho "dev": com os roteiros em Markdown e um script de renderização,
> gerar 8 slides vira `python gerar_carrossel.py roteiros/2026-w40-dns.md`.

---

## 7. Calendário editorial — primeiras 4 semanas

3 posts/semana: **terça, quinta e sábado**, 12h ou 19h.

| Sem | Dia | Pilar | Tema | Formato |
|---|---|---|---|---|
| 1 | Ter | Redes | O que acontece quando você digita um site e aperta Enter | Passo a passo |
| 1 | Qui | Segurança | 5 sinais de phishing que passam pelo filtro | Lista |
| 1 | Sáb | Cloud | IaaS × PaaS × SaaS explicado com pizza | Comparativo |
| 2 | Ter | IA | O que é RAG e por que sua empresa provavelmente precisa | Glossário |
| 2 | Qui | Redes | Subnetting em 5 minutos (sem decoreba) | Passo a passo |
| 2 | Sáb | Carreira | 4 certificações que valem o dinheiro em 2026 | Lista |
| 3 | Ter | Segurança | Princípio do menor privilégio na prática (IAM) | Erro/acerto |
| 3 | Qui | Cloud | Sua fatura da AWS: 6 vazamentos silenciosos de custo | Lista |
| 3 | Sáb | IA | 3 tarefas de infra que dá pra delegar a um LLM hoje | Lista |
| 4 | Ter | Redes | Troubleshooting: ping, traceroute, dig, ss — qual usar quando | Comparativo |
| 4 | Qui | Segurança | Anatomia de um ataque de ransomware, fase por fase | Estudo de caso |
| 4 | Sáb | Cloud | Zero Trust: o que é de verdade (e o que é marketing) | Mito x verdade |

---

## 8. Exemplo pronto — carrossel completo

**Tema:** "O que acontece quando você digita um site e aperta Enter" · Pilar: Redes · 8 slides

```
SLIDE 1 (capa)
  VOCÊ DIGITA UM SITE
  E APERTA ENTER.
  O QUE ACONTECE
  NOS PRÓXIMOS 200 ms?
  → arrasta

SLIDE 2 (contexto)
  Essa é A pergunta clássica de entrevista de infra.
  Quem responde bem mostra que entende a stack inteira.
  Vamos por camadas.

SLIDE 3
  1. DNS — achar o endereço
  O navegador pergunta: "qual o IP de exemplo.com?"
  Ordem de busca: cache do browser → cache do SO →
  resolver do provedor → servidores raiz.
  $ dig exemplo.com +trace

SLIDE 4
  2. TCP — abrir a conversa
  Three-way handshake: SYN → SYN-ACK → ACK.
  Três viagens antes de qualquer byte útil.
  É por isso que latência alta dói mesmo com link rápido.

SLIDE 5
  3. TLS — trancar a porta
  Troca de certificado + chaves de sessão.
  O cadeado não diz que o site é confiável.
  Diz que a conexão é criptografada. Não é a mesma coisa.

SLIDE 6
  4. HTTP — pedir a página
  GET / HTTP/2
  Host: exemplo.com
  O servidor responde com status + headers + corpo.
  200 = ok · 301 = mudou · 404 = não existe · 502 = backend caiu

SLIDE 7
  5. Renderização
  HTML → DOM · CSS → CSSOM · junta tudo → pinta na tela.
  JS pode bloquear esse processo.
  Por isso "otimizar imagem" nem sempre resolve site lento.

SLIDE 8 (CTA)
  Salva esse post.
  Você vai querer revisar antes da próxima entrevista.

  Qual camada você acha mais difícil de explicar?
  Comenta aí 👇
```

**Legenda:**

> Essa pergunta cai em entrevista de infra desde sempre — e ainda derruba gente sênior.
>
> O truque não é decorar as 5 etapas. É conseguir descer o nível de detalhe conforme
> perguntam: começa em "DNS resolve o nome", e se cavarem, você explica cache,
> TTL e iterativo vs. recursivo.
>
> Passei os 200 ms inteiros nos slides. Salva pra revisar depois.
>
> Qual dessas camadas você trava na hora de explicar?
>
> #redes #infraestrutura #ti #devops #cloud #cybersecurity #carreiraemti #dns #tcpip #suportetecnico

---

## 9. Legenda, CTA e hashtags

**Estrutura da legenda (4 blocos):**
1. Primeira linha = repete/amplia o gancho da capa (é o que aparece antes do "mais").
2. 2–4 linhas de desenvolvimento — traga o que **não** coube no carrossel.
3. CTA único e específico.
4. Hashtags no fim.

**CTAs por objetivo:**
- Alcance → "Marca alguém do time que precisa ler isso"
- Salvamento (o sinal mais forte) → "Salva, você vai precisar disso na próxima sprint"
- Comentário → pergunta **fechada**, de opinião, fácil de responder
- Seguidor → "Posto isso 3x por semana. Segue se for útil."

**Hashtags — 10 a 15, em 3 camadas:**
- Amplas (3): `#tecnologia #ti #programacao`
- Nicho (7): `#redesdecomputadores #cybersecurity #cloudcomputing #devops #aws #linux #infraestrutura`
- Long tail (3): `#certificacaoaws #analistadesuporte #zerotrust`

Rode 3 blocos alternados de hashtags e compare o alcance de "não seguidores".

---

## 10. Métricas e otimização

**Acompanhe semanalmente (planilha simples):**

| Métrica | Onde olha | O que significa | Meta inicial |
|---|---|---|---|
| Taxa de salvamento | Salvos ÷ alcance | Valor percebido | > 3% |
| Taxa de compartilhamento | Compart. ÷ alcance | Utilidade social | > 1,5% |
| Retenção do carrossel | Visualizações do último slide | Qualidade do roteiro | > 40% |
| % de não seguidores | Insights → alcance | Potencial de crescimento | > 50% |
| Comentários | — | Conversa real | > 10 |

**Regras de decisão:**
- Capa boa + retenção ruim → problema é o **conteúdo do meio**. Corte slides.
- Retenção boa + salvamento baixo → conteúdo é interessante mas **não é útil**. Adicione comando/checklist.
- Alcance baixo geral → problema é a **capa**. Teste outra fórmula de gancho.
- Post que estourou: refaça o tema em 60 dias com outro ângulo. Funciona de novo.

**Ciclo:** a cada 12 posts, ranqueie por salvamento. Os 3 melhores viram série;
os 3 piores saem do calendário.

---

## 11. Checklist de publicação

```
ROTEIRO
[ ] Capa com no máximo 7 palavras
[ ] Uma ideia por slide
[ ] Pelo menos 1 número, comando ou exemplo concreto
[ ] Informação técnica conferida em fonte oficial
[ ] Slide final com CTA único

DESIGN
[ ] 1080 × 1350 px, margem de 100 px respeitada
[ ] Contraste conferido (legível no celular, no sol)
[ ] Numeração dos slides e seta de continuidade
[ ] Faixa de cor do pilar correta
[ ] Sem erro de digitação (leia de trás pra frente)

PUBLICAÇÃO
[ ] Primeira linha da legenda repete o gancho
[ ] 10–15 hashtags em 3 camadas
[ ] Texto alternativo preenchido (acessibilidade + SEO)
[ ] Agendado para Ter/Qui/Sáb, 12h ou 19h
[ ] Bloco de 30 min reservado para responder comentários
```

---

## 12. Backlog — 30 ideias prontas

**Redes:** subnetting sem decoreba · DNS: A, CNAME, MX, TXT · NAT explicado · TCP vs. UDP com analogia
· o que o traceroute realmente mostra · VLAN na prática · por que seu Wi-Fi cai às 19h

**Segurança:** OWASP Top 10 em 10 slides · MFA: por que SMS é o pior fator · como ler um log de auth
· LGPD para time técnico · hardening de servidor Linux em 7 passos · o que fazer na 1ª hora de um incidente

**Cloud:** regiões e zonas de disponibilidade · IAM: os 5 erros mais caros · Terraform em 8 slides
· FinOps: 6 vazamentos de custo · serverless: quando NÃO usar · backup 3-2-1 na nuvem

**IA:** token, contexto e por que o modelo "esquece" · RAG vs. fine-tuning · alucinação: por que acontece
· IA em SOC: o que já funciona · prompt injection · custo real de rodar um LLM

**Carreira:** portfólio de infra sem experiência · homelab com R$ 500 · 4 certificações que valem
· como estudar para AWS SAA · o que perguntar na entrevista

---

## 13. Próximos passos

1. **Semana 0** — fechar paleta e tipografia; montar 1 template mestre no Canva (ou o script Python).
2. **Semana 0** — escrever os 12 roteiros da tabela da seção 7, em Markdown, neste repo.
3. **Semana 1** — publicar os 3 primeiros; medir.
4. **Semana 4** — revisar métricas, cortar o que não salvou, dobrar no que salvou.

**Automação possível (este repo é Python):** um script `gerar_carrossel.py` que lê um
roteiro em Markdown (um slide por `##`) e renderiza os 8 PNGs com Pillow, aplicando o
design system da seção 4 automaticamente. Elimina a etapa manual de design.
