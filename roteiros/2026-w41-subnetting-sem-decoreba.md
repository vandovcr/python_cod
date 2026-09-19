---
titulo: Subnetting em 5 minutos, sem decoreba
pilar: redes
handle: "@seuperfil"
---

## SUBNETTING SEM DECOREBA

A tabela some na hora da prova. O raciocínio não.

## A única coisa pra decorar

As potências de 2, da direita para a esquerda dentro de um octeto:

```
128  64  32  16  8  4  2  1
```

Com isso você deriva qualquer máscara. Sem isso, nada funciona.

## O que a máscara significa

O prefixo diz quantos bits são de rede. O resto é de host.

- /24 → 24 bits de rede, 8 de host
- 8 bits de host → 2⁸ = 256 endereços

## Quantos hosts cabem

```
hosts = 2^(32 - prefixo) - 2
```

Os dois que somem são o endereço de rede e o de broadcast.

! /24 tem 256 endereços e 254 hosts usáveis. Não 256.

## O truque do bloco

Pegue o último octeto da máscara e subtraia de 256. O resultado é o tamanho do bloco.

- /26 → 255.255.255.192 → 256 − 192 = 64
- /27 → 255.255.255.224 → 256 − 224 = 32
- /28 → 255.255.255.240 → 256 − 240 = 16

## Exemplo completo

192.168.10.0/26 → blocos de 64 endereços:

- .0 a .63 (hosts .1 a .62)
- .64 a .127
- .128 a .191
- .192 a .255

Quatro sub-redes, 62 hosts cada.

## Conferindo na máquina

```
$ ipcalc 192.168.10.0/26
$ sipcalc 192.168.10.0/26
```

Use para conferir a conta, nunca para substituir o raciocínio — na prova não tem terminal.

## Salva e pratica

Faça dez exercícios com /26, /27 e /28. Depois disso não sai mais da cabeça.

Qual prefixo ainda te confunde?

## LEGENDA

Todo mundo aprende subnetting decorando uma tabela. E toda tabela decorada evapora exatamente na hora em que você precisa dela — na prova de certificação ou no meio de um incidente.

O caminho que funciona é outro: decore só as potências de 2 e derive o resto. São três contas e elas resolvem qualquer caso.

O truque do bloco (256 menos o octeto da máscara) é o que mais acelera na prática. Com ele você enxerga as faixas de cabeça, sem papel.

Salva pra treinar. Dez exercícios e vira automático.

#redes #redesdecomputadores #ccna #tcpip #infraestrutura #ti #suportetecnico #networking #carreiraemti #cisco #linux #certificacao
