---
titulo: O que é RAG e por que sua empresa provavelmente precisa
pilar: ia
handle: "@seuperfil"
---

## RAG EXPLICADO SEM ENROLAÇÃO

O modelo não sabe nada da sua empresa. RAG resolve isso.

## O problema

Um LLM aprendeu com a internet até certa data. Ele nunca viu o seu manual interno, o seu contrato, o seu chamado de ontem.

! Perguntar mesmo assim não devolve "não sei". Devolve algo plausível e errado.

## RAG em uma frase

Antes de responder, busque o trecho certo do seu material e cole no prompt.

RAG = Retrieval-Augmented Generation. Geração aumentada por recuperação.

## Como funciona: indexar

Você quebra os documentos em pedaços e transforma cada pedaço em um vetor — uma lista de números que representa o significado.

Tudo isso vai para um banco vetorial.

## Como funciona: responder

A pergunta do usuário também vira vetor. O sistema busca os pedaços mais próximos e monta o prompt:

```
Contexto: <trechos recuperados>
Pergunta: <pergunta do usuário>
Responda usando apenas o contexto.
```

## Por que não fine-tuning

Fine-tuning ensina formato e estilo. É caro e lento para ensinar fatos.

! Documento mudou? No RAG você troca o arquivo. No fine-tuning você treina tudo de novo.

## Onde o RAG quebra

Se a busca traz o trecho errado, o modelo responde errado com toda a confiança do mundo.

- pedaço grande demais dilui o sentido
- pedaço pequeno demais perde o contexto
- sem citação da fonte ninguém consegue auditar

! Qualidade de RAG é 80% recuperação e 20% modelo.

## Salva pra próxima reunião

Quando pedirem "uma IA que responde sobre nossos documentos", é isso que estão pedindo.

Sua empresa já tentou? Deu certo?

## LEGENDA

"Queremos uma IA que responda sobre os nossos documentos." Essa frase virou pauta de reunião em toda empresa — e quase sempre o que estão pedindo é RAG, não treinar um modelo.

A parte que mais gera frustração em projeto de RAG não é o modelo. É a recuperação. Um projeto com modelo de ponta e busca mal ajustada entrega resposta pior que um projeto simples com busca bem feita.

Por isso a regra que fecha o carrossel: 80% recuperação, 20% modelo. Se o seu RAG está ruim, provavelmente o problema não é o LLM.

Sua empresa já tentou? Parou em qual etapa?

#ia #inteligenciaartificial #rag #llm #machinelearning #dados #ti #cloud #devops #tecnologia #arquitetura #carreiraemti
