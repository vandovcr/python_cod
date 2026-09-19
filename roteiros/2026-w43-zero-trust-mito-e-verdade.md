---
titulo: Zero Trust — o que é de verdade e o que é marketing
pilar: cloud
handle: "@seuperfil"
---

## ZERO TRUST NÃO É UM PRODUTO

Três mitos que fornecedor adora e uma definição que resolve.

## Mito 1: dá para comprar

Não existe caixa de Zero Trust. É um modelo de arquitetura, descrito em documento público (NIST SP 800-207).

! Quando um fornecedor diz que vende Zero Trust, ele está vendendo um pedaço e chamando de tudo.

## Mito 2: é a VPN nova

Zero Trust substitui o modelo de perímetro, não uma ferramenta específica.

Trocar VPN por ZTNA pode ser consequência do caminho, mas fazer só isso e parar por aí é rebatizar a VPN.

## Mito 3: não confiar em ninguém

O nome é infeliz. Não se trata de ausência de confiança — se trata de confiança verificada a cada acesso, em vez de concedida uma vez na entrada.

! O modelo antigo confiava em quem já estava dentro da rede. Esse é o problema que o Zero Trust ataca.

## O que é de verdade: 3 princípios

- verificar explicitamente — identidade, dispositivo e contexto a cada requisição
- menor privilégio — acesso mínimo, pelo tempo mínimo
- assumir violação — projetar como se o invasor já estivesse dentro

## Como isso aparece na prática

- MFA resistente a phishing, não SMS
- acesso por aplicação, não por faixa de rede
- postura do dispositivo avaliada antes de liberar
- microssegmentação para conter movimento lateral
- telemetria e registro de tudo

## Por onde começar

Na ordem, pelo que dá mais resultado por esforço:

- MFA forte em tudo que é remoto
- inventário de identidades e remoção de contas órfãas
- eliminar acesso permanente a produção

! Começar por microssegmentação é o erro clássico. É a parte mais cara e a que menos entrega no início.

## Salva antes da próxima reunião

Quando ouvir "nossa solução é Zero Trust", pergunte qual dos três princípios ela cobre.

Sua empresa está em qual estágio?

## LEGENDA

Zero Trust virou etiqueta de marketing e perdeu o sentido. Vale voltar ao documento original: NIST SP 800-207. É público, é curto e não vende nada.

O nome atrapalha. Não é sobre desconfiar de todo mundo — é sobre verificar sempre, em vez de confiar uma vez na entrada e liberar o resto da rede. O modelo de perímetro tratava "estar dentro" como prova de identidade. Era isso que quebrava.

A parte prática que mais vejo errada é a ordem. Time começa por microssegmentação, que é cara, demorada e entrega pouco no início. O retorno rápido está em MFA resistente a phishing e em limpar identidade órfã.

Dica pra próxima reunião com fornecedor: pergunte qual dos três princípios a solução cobre. A resposta costuma ser reveladora.

#zerotrust #cybersecurity #cloud #seguranca #cloudsecurity #ti #infraestrutura #iam #devops #arquitetura #segurancadainformacao #nist
