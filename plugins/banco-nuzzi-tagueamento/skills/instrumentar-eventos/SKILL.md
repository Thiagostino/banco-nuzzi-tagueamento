---
name: instrumentar-eventos
description: >
  Planeja e implementa eventos novos no dataLayer do app Banco Nuzzi. Use quando uma tela,
  botão ou fluxo novo precisar de medição, ou quando alguém pedir para "taguear" uma mudança.
  Produz a entrada no tracking plan, o código do dataLayer e atualiza o GTM.
---

# Instrumentar eventos no Banco Nuzzi

Siga a skill `taxonomia` para nomes, tipos e regras de dado pessoal. Esta skill diz como transformar uma mudança no app em evento documentado e implementado.

## 1. Decida se precisa de evento novo

- O gesto já é coberto por um evento existente? Um toque em link novo é `select_content` com `data-track`; um banner novo é `view_promotion` e `select_promotion` com `data-promo`. Nesses casos não crie evento, só adicione o atributo e a linha no catálogo.
- Crie evento só para uma ação de negócio que entra num funil ou numa métrica. Se você não consegue dizer em uma frase qual pergunta ele responde, não crie.

## 2. Siga o padrão do código

- A função de envio é `track(evento, parâmetros)`, dentro do `index.html`. Ela empurra o objeto em `window.dataLayer`.
- Chame `track` no ponto exato do gesto, depois da validação e antes da troca de tela.
- Use só variáveis disponíveis nesse ponto. Se um dado útil está em outro lugar, anote no plano em vez de reestruturar o código.

## 3. Escolha os parâmetros

De dois a quatro parâmetros por evento. Cada um precisa responder "qual filtro ou eixo de gráfico ele permite?". Não repita o que outro evento da sessão já informa (o `user_id` vem do `login` e do `page_view`).

## 4. Registre no tracking plan

Adicione um objeto em `trackingPlan` do `tracking-plan/tracking-plan.json`, no mesmo formato dos outros:

```json
{
  "id": "EV-24",
  "eventName": "nome_do_evento",
  "category": "Área logada",
  "status": "Em homologação",
  "owner": "Time responsável",
  "description": {
    "behavior": "O que o cliente fez, em linguagem de negócio.",
    "trigger": "Condição exata do disparo.",
    "disambiguation": "Diferença para eventos parecidos.",
    "useCases": "Funil ou métrica em que entra.",
    "keyProperties": "param_a, param_b",
    "technical": "seletor em /tela"
  },
  "aiDescription": "As seis partes acima num texto só, na mesma ordem.",
  "aiUses": { "answerQuestions": "Pergunta de exemplo.", "makeDecisions": "Decisão de exemplo." },
  "connectsTo": "Entidades ligadas ao evento.",
  "eventProperties": [
    { "name": "param_a", "type": "string", "required": "Sim", "description": "...", "possibleValues": "...", "example": "...", "source": "...", "lgpd": "Não pessoal" }
  ],
  "dataLayerPush": "// Quando: ...\nwindow.dataLayer.push({\n  event: 'nome_do_evento',\n  param_a: 'valor'\n});",
  "gtm": { "trigger": "CE · nome_do_evento", "tag": "GA4 · nome_do_evento", "triggerType": "Evento personalizado", "eventNameMatch": "nome_do_evento" },
  "implementationLocations": [ { "filePath": "index.html", "codeContext": "função ou listener onde a chamada fica" } ]
}
```

O `codeContext` é a âncora estável (nome da função ou do listener). A linha e o `trackingCode` são preenchidos pelo gerador.

## 5. Gere e valide

```bash
python3 tools/gerar_artefatos.py   # atualiza linhas do código, eventos.md, contêiner do GTM e planilha
python3 tools/validar_plano.py     # falha se código e plano divergirem
```

Não entregue a mudança com o validador falhando.

## 6. Apresente o plano

Para cada evento, diga o que ele mede, onde está no código e quais parâmetros envia e por quê. Separe o que está pronto para o GTM do que ainda depende de decisão (owner, nome, parâmetro em aberto). Pergunte se algo precisa mudar antes de publicar o contêiner.
