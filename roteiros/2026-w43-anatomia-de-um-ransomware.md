---
titulo: Anatomia de um ataque de ransomware, fase por fase
pilar: seguranca
handle: "@seuperfil"
---

## A CRIPTOGRAFIA É O ÚLTIMO PASSO

Quando a tela de resgate aparece, o ataque já acabou. Ele começou semanas antes.

## Fase 1 — entrada

Quase sempre por uma destas quatro portas:

- phishing com anexo ou credencial
- VPN e RDP expostos sem MFA
- vulnerabilidade conhecida e não corrigida
- credencial vazada em outro serviço

! Nenhuma delas é sofisticada. Todas são evitáveis.

## Fase 2 — reconhecimento

O invasor não faz nada barulhento. Ele olha.

Mapeia o domínio, encontra os servidores de arquivo, entende quem é administrador e onde está o backup.

Essa fase costuma durar semanas, não minutos.

## Fase 3 — escalada de privilégio

O objetivo é uma conta de administrador de domínio. Com ela, o resto é trivial.

Caminhos comuns: senha reutilizada, conta de serviço com privilégio alto, falha de configuração no Active Directory.

## Fase 4 — movimento lateral e cópia dos dados

Com privilégio alto, o invasor alcança todo o parque.

! Antes de criptografar, ele copia. É a dupla extorsão: pagar para recuperar e pagar para não vazar. O backup resolve a primeira, não a segunda.

## Fase 5 — destruir o backup

Passo deliberado e sempre anterior à criptografia:

- apaga as cópias de sombra do Windows
- apaga os backups acessíveis pela rede
- desliga o agente de proteção

! Backup que o servidor comprometido consegue apagar não é backup. É cópia.

## Fase 6 — criptografia e resgate

Só aqui a tela aparece. Normalmente fora do horário comercial, para atrasar a resposta.

A essa altura o invasor está no ambiente há semanas e já tem os dados.

## Onde a defesa acontece

Nas fases 1 a 5, não na 6.

- MFA em todo acesso remoto
- correção de vulnerabilidade com prazo
- backup imutável e fora da rede
- monitorar comportamento, não só assinatura

## Salva e revisa seu backup hoje

Uma pergunta só: um administrador comprometido conseguiria apagar suas cópias?

Se a resposta for sim, você tem trabalho pra hoje.

## LEGENDA

O erro mental mais comum sobre ransomware é achar que ele é um evento. Ele é um processo — e a criptografia é o último passo, não o primeiro.

Quando a tela de resgate aparece, o invasor já está no ambiente há semanas. Já mapeou a rede, já conseguiu privilégio de administrador, já copiou os dados e já apagou o que conseguiu alcançar de backup.

É por isso que "eu tenho backup" parou de ser resposta suficiente. Contra dupla extorsão, backup te devolve a operação, mas não impede o vazamento.

A pergunta do último slide é a que vale fazer hoje: um administrador comprometido conseguiria apagar suas cópias? Se sim, você não tem backup — tem cópia.

Defesa acontece nas fases 1 a 5.

#cybersecurity #ransomware #seguranca #segurancadainformacao #backup #ti #infraestrutura #blueteam #soc #lgpd #devops #activedirectory
