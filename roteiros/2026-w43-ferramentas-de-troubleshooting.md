---
titulo: ping, traceroute, dig, ss — qual usar quando
pilar: redes
handle: "@seuperfil"
---

## "A REDE ESTÁ LENTA": POR ONDE COMEÇAR

Cinco ferramentas, uma ordem. Suba a pilha, camada por camada.

## dig — o nome resolve?

Primeira pergunta sempre. Se o DNS não responde, testar o resto é perda de tempo.

```
$ dig +short exemplo.com
$ dig @8.8.8.8 exemplo.com
```

! Resolve no 8.8.8.8 mas não no resolver da empresa? O problema é DNS interno, não a aplicação.

## ping — o host responde?

Confirma que existe caminho de ida e volta e mostra a latência.

```
$ ping -c 5 exemplo.com
```

! ICMP bloqueado não significa host fora do ar. Muito firewall descarta ping e serve HTTP normalmente.

## mtr — onde a rota quebra

Melhor que o traceroute puro: mostra perda por salto ao longo do tempo, não um retrato de um instante.

```
$ mtr -rwc 100 exemplo.com
```

Perda que aparece num salto do meio e some no destino é priorização do roteador, não problema real.

## ss — a porta está escutando?

Resolve a dúvida "o serviço subiu mesmo?" sem sair da máquina.

```
$ ss -tlnp
$ ss -tn state established
```

Substituiu o netstat. Mesma ideia, saída mais rápida.

## curl -v — a aplicação responde?

Fecha o ciclo: handshake TLS, redirecionamento, código de status, tempo de cada etapa.

```
$ curl -vso /dev/null \
    -w "%{time_total}" https://exemplo.com
```

## A ordem que economiza uma hora

- dig — o nome resolve
- ping — o host responde
- mtr — o caminho está limpo
- ss — a porta está aberta
- curl — a aplicação responde

! Pular etapa é o que faz troubleshooting virar adivinhação.

## Salva pro próximo incidente

Você vai querer essa sequência às 3h da manhã.

Qual dessas você usa menos do que deveria?

## LEGENDA

"A rede está lenta." A frase mais vaga que existe em suporte — e a que mais consome tempo quando você ataca pelo lugar errado.

A sequência dos slides não é aleatória: ela sobe a pilha. Cada ferramenta só faz sentido depois que a anterior passou. Testar a aplicação antes de confirmar que o nome resolve é onde a maioria perde a primeira hora.

Duas armadilhas que valem repetir:

ICMP bloqueado não é host fora do ar. Um monte de firewall descarta ping e entrega HTTP sem problema nenhum.

E perda de pacote que aparece num salto do meio, mas some no destino, quase sempre é o roteador despriorizando ICMP — não é falha de rota.

Salva. Você vai querer isso às 3h da manhã.

#redes #troubleshooting #linux #suportetecnico #infraestrutura #ti #sre #devops #networking #redesdecomputadores #dns #carreiraemti
