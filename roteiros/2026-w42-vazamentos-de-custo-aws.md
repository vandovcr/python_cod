---
titulo: 6 vazamentos silenciosos na fatura da AWS
pilar: cloud
handle: "@seuperfil"
---

## 6 VAZAMENTOS NA SUA FATURA DA AWS

A conta não cresce por um motivo grande. Cresce por seis pequenos.

## 1. Disco órfão e snapshot antigo

Você apagou a instância. O volume EBS continua lá, cobrando por GB, para sempre.

```
$ aws ec2 describe-volumes \
    --filters Name=status,Values=available
```

Snapshot sem política de retenção acumula anos de backup que ninguém vai restaurar.

## 2. IP público parado

IPv4 público é cobrado por hora — associado ou não.

! Dez IPs esquecidos em projeto encerrado viram uma assinatura mensal que ninguém lembra de ter feito.

## 3. NAT Gateway

Cobra por hora de existência e também por GB processado. O segundo costuma ser a surpresa.

Para tráfego com S3 e DynamoDB, um VPC Endpoint tira esse volume do NAT e corta a conta.

## 4. Transferência entre zonas

Tráfego entre zonas de disponibilidade é cobrado nas duas pontas.

Aplicação numa AZ conversando com banco na outra, o dia inteiro, vira uma linha gorda na fatura.

## 5. Ambiente de desenvolvimento 24/7

Dev e homologação ligados nos fins de semana e à noite.

- 168 horas na semana
- ~50 horas de uso real
- o resto é aluguel de máquina parada

Agendar o desligamento costuma cortar dois terços desse custo.

## 6. Log sem prazo de validade

CloudWatch Logs guarda para sempre se você não disser o contrário.

```
$ aws logs put-retention-policy \
    --log-group-name /aws/lambda/app \
    --retention-in-days 30
```

! Grupo de log criado sem retenção é o vazamento mais silencioso da lista.

## Salva e audita sua conta

Abra o Cost Explorer agrupando por serviço. A surpresa costuma estar no terceiro lugar.

Qual desses você já pagou sem perceber?

## LEGENDA

Fatura de nuvem raramente estoura por causa de uma decisão errada. Ela estoura por seis decisões certas que ninguém revisou depois.

O item que mais pega gente experiente é o NAT Gateway. Todo mundo sabe que ele cobra por hora — e esquece que cobra por GB processado. Aplicação conversando muito com S3 através do NAT gera uma linha na fatura que não tem explicação óbvia no console.

O mais fácil de resolver é o último: política de retenção em log. Leva um comando e corta um custo que só cresce.

Dica de auditoria: abra o Cost Explorer agrupado por serviço e olhe o terceiro colocado. O primeiro e o segundo você já conhece. O terceiro é onde mora a surpresa.

Qual desses você já pagou sem perceber?

#aws #cloud #finops #cloudcomputing #devops #ti #infraestrutura #custos #arquitetura #sre #tecnologia #carreiraemti
