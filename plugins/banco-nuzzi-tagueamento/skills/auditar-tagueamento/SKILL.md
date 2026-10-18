---
name: auditar-tagueamento
description: >
  Audita o tagueamento do app Banco Nuzzi contra o tracking plan e as regras de governança.
  Use em homologação, antes de publicar uma versão do GTM, ou quando alguém desconfiar de um
  número. Aponta divergências, dado pessoal, descrições fracas e eventos duplicados.
---

# Auditar o tagueamento do Banco Nuzzi

## Ciclo

1. **Detectar.** Rode `python3 tools/validar_plano.py`. Depois percorra o `tracking-plan.json` inteiro com os critérios abaixo. Toda conclusão precisa de evidência (arquivo e linha, ou o evento visto no Modo de visualização do GTM).
2. **Esclarecer.** Antes de propor mudança, faça uma pergunta por vez sobre o significado de negócio que não está escrito.
3. **Resolver.** Corrija primeiro a documentação. Mudança de nome ou remoção de evento passa por descontinuação: marque `Descontinuado`, mantenha o evento por um ciclo e avise quem usa.
4. **Prevenir.** Registre a regra que evitaria o problema na skill `taxonomia` ou no `contexto-ia.md`.

## Critérios, do mais grave ao menos grave

| Gravidade | O que procurar |
| --- | --- |
| Bloqueia | Dado pessoal ou financeiro do cliente em qualquer parâmetro, inclusive em `link_text` montado a partir de texto da tela |
| Bloqueia | Evento no código sem documentação, ou documentado sem existir no código |
| Alta | Nome de evento fora do catálogo de eventos GA4 do TagOps |
| Alta | Botão ou link sem `data-click` (toque sem `click`) |
| Alta | Parâmetro opcional omitido em vez de `undefined`, que deixa o GTM ler um valor antigo |
| Alta | Dois eventos para o mesmo gesto sem diferença documentada |
| Média | Descrição só técnica, sem `behavior` em linguagem de negócio ou sem `disambiguation` |
| Média | Mesmo conceito com nomes diferentes entre eventos |
| Baixa | Exemplo, owner ou valores possíveis desatualizados |

## Pontos conhecidos

- Todo nome de evento precisa existir no catálogo de eventos GA4 do TagOps (automatic ou recommended). Evento personalizado é divergência de gravidade Alta.
- `click` e o evento de negócio saem no mesmo toque. Contar os dois como dois toques é erro de análise, não de tagueamento.
- `form_submit` leva parâmetros do login e do Pix; os que não se aplicam vão como `undefined`. Um valor herdado do envio anterior no GTM é divergência Alta.
- Arrastar o carrossel não gera `click`; a exposição do banner novo é `view_promotion`.

## Como reportar

Uma tabela com gravidade, evento, evidência e correção proposta, ordenada pela gravidade. Comece pela correção de maior impacto e diga por quê. Não aplique mudança no plano ou no código sem confirmação.
