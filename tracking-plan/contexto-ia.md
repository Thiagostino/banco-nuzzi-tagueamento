# Contexto para a IA · Banco Nuzzi

Este arquivo é o contexto de projeto que uma IA precisa ler antes de responder perguntas ou tomar decisões com os dados do app. Ele cobre o que não cabe na descrição de um evento: termos do negócio, funis, métricas e regras que valem para todos os eventos.

## O app

App fictício de banco para testes de tagueamento. Tem uma tela de acesso deslogada (`/acesso`), a tela de senha (`/entrar`) e a área logada com cinco abas: Início, Extrato, Pix, Cartões e Investimentos. Cada tela é uma página virtual com rota por `#hash`.

## Os 9 eventos

Todos os nomes vêm do catálogo de eventos GA4 do TagOps. Nenhum evento é personalizado.

| Evento | Tipo no catálogo | O que registra |
| --- | --- | --- |
| `page_view` | automatic | Tela vista (página virtual) |
| `click` | automatic | Todo toque em botão ou link do app (`link_id` diz qual) |
| `view_promotion` | recommended | Banner interno visível na tela |
| `select_promotion` | recommended | Toque no botão de um banner |
| `form_start` | automatic | Início do preenchimento da senha ou do Pix |
| `form_submit` | automatic | Envio da senha ou do Pix, com o resultado em `step` |
| `login` | recommended | Login aceito |
| `generate_lead` | recommended | Pedido de abertura de conta ou de cartão |
| `select_item` | recommended | Produto de investimento escolhido para aplicar |

## Glossário

| Termo | Significado no app |
| --- | --- |
| Área logada | Telas com `page_type = area_logada`. Só abrem depois do evento `login`. |
| Tela de acesso | Primeira tela do app para quem não está logado (`/acesso`, `page_type = publico`). |
| Página virtual | Troca de tela sem recarregar a página. Gera `page_view` com o `page_path` da rota. |
| Elemento (`link_id`) | Código fixo de cada botão ou link, no atributo `data-click`. Lista em `catalogs.elements`. |
| Banner interno | Peça de campanha dentro do app, identificada por `promotion_id`. Catálogo em `catalogs.banners`. |
| Posição (`creative_slot`) | Lugar do banner na tela: `acesso_destaque_1`, `inicio_oferta_2`, `cartoes_oferta_1` e assim por diante. |
| Pix | Transferência instantânea. O funil tem três etapas: dados, revisão e comprovante. |
| Chave Pix | Identificador de quem recebe (e-mail, celular, CPF, CNPJ ou aleatória). Nunca entra no dataLayer; só o tipo vai em `pix_key_type`. |
| CDI | Taxa de referência da renda fixa. "104% do CDI" é a rentabilidade do CDB Liquidez Diária. |
| Segmento (`customer_segment`) | Classificação comercial do cliente. No teste, sempre `pf_alta_renda`. |
| Lead | Pedido de produto (`generate_lead`): abertura de conta ou cartão. O tipo vai em `lead_source`. |

## Funis

| Funil | Etapas, em ordem | Observação |
| --- | --- | --- |
| Login | `form_start` (form_id=login) → `form_submit` (step=aprovado) → `login` | Cada recusa é `form_submit` com `step=recusado` e `error_type`. Quem chegou ao login vindo de uma tela logada tem um `click` antes, com `link_url` da tela pedida. |
| Pix | `form_start` (form_id=pix) → `form_submit` (step=revisao) → `form_submit` (step=confirmado) | `step=recusado` são as recusas da validação; `click` com `link_id=pix_corrigir` é a volta da revisão. Só `step=confirmado` conta como Pix concluído. |
| Banner | `view_promotion` → `select_promotion` → evento da ação | A ação pode ser `generate_lead` ou o `page_view` da tela de destino. Use o mesmo `promotion_id` em todas as etapas. |

## Métricas

| Métrica | Como calcular |
| --- | --- |
| Taxa de toque de banner | `select_promotion` ÷ `view_promotion`, por `promotion_id` e `creative_slot` |
| Conversão do login | clientes com `login` ÷ clientes com `form_start` (form_id=login) |
| Taxa de erro do login | `form_submit` (form_id=login, step=recusado) ÷ todos os `form_submit` de login, por `error_type` |
| Conversão do Pix | `form_submit` (form_id=pix, step=confirmado) ÷ `form_start` (form_id=pix) |
| Valor de Pix pelo app | soma de `value` em `form_submit` com form_id=pix e step=confirmado (moeda em `currency`) |
| Uso de botões | contagem de `click` por `link_id` e `page_path` |
| Demanda por atalhos sem fluxo | contagem de `click` dos `link_id` marcados "Sem fluxo" em `catalogs.elements` |

## Regras que valem para todos os eventos

- `click` sai primeiro, na fase de captura. O evento de negócio do mesmo toque (`select_promotion`, `form_submit`, `login`, `generate_lead`, `select_item`) vem logo depois. Não some os dois como se fossem dois toques.
- `click` do app tem sempre `outbound=false`. O click automático do GA4 para links externos vem com `outbound=true`.
- As teclas numéricas da senha não geram `click`: nenhum dígito é enviado.
- `user_id` só existe depois do `login`. Em `page_view` deslogado ele vai como `undefined`, para limpar o valor anterior no GTM.
- Parâmetros que não se aplicam a um `form_submit` (ex.: `value` no login) vão como `undefined`.
- Nenhum evento carrega senha, agência, conta, saldo, valor de fatura ou chave Pix.
- IDs são sempre texto. Valores em dinheiro são número com ponto decimal.
- `view_promotion` mede exposição real (60% do banner visível), uma vez por banner a cada `page_view`.
- O Pix confirmado não é `purchase`: Pix não é receita do banco, e `purchase` inflaria a receita no GA4.

## Perguntas que a IA não deve responder com estes dados

- Quem é o cliente. O `user_id` é pseudonimizado de propósito.
- Saldo, fatura ou patrimônio do cliente. Esses valores não são coletados.
- Se um Pix chegou ao destino. `form_submit` com step=confirmado registra o envio pelo app; a liquidação está no core bancário, ligada por `transaction_id`.
