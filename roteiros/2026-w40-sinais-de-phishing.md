---
titulo: 5 sinais de phishing que passam pelo filtro
pilar: seguranca
handle: "@seuperfil"
---

## O PHISHING QUE PASSA PELO FILTRO

5 sinais que o antispam não vê — mas você vê.

## Por que o filtro deixa passar

O antispam barra volume e reputação ruim. Ataque direcionado é um e-mail só, de um domínio novo e limpo.

! O golpe passa no SPF e no DKIM porque o atacante é dono do domínio falso.

## 1. Domínio parecido, não igual

Troca de caractere que o olho corrige sozinho:

- micros0ft.com (zero no lugar do "o")
- rnicrosoft.com ("rn" parece "m")
- empresa-rh.com em vez de rh.empresa.com

```
$ whois suspeito.com | grep -i creation
```

Domínio criado semana passada é bandeira vermelha.

## 2. Remetente e Reply-To diferentes

O "De" mostra o nome bonito. A resposta vai para outro lugar.

```
From: Financeiro <financeiro@empresa.com>
Reply-To: financeiro@empresa-pag.net
```

Abra o cabeçalho completo antes de responder qualquer coisa que envolva dinheiro.

## 3. Urgência combinada com sigilo

"Resolve hoje" e "não comenta com ninguém" na mesma mensagem.

! Urgência existe no trabalho. Sigilo interno não. A dupla é o padrão de fraude do CEO.

## 4. O link não é o que está escrito

O texto diz um domínio, o href aponta para outro. Encurtador em e-mail corporativo também é sinal.

No celular, segure o link para ver o destino antes de tocar.

## 5. O pedido quebra um processo

Mudança de conta bancária por e-mail. Código de MFA pedido por "suporte". Nota fiscal fora do fluxo.

! Nenhum suporte legítimo pede seu código de MFA. Nenhum.

## Salva esse checklist

Cinco segundos de conferência custam menos que um incidente.

Qual desses você já viu chegar na sua caixa?

## LEGENDA

O filtro de spam é ótimo contra campanha em massa. Contra um e-mail só, escrito à mão, de um domínio registrado ontem, ele é quase inútil — e é exatamente esse que dá prejuízo.

O detalhe que quase ninguém sabe: esse e-mail passa em SPF, DKIM e DMARC sem problema. Não porque a autenticação falhou, mas porque o atacante autenticou corretamente um domínio que é dele.

Os 5 sinais estão nos slides. O último é o mais importante.

Qual desses você já pegou chegando?

#cybersecurity #seguranca #phishing #ti #infraestrutura #segurancadainformacao #redes #devops #suportetecnico #lgpd #socanalyst #carreiraemti
