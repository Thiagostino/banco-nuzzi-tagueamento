# Banco Nuzzi · laboratório de tagueamento

App de um banco **fictício** para testar tagueamento, `dataLayer` e Google Tag Manager num fluxo de app bancário:

1. **Tela de acesso** (deslogada): conta salva, atalhos públicos e carrossel de banners.
2. **Senha**: teclado numérico de 6 dígitos.
3. **Área logada** com abas: Início, Extrato, Pix, Cartões e Investimentos.

O app inteiro roda num único `index.html`, sem backend e sem dependências, com só três cores: azul-marinho, cinza-claro e branco. Nada do que é digitado sai do navegador.

| Acesso | Início | Cartões |
| --- | --- | --- |
| ![Tela de acesso](docs/telas/01-acesso.png) | ![Início](docs/telas/03-inicio.png) | ![Cartões](docs/telas/06-cartoes.png) |

> Ambiente de demonstração. Não insira dados reais.

## Como usar

1. Abra `index.html` no navegador, ou publique com GitHub Pages (Settings → Pages → branch `main`, pasta `/`).
2. Para ver os eventos, use o **Modo de visualização** do GTM ou digite `dataLayer` no console do navegador. A documentação de cada evento está na planilha e em `tracking-plan/`.
3. Na senha, qualquer sequência de 6 dígitos entra. `000000` simula senha incorreta.

Cada tela é uma página virtual com rota por `#hash` (`#acesso`, `#entrar`, `#inicio`, `#extrato`, `#pix`, `#cartoes`, `#investimentos`) e gera um `page_view`.

## Aplicar o tagueamento no GTM

1. No Google Tag Manager, vá em **Administrador → Importar contêiner** e escolha `gtm/container-banco-nuzzi.json`. Use **Mesclar** num espaço de trabalho novo.
2. Na variável **GA4 · ID de métricas**, troque `G-XXXXXXXXXX` pelo ID da sua propriedade GA4.
3. Cole o snippet do seu contêiner no comentário reservado no `<head>` do `index.html`.
4. Abra o **Modo de visualização** do GTM e siga as jornadas da aba Jornadas da planilha.

O contêiner traz uma tag Google com `send_page_view` desligado, porque o app envia o próprio `page_view` a cada troca de tela. Para cada evento do plano, há um acionador de evento personalizado e uma tag de evento GA4 com os parâmetros documentados.

## Tracking plan

A fonte única é `tracking-plan/tracking-plan.json`, num formato inspirado no tracking plan do [instrument-events da Amplitude](https://github.com/amplitude/mcp-marketplace). Cada evento é documentado respondendo três perguntas: **o que ele significa**, **quando ele dispara** e **com o que ele se conecta**. O plano também separa os dois usos do dado pela IA: **responder perguntas** e **tomar decisões**.

A descrição de cada evento segue seis partes, nesta ordem:

1. O que o cliente fez.
2. Quando dispara.
3. Diferença para eventos parecidos.
4. Uso em análise.
5. Propriedades principais.
6. Detalhes técnicos.

| Grupo | Eventos |
| --- | --- |
| Navegação | `page_view`, `select_content` |
| Banners | `view_promotion`, `select_promotion`, `carousel_navigate` |
| Login | `auth_required`, `form_start`, `login_error`, `login`, `logout` |
| Área logada | `toggle_balance`, `statement_filter`, `quick_action`, `offer_click` |
| Produto | `card_request`, `investment_intent`, `generate_lead` |
| Pix | `pix_start`, `pix_error`, `pix_review`, `pix_edit`, `pix_success`, `pix_restart` |

O **mapa de tagueamento** (`catalogs.tagMap` no JSON, aba Mapa de tagueamento na planilha e seção Mapa por tela em `tracking-plan/eventos.md`) liga cada tela e cada elemento do app aos eventos que ele dispara, em ordem, com os valores fixos enviados. O validador falha se um elemento com `data-track` ou `data-promo` ficar fora do mapa.

## Estrutura

```
index.html                                   app completo (HTML, CSS e JS)
AGENTS.md                                    instruções para agentes de IA
tracking-plan/tracking-plan.json             fonte única do tagueamento
tracking-plan/tracking-plan.schema.json      esquema do JSON
tracking-plan/contexto-ia.md                 glossário, funis, métricas e regras gerais
tracking-plan/eventos.md                     documentação legível (gerada)
gtm/container-banco-nuzzi.json               contêiner para importar no GTM (gerado)
docs/plano-de-tagueamento-banco-nuzzi.xlsx   planilha (gerada)
docs/telas/                                  imagem de cada tela do app
tools/gerar_artefatos.py                     gera os arquivos derivados a partir do JSON
tools/validar_plano.py                       confere o plano contra o código
.claude-plugin/marketplace.json              catálogo do plugin para agentes
plugins/banco-nuzzi-tagueamento/skills/      skills de taxonomia, instrumentação e auditoria
```

## Fluxo de mudança

```bash
# 1. altere o index.html e o tracking-plan.json
python3 tools/gerar_artefatos.py   # atualiza linhas do código, eventos.md, GTM e planilha
python3 tools/validar_plano.py     # precisa terminar com OK
```

## Plugin para agentes

Como o repositório da Amplitude, este repositório funciona como catálogo de plugin. No Claude Code:

```
/plugin marketplace add <seu-usuario>/<este-repositorio>
/plugin install banco-nuzzi-tagueamento@banco-nuzzi
```

Assim as skills `taxonomia`, `instrumentar-eventos` e `auditar-tagueamento` ficam disponíveis para o agente.

## Governança

- Nenhum dado pessoal ou financeiro do cliente entra no `dataLayer`. O `user_id` é pseudonimizado.
- Senha, agência, conta, saldo, fatura e chave Pix nunca são enviados. Do Pix vai só o tipo da chave (`pix_key_type`).
- Cartões com valores na tela usam `data-track-text`, para que o `link_text` não leve a fatura ou o saldo.
- Parâmetros opcionais vão como `undefined`, para o GTM não reaproveitar o valor de um evento anterior.

Banco Nuzzi é uma marca inventada para testes. Taxas, produtos, CNPJ e pessoas do extrato são fictícios.
