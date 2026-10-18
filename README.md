# Banco Nuzzi · laboratório de tagueamento

Site de um banco **fictício** para testar tagueamento, `dataLayer` e Google Tag Manager num cenário de internet banking: home com banners internos, páginas de produto, login de demonstração, área logada e um fluxo de Pix em três etapas.

Tudo roda num único `index.html`, sem backend e sem dependências. Nada do que é digitado sai do navegador.

> Ambiente de demonstração. Não insira dados reais.

## Como usar

1. Abra `index.html` no navegador, ou publique com GitHub Pages (Settings → Pages → branch `main`, pasta `/`).
2. Clique em **dataLayer**, no canto inferior direito, para ver os eventos ao vivo e copiar o JSON.
3. Para entrar na área logada, a conta já vem preenchida. Use qualquer senha de 6 dígitos, por exemplo `123456`.
4. Para testar com o GTM, cole o snippet do seu contêiner no comentário reservado no `<head>` do `index.html`.

A navegação é por `#hash` (`#inicio`, `#cartoes`, `#investimentos`, `#entrar`, `#conta`, `#pix`). Cada troca de tela gera um `page_view` virtual.

## Plano de tagueamento

O plano completo está em [`docs/plano-de-tagueamento-banco-nuzzi.xlsx`](docs/plano-de-tagueamento-banco-nuzzi.xlsx), com as abas Eventos, Parâmetros, Banners, Telas, Jornadas e Elementos.

Cada evento é documentado respondendo três perguntas: **o que ele significa**, **quando ele dispara** e **com o que ele se conecta**. O plano também separa os dois usos do dado pela IA, para responder perguntas e para tomar decisões.

| Grupo | Eventos |
| --- | --- |
| Navegação | `page_view`, `select_content`, `menu_toggle` |
| Banners | `view_promotion`, `select_promotion`, `carousel_navigate` |
| Login | `auth_required`, `form_start`, `login_error`, `login`, `logout` |
| Área logada | `toggle_balance`, `quick_action`, `offer_click` |
| Produto | `card_request`, `investment_intent`, `generate_lead` |
| Pix | `pix_start`, `pix_error`, `pix_review`, `pix_edit`, `pix_success`, `pix_restart` |

## Governança

- Nenhum dado pessoal entra no `dataLayer`. O `user_id` é pseudonimizado.
- Senha, agência, conta, saldo e chave Pix nunca são enviados. Do Pix vai só o tipo da chave (`pix_key_type`).
- `view_promotion` só dispara com 50% do banner visível, uma vez por banner a cada `page_view`.

## Estrutura

```
index.html                               site completo (HTML, CSS e JS)
docs/plano-de-tagueamento-banco-nuzzi.xlsx  plano de tagueamento
```

Banco Nuzzi é uma marca inventada para testes. Taxas, produtos, CNPJ e pessoas do extrato são fictícios.
