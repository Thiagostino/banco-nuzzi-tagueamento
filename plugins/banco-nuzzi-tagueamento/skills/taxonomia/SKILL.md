---
name: taxonomia
description: >
  Fonte de verdade da taxonomia de eventos do app Banco Nuzzi. Use quando um agente precisar
  ler, explicar, revisar ou propor eventos e parâmetros do dataLayer, responder perguntas de
  negócio com esses eventos, ou checar nomenclatura, descrições e regras de dado pessoal.
---

# Taxonomia do Banco Nuzzi

## Quando usar

- Alguém pergunta o que um evento significa, quando ele dispara ou como usar numa análise.
- Um agente vai escrever uma consulta, um painel ou uma resposta com os eventos do app.
- Alguém propõe um evento ou parâmetro novo e quer saber se ele segue o padrão.
- Uma revisão de tagueamento precisa de um critério para dizer o que está certo.

## Onde estão as respostas

Leia nesta ordem e não invente o que não estiver escrito:

1. `tracking-plan/tracking-plan.json`: fonte única. Um objeto por evento em `trackingPlan`, com descrição, parâmetros, código do dataLayer e locais no código. Catálogos de banners, telas, elementos e jornadas em `catalogs`.
2. `tracking-plan/contexto-ia.md`: glossário, funis, métricas e regras que valem para todos os eventos.
3. `tracking-plan/eventos.md`: a mesma informação do JSON em texto, gerada por `tools/gerar_artefatos.py`.

Se a resposta não estiver nesses arquivos, diga que não está documentada. Não deduza o significado de um evento pelo nome.

## Princípio da documentação

Cada evento responde três perguntas: o que ele significa, quando ele dispara e com o que ele se conecta. E separa os dois usos do dado pela IA:

- **Para responder perguntas**, a IA precisa do significado em linguagem de negócio (`description.behavior`) e da diferença para eventos parecidos (`description.disambiguation`).
- **Para tomar decisões**, a IA precisa do momento exato do disparo (`description.trigger`) e das entidades ligadas ao evento (`connectsTo`: cliente, banner, transação).

## Estrutura da descrição de um evento

Toda descrição segue esta ordem. O campo `aiDescription` junta as seis partes em um texto pronto para catálogos e ferramentas de IA.

| Ordem | Campo | O que escrever |
| --- | --- | --- |
| 1 | `behavior` | O que o cliente fez, sem termo técnico |
| 2 | `trigger` | Condição exata do disparo: gesto, tela, sucesso ou falha, o que vem antes e depois |
| 3 | `disambiguation` | Como ele se diferencia dos eventos de nome ou momento parecido |
| 4 | `useCases` | Em que funil ou métrica ele entra |
| 5 | `keyProperties` | Os parâmetros mais usados em análise |
| 6 | `technical` | Seletor e tela; o resto fica em `implementationLocations` |

Descrição ruim: "dispara no clique do botão". Descrição boa: "O cliente tocou no botão de um banner interno. Dispara antes da troca de tela e antes do evento da ação do botão."

## Nomenclatura

- Eventos em `snake_case`, em inglês, no padrão dos eventos recomendados do GA4 quando há equivalente (`page_view`, `view_promotion`, `select_promotion`, `login`, `generate_lead`). Esta é a convenção do projeto e vale mais que qualquer padrão externo.
- Um gesto do cliente gera um nome de evento. Variações vão em parâmetro (`card_tier`, `action_id`), não em eventos novos.
- Parâmetros em `snake_case`, com o mesmo nome para o mesmo conceito em todos os eventos (`page_path`, `promotion_id`, `user_id`).
- Nomes distintos para conceitos distintos: `filter` no extrato, `control` no carrossel, `state` no saldo.

## Tipos de parâmetro

| Tipo | Regra | Exemplo |
| --- | --- | --- |
| IDs | sempre texto | `"transaction_id": "E1792334211000"` |
| Valores | número com ponto decimal, moeda em `currency` | `"value": 150.00` |
| Listas fechadas | texto em `snake_case` | `"error_type": "senha_incorreta"` |
| Opcional sem valor | `undefined` no push, nunca `null` ou texto vazio | `user_id` em `page_view` deslogado |

## Dado pessoal (regra que bloqueia)

Nenhum evento pode carregar senha, agência, conta, saldo, valor de fatura, chave Pix ou qualquer dado que identifique o cliente. O `user_id` é pseudonimizado e só aparece depois do `login`. Se uma proposta violar esta regra, recuse a proposta e diga qual campo viola, mesmo que a pergunta seja sobre outra coisa.

## Status

| Status | Significado |
| --- | --- |
| Implementado | Está no código e no plano |
| Em homologação | Em teste no ciclo atual |
| Aprovado | Passou na homologação |
| Ajustar | Funciona, mas tem um problema documentado em `description.disambiguation` ou nos pontos de atenção |
| Descontinuado | Não deve ser usado em análises novas |
