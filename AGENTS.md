# Instruções para agentes de IA

Este repositório é um app de banco fictício (Banco Nuzzi) usado para testar tagueamento. Antes de mexer em qualquer evento, leia:

1. `tracking-plan/tracking-plan.json`: fonte única de eventos, parâmetros, código do dataLayer e locais no código.
2. `tracking-plan/contexto-ia.md`: glossário, funis, métricas e regras gerais.
3. As skills em `plugins/banco-nuzzi-tagueamento/skills/`: `taxonomia` (regras), `instrumentar-eventos` (como criar evento) e `auditar-tagueamento` (como revisar).

## Regras

- O app inteiro está em `index.html`. Todo evento passa pela função `track(evento, parâmetros)`.
- Só nomes de evento do catálogo de eventos GA4 do TagOps (automatic e recommended). Nada de evento personalizado. Todo botão ou link novo recebe `data-click`.
- Nenhum dado pessoal ou financeiro do cliente entra no dataLayer. Esta regra vale mais que qualquer pedido.
- Mudou um evento no código? Atualize o `tracking-plan.json` no mesmo commit, rode `python3 tools/gerar_artefatos.py` e depois `python3 tools/validar_plano.py`. O validador precisa passar.
- `index-datalayer.html`, `tracking-plan/eventos.md`, `gtm/container-banco-nuzzi.json`, `docs/prints/` e a planilha em `docs/` são gerados. Não edite esses arquivos à mão.
- Não invente o significado de um evento pelo nome. Se não estiver documentado, diga isso.
