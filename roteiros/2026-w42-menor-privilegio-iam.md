---
titulo: Princípio do menor privilégio na prática (IAM)
pilar: seguranca
handle: "@seuperfil"
---

## SEU IAM ESTÁ ABERTO DEMAIS

Quatro erros que aparecem em quase todo incidente em nuvem.

## Por que isso importa

Vazamento em nuvem raramente começa com uma falha exótica. Começa com uma credencial que podia mais do que precisava.

! O atacante não precisa invadir o que já está permitido.

## Erro 1: a política com asterisco

Errado:

```
"Action": "*",
"Resource": "*"
```

Certo:

```
"Action": ["s3:GetObject"],
"Resource": "arn:aws:s3:::bucket/rel/*"
```

Ação específica, recurso específico.

## Erro 2: chave de longa duração

Chave de acesso fixa no código, no CI ou no .env do time.

Certo: credencial temporária por role assumida. Em pipeline, use federação OIDC — sem segredo guardado em lugar nenhum.

! Chave que não expira só precisa vazar uma vez.

## Erro 3: humano com acesso direto a produção

Errado: usuário nominal com permissão permanente de escrita em produção.

Certo: acesso por role assumida, com MFA e janela de tempo. O usuário do dia a dia só lê.

## Erro 4: ninguém revisa

Permissão só cresce. Concedida na pressa, nunca removida.

```
$ aws accessanalyzer list-findings-v2 \
    --analyzer-arn <arn-do-analisador>
```

O analisador de acesso não utilizado aponta role e permissão paradas. Trimestralmente: remova o que não foi usado em 90 dias.

## Como começar sem parar tudo

Não tente adivinhar a permissão mínima de primeira — você quebra produção e o time perde a confiança no processo.

- comece permissivo e monitore o uso real
- corte com base no log, não em palpite
- automatize a revisão, senão ela não acontece

## Salva e revisa seu IAM

Abra o console hoje e procure o primeiro asterisco.

Quantos você achou?

## LEGENDA

Quase todo incidente grave em nuvem tem o mesmo parágrafo no relatório final: "a credencial comprometida possuía permissões além do necessário".

Não é falha exótica. É permissão dada na pressa numa sexta-feira e nunca revisada.

O slide que mais gera discussão é o último antes do CTA: não tente acertar a permissão mínima de primeira. Você derruba produção, o time perde a paciência e o processo morre. Comece permissivo, observe o uso real e corte com base em log.

Menor privilégio é destino, não ponto de partida.

Abre o console e procura o primeiro asterisco. Quantos você achou?

#cybersecurity #iam #aws #cloud #seguranca #devops #cloudsecurity #ti #infraestrutura #zerotrust #segurancadainformacao #azure
