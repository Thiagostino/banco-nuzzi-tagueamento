# Contexto para a IA · Banco Nuzzi

Este arquivo é o contexto de projeto que uma IA precisa ler antes de responder perguntas ou tomar decisões com os dados do app. Ele cobre o que não cabe na descrição de um evento: termos do negócio, funis, métricas e regras que valem para todos os eventos.

## O app

App fictício de banco para testes de tagueamento. Tem uma tela de acesso deslogada (`/acesso`), a tela de senha (`/entrar`) e a área logada com cinco abas: Início, Extrato, Pix, Cartões e Investimentos. Cada tela é uma página virtual com rota por `#hash`.

## Glossário

| Termo | Significado no app |
| --- | --- |
| Área logada | Telas com `page_type = area_logada`. Só abrem depois do evento `login`. |
| Tela de acesso | Primeira tela do app para quem não está logado (`/acesso`, `page_type = publico`). |
| Página virtual | Troca de tela sem recarregar a página. Gera `page_view` com o `page_path` da rota. |
| Banner interno | Peça de campanha dentro do app, identificada por `promotion_id`. Catálogo em `tracking-plan.json`, chave `catalogs.banners`. |
| Posição (`creative_slot`) | Lugar do banner na tela: `acesso_destaque_1`, `inicio_oferta_2`, `cartoes_oferta_1` e assim por diante. |
| Pix | Transferência instantânea. O funil tem três etapas: dados, revisão e comprovante. |
| Chave Pix | Identificador de quem recebe (e-mail, celular, CPF, CNPJ ou aleatória). Nunca entra no dataLayer; só o tipo vai em `pix_key_type`. |
| CDI | Taxa de referência da renda fixa. "104% do CDI" é a rentabilidade do CDB Liquidez Diária. |
| Segmento (`customer_segment`) | Classificação comercial do cliente. No teste, sempre `pf_alta_renda`. |
| Lead | Pedido de quem ainda não é cliente (`generate_lead`). Interesse de cliente logado em oferta é `offer_click`. |

## Funis

| Funil | Etapas, em ordem | Observação |
| --- | --- | --- |
| Login | `form_start` → `login` | `login_error` registra cada recusa entre as etapas. `auth_required` antes de `form_start` indica que o cliente queria uma tela específica (`target_path`). |
| Pix | `pix_start` → `pix_review` → `pix_success` | `pix_error` e `pix_edit` são perdas ou voltas entre as etapas. Só `pix_success` conta como Pix concluído. |
| Banner | `view_promotion` → `select_promotion` → evento da ação | A ação pode ser `generate_lead`, `offer_click`, `card_request` ou um `page_view` da tela de destino. Use o mesmo `promotion_id` em todas as etapas. |

## Métricas

| Métrica | Como calcular |
| --- | --- |
| Taxa de toque de banner | `select_promotion` ÷ `view_promotion`, por `promotion_id` e `creative_slot` |
| Conversão do login | clientes com `login` ÷ clientes com `form_start` |
| Taxa de erro do login | `login_error` ÷ (`login` + `login_error`), por `error_type` |
| Conversão do Pix | `pix_success` ÷ `pix_start` |
| Valor de Pix pelo app | soma de `value` em `pix_success` (moeda em `currency`) |
| Demanda por atalhos sem fluxo | contagem de `quick_action` por `action_id` |

## Regras que valem para todos os eventos

- `user_id` só existe depois do `login`. Em `page_view` deslogado ele vai como `undefined`, para limpar o valor anterior no GTM.
- Nenhum evento carrega senha, agência, conta, saldo, valor de fatura ou chave Pix.
- IDs são sempre texto. Valores em dinheiro são número com ponto decimal.
- Um toque num botão de banner gera dois eventos: `select_promotion` e, quando existe, o evento da ação. Não some os dois como se fossem dois toques.
- `view_promotion` mede exposição real (60% do banner visível), uma vez por banner a cada `page_view`.
- O banner do Black na tela de acesso não gera `card_request`. Ele leva ao login (`auth_required`) e à tela Cartões.

## Perguntas que a IA não deve responder com estes dados

- Quem é o cliente. O `user_id` é pseudonimizado de propósito.
- Saldo, fatura ou patrimônio do cliente. Esses valores não são coletados.
- Se um Pix chegou ao destino. `pix_success` registra o envio pelo app; a liquidação está no core bancário, ligada por `transaction_id`.
