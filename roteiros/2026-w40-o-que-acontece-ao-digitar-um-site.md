---
titulo: O que acontece quando você digita um site e aperta Enter
pilar: redes
handle: "@seuperfil"
---

## O QUE ACONTECE DEPOIS QUE VOCÊ APERTA ENTER?

Os 200 ms entre o clique e a página na tela.

## A pergunta clássica de entrevista

Quem responde bem mostra que entende a stack inteira — do cabo ao pixel.

Vamos por camadas.

## 1. DNS — achar o endereço

O navegador pergunta: "qual é o IP de exemplo.com?"

- cache do browser
- cache do sistema operacional
- resolver do provedor
- servidores raiz

```
$ dig exemplo.com +trace
```

## 2. TCP — abrir a conversa

Three-way handshake: SYN, SYN-ACK, ACK.

São três viagens de ida e volta antes de qualquer byte útil trafegar.

! É por isso que latência alta dói mesmo com link de 1 Gbps.

## 3. TLS — trancar a porta

Troca de certificado e derivação das chaves de sessão.

! O cadeado não diz que o site é confiável. Diz que a conexão é criptografada. Não é a mesma coisa.

## 4. HTTP — pedir a página

```
GET / HTTP/2
Host: exemplo.com
```

- 200 — deu certo
- 301 — mudou de lugar
- 404 — não existe
- 502 — o backend caiu

## 5. Renderização

HTML vira DOM. CSS vira CSSOM. O browser junta os dois e pinta a tela.

JavaScript pode bloquear esse processo — por isso "otimizar imagem" nem sempre resolve site lento.

## Salva esse post

Você vai querer revisar isso antes da próxima entrevista.

Qual dessas camadas você trava na hora de explicar?

## LEGENDA

Essa pergunta cai em entrevista de infra desde sempre — e ainda derruba gente sênior.

O truque não é decorar as 5 etapas. É conseguir descer o nível de detalhe conforme perguntam: começa em "DNS resolve o nome" e, se cavarem, você explica cache, TTL e resolução iterativa vs. recursiva.

Passei os 200 ms inteiros nos slides. Salva pra revisar depois.

Qual dessas camadas você trava na hora de explicar?

#redes #infraestrutura #ti #devops #cloud #cybersecurity #carreiraemti #dns #tcpip #suportetecnico #linux #redesdecomputadores
