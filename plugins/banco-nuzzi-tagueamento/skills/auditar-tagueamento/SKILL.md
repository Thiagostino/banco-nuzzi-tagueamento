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
| Alta | Parâmetro opcional omitido em vez de `undefined`, que deixa o GTM ler um valor antigo |
| Alta | Dois eventos para o mesmo gesto sem diferença documentada |
| Média | Descrição só técnica, sem `behavior` em linguagem de negócio ou sem `disambiguation` |
| Média | Mesmo conceito com nomes diferentes entre eventos |
| Baixa | Exemplo, owner ou valores possíveis desatualizados |

## Pontos conhecidos

- `offer_click` dispara no mesmo toque que `select_promotion` e não acrescenta informação além de `offer_id`. Status "Ajustar": decidir se sai ou se vira o único evento de intenção da oferta.
- O carrossel dispara `carousel_navigate` quando a rolagem para. Um arrasto que passa por dois banners gera um evento, com o banner final.
- `auth_required` vai sem `page_path` quando o app já abre numa tela logada.

## Como reportar

Uma tabela com gravidade, evento, evidência e correção proposta, ordenada pela gravidade. Comece pela correção de maior impacto e diga por quê. Não aplique mudança no plano ou no código sem confirmação.
