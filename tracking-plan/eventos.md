# Eventos do Banco Nuzzi

Versão 2.0.0 · atualizado em 2026-10-18 · gerado de `tracking-plan.json` por `tools/gerar_artefatos.py`.

Cada evento responde o que ele significa, quando ele dispara e com o que ele se conecta, e separa os dois usos do dado pela IA: responder perguntas e tomar decisões.

App fictício de banco para testar dataLayer e GTM. Todo botão e link gera click; quando o toque conclui uma ação, o evento de negócio sai em seguida. Todos os nomes de evento seguem o catálogo de eventos GA4 do TagOps (automatic e recommended); nenhum evento é personalizado. Erros de validação são form_submit com step=recusado.

| Evento | Catálogo GA4 (TagOps) | Categoria | Quando dispara | Status |
| --- | --- | --- | --- | --- |
| [`page_view`](#page_view) | GA4 automático | Navegação | Ao abrir o app e a cada troca de #hash, depois da checagem de login. | Implementado |
| [`click`](#click) | GA4 automático | Navegação | No toque em qualquer elemento com data-click, na fase de captura do clique: sai antes de qualquer outro evento do mesmo toque (page_view, login, generate_lead, select_promotion, form_submit). | Implementado |
| [`view_promotion`](#view_promotion) | GA4 recomendado | Banners | Quando ao menos 60% do banner fica visível (IntersectionObserver), inclusive ao arrastar o carrossel ou tocar num indicador. | Implementado |
| [`select_promotion`](#select_promotion) | GA4 recomendado | Banners | No toque em .promo-cta dentro de [data-promo], logo depois do click do mesmo botão. | Implementado |
| [`form_start`](#form_start) | GA4 automático | Formulários | No primeiro gesto de preenchimento do formulário, uma vez por abertura da tela. | Implementado |
| [`login`](#login) | GA4 recomendado | Login | No toque em Entrar com 6 dígitos aceitos, logo depois do click btn_entrar e antes de ir para o destino guardado (ou /inicio). | Implementado |
| [`form_submit`](#form_submit) | GA4 automático | Formulários | No toque no botão que envia o formulário (Entrar, Continuar ou Confirmar Pix), logo depois do click do mesmo botão. | Implementado |
| [`generate_lead`](#generate_lead) | GA4 recomendado | Produto | No toque em 'Abrir conta' ou 'Quero abrir' na tela de acesso (abertura_conta) e em 'Pedir o Black' (cartao_black) ou 'Pedir adicional' (cartao_adicional) na tela Cartões. | Implementado |
| [`select_item`](#select_item) | GA4 recomendado | Produto | No toque em Investir num produto da tela Investimentos, logo depois do click do mesmo botão. | Implementado |

## Migração da versão 1 (23 eventos) para a 2 (9 eventos)

| Evento removido | Agora é | Como identificar |
| --- | --- | --- |
| `select_content` | `click` | link_id substitui item_id; element_type substitui content_type |
| `carousel_navigate` | `click (indicadores)` | Arrastar deixou de gerar evento: a exposição do banner novo já é view_promotion |
| `quick_action` | `click` | link_id do atalho (ajuda, atalho_pagar, cartoes_bloquear...) |
| `toggle_balance` | `click` | link_id=ocultar_saldo; link_text diz a ação |
| `statement_filter` | `click` | link_id=filtro_todos, filtro_entradas ou filtro_saidas |
| `logout` | `click` | link_id=sair; o GA4 limpa o user_id logo depois |
| `pix_edit` | `click` | link_id=pix_corrigir |
| `pix_restart` | `click` | link_id=pix_novo |
| `offer_click` | `select_promotion` | O toque no banner já é select_promotion; o click diz qual botão |
| `card_request` | `generate_lead` | lead_source=cartao_black ou cartao_adicional |
| `investment_intent` | `select_item` | items[0].item_id = produto |
| `pix_start` | `form_start` | form_id=pix |
| `pix_review` | `form_submit` | form_id=pix, step=revisao |
| `pix_success` | `form_submit` | form_id=pix, step=confirmado. Não virou purchase: Pix não é receita |
| `pix_error` | `form_submit` | form_id=pix, step=recusado, error_type |
| `login_error` | `form_submit` | form_id=login, step=recusado, error_type |
| `auth_required` | `click + page_view` | o click do botão traz link_url com a tela pedida; o page_view seguinte é /entrar |

## Mapa por tela

Cada elemento do app e os eventos que ele dispara, em ordem. Imagens das telas em `docs/telas/`.


### /acesso

![/acesso](../docs/telas/01-acesso.png)

| ID | Área | Elemento | Seletor | Gesto | Eventos | Valores fixos | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EL-01 | Tela inteira | Tela de acesso | `[data-page=acesso]` | Abrir o app deslogado | page_view | page_path=/acesso · page_type=publico · login_status=logged_out | [ver](../docs/prints/EL-01.jpg) |
| EL-02 | Topo | Ícone de ajuda (?) | `[data-click=ajuda]` | Toque | click | link_id=ajuda · element_type=icon · page_path=/acesso | [ver](../docs/prints/EL-02.jpg) |
| EL-03 | Conta salva | Link Trocar | `[data-click=trocar_conta]` | Toque | click | link_id=trocar_conta · element_type=link · page_path=/acesso | [ver](../docs/prints/EL-03.jpg) |
| EL-04 | Botão principal | Acessar minha conta | `[data-click=acesso_entrar]` | Toque | click → page_view | link_id=acesso_entrar · element_type=cta · link_url=/entrar · depois page_path=/entrar | [ver](../docs/prints/EL-04.jpg) |
| EL-05 | Atalhos | Pix | `[data-click=acesso_pix]` | Toque | click → page_view | link_id=acesso_pix · element_type=shortcut · link_url=/pix · depois page_path=/entrar | [ver](../docs/prints/EL-05.jpg) |
| EL-06 | Atalhos | Token | `[data-click=acesso_token]` | Toque | click | link_id=acesso_token · element_type=shortcut · page_path=/acesso | [ver](../docs/prints/EL-06.jpg) |
| EL-07 | Atalhos | Bloquear cartão | `[data-click=acesso_bloquear_cartao]` | Toque | click | link_id=acesso_bloquear_cartao · element_type=shortcut · page_path=/acesso | [ver](../docs/prints/EL-07.jpg) |
| EL-08 | Atalhos | Abrir conta | `[data-click=acesso_abrir_conta]` | Toque | click → generate_lead | link_id=acesso_abrir_conta · element_type=shortcut · lead_source=abertura_conta | [ver](../docs/prints/EL-08.jpg) |
| EL-09 | Carrossel Para você | Indicadores (bolinhas) | `[data-carousel=acesso_destaques] .dot` | Toque | click → view_promotion | element_type=carousel_indicator · page_path=/acesso | [ver](../docs/prints/EL-09.jpg) |
| EL-10 | Carrossel Para você | Banner Abra sua conta | `[data-promo=bnr_abra_conta]` | Aparecer 60% na tela | view_promotion | promotion_id=bnr_abra_conta · creative_slot=acesso_destaque_1 | [ver](../docs/prints/EL-10.jpg) |
| EL-11 | Carrossel Para você | Botão Quero abrir | `[data-click=bnr_abra_conta_cta]` | Toque | click → select_promotion → generate_lead | link_id=bnr_abra_conta_cta · element_type=banner_cta · promotion_id=bnr_abra_conta · lead_source=abertura_conta | [ver](../docs/prints/EL-11.jpg) |
| EL-12 | Carrossel Para você | Banner Nuzzi Black | `[data-promo=bnr_cartao_black]` | Aparecer 60% na tela | view_promotion | promotion_id=bnr_cartao_black · creative_slot=acesso_destaque_2 | [ver](../docs/prints/EL-12.jpg) |
| EL-13 | Carrossel Para você | Botão Conhecer o Black | `[data-click=bnr_cartao_black_cta]` | Toque | click → select_promotion → page_view | link_id=bnr_cartao_black_cta · element_type=banner_cta · promotion_id=bnr_cartao_black · depois page_path=/entrar | [ver](../docs/prints/EL-13.jpg) |
| EL-14 | Carrossel Para você | Banner CDB 104% do CDI | `[data-promo=bnr_cdb_liquidez]` | Aparecer 60% na tela | view_promotion | promotion_id=bnr_cdb_liquidez · creative_slot=acesso_destaque_3 | [ver](../docs/prints/EL-14.jpg) |
| EL-15 | Carrossel Para você | Botão Ver investimentos | `[data-click=bnr_cdb_liquidez_cta]` | Toque | click → select_promotion → page_view | link_id=bnr_cdb_liquidez_cta · element_type=banner_cta · promotion_id=bnr_cdb_liquidez · depois page_path=/entrar | [ver](../docs/prints/EL-15.jpg) |

### /entrar

![/entrar](../docs/telas/02-senha.png)

| ID | Área | Elemento | Seletor | Gesto | Eventos | Valores fixos | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EL-16 | Tela inteira | Tela de senha | `[data-page=entrar]` | Abrir | page_view | page_path=/entrar · page_type=login | [ver](../docs/prints/EL-16.jpg) |
| EL-17 | Topo | Seta Voltar | `[data-click=senha_voltar]` | Toque | click → page_view | link_id=senha_voltar · element_type=cta · link_text=Voltar · depois page_path=/acesso | [ver](../docs/prints/EL-17.jpg) |
| EL-18 | Teclado | Teclas de 0 a 9 | `#keypad [data-key]` | Primeiro dígito | form_start | form_id=login · page_path=/entrar | [ver](../docs/prints/EL-18.jpg) |
| EL-19 | Teclado | Esqueci | `[data-click=esqueci_senha]` | Toque | click | link_id=esqueci_senha · element_type=link · page_path=/entrar | [ver](../docs/prints/EL-19.jpg) |
| EL-20 | Botão | Entrar com menos de 6 dígitos | `[data-click=btn_entrar]` | Toque | click → form_submit | link_id=btn_entrar · element_type=cta · form_id=login · step=recusado · error_type=senha_incompleta | [ver](../docs/prints/EL-20.jpg) |
| EL-21 | Botão | Entrar com 000000 | `[data-click=btn_entrar]` | Toque | click → form_submit | link_id=btn_entrar · element_type=cta · form_id=login · step=recusado · error_type=senha_incorreta | [ver](../docs/prints/EL-21.jpg) |
| EL-22 | Botão | Entrar com 6 dígitos | `[data-click=btn_entrar]` | Toque | click → form_submit → login → page_view | link_id=btn_entrar · element_type=cta · form_id=login · step=aprovado · method=senha_eletronica · user_id=u_8f2c41a9 · depois page_path do destino | [ver](../docs/prints/EL-22.jpg) |

### /inicio

![/inicio](../docs/telas/03-inicio.png)

| ID | Área | Elemento | Seletor | Gesto | Eventos | Valores fixos | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EL-23 | Tela inteira | Início | `[data-page=inicio]` | Abrir | page_view | page_path=/inicio · page_type=area_logada · user_id | [ver](../docs/prints/EL-23.jpg) |
| EL-24 | Topo | Ícone de olho | `[data-click=ocultar_saldo]` | Toque | click | link_id=ocultar_saldo · element_type=icon · page_path=/inicio | [ver](../docs/prints/EL-24.jpg) |
| EL-25 | Topo | Sino de notificações | `[data-click=notificacoes]` | Toque | click | link_id=notificacoes · element_type=icon · page_path=/inicio | [ver](../docs/prints/EL-25.jpg) |
| EL-26 | Topo | Ícone Sair | `[data-click=sair]` | Toque | click → page_view | link_id=sair · element_type=icon · depois page_path=/acesso · login_status=logged_out | [ver](../docs/prints/EL-26.jpg) |
| EL-27 | Saldo | Ver extrato | `[data-click=inicio_ver_extrato]` | Toque | click → page_view | link_id=inicio_ver_extrato · element_type=cta · link_url=/extrato · depois page_path=/extrato | [ver](../docs/prints/EL-27.jpg) |
| EL-28 | Atalhos | Pix | `[data-click=atalho_pix]` | Toque | click → page_view | link_id=atalho_pix · element_type=shortcut · link_url=/pix · depois page_path=/pix | [ver](../docs/prints/EL-28.jpg) |
| EL-29 | Atalhos | Pagar | `[data-click=atalho_pagar]` | Toque | click | link_id=atalho_pagar · element_type=shortcut · page_path=/inicio | [ver](../docs/prints/EL-29.jpg) |
| EL-30 | Atalhos | Transferir | `[data-click=atalho_transferir]` | Toque | click | link_id=atalho_transferir · element_type=shortcut · page_path=/inicio | [ver](../docs/prints/EL-30.jpg) |
| EL-31 | Atalhos | Recarga | `[data-click=atalho_recarga]` | Toque | click | link_id=atalho_recarga · element_type=shortcut · page_path=/inicio | [ver](../docs/prints/EL-31.jpg) |
| EL-32 | Atalhos | Cartões | `[data-click=atalho_cartoes]` | Toque | click → page_view | link_id=atalho_cartoes · element_type=shortcut · link_url=/cartoes · depois page_path=/cartoes | [ver](../docs/prints/EL-32.jpg) |
| EL-33 | Atalhos | Investir | `[data-click=atalho_investir]` | Toque | click → page_view | link_id=atalho_investir · element_type=shortcut · link_url=/investimentos · depois page_path=/investimentos | [ver](../docs/prints/EL-33.jpg) |
| EL-34 | Carrossel de ofertas | Indicadores (bolinhas) | `[data-carousel=inicio_ofertas] .dot` | Toque | click → view_promotion | element_type=carousel_indicator · page_path=/inicio | [ver](../docs/prints/EL-34.jpg) |
| EL-35 | Carrossel de ofertas | Banner Crédito pré-aprovado | `[data-promo=bnr_credito_preaprovado]` | Aparecer 60% na tela | view_promotion | promotion_id=bnr_credito_preaprovado · creative_slot=inicio_oferta_1 | [ver](../docs/prints/EL-35.jpg) |
| EL-36 | Carrossel de ofertas | Botão Simular parcelas | `[data-click=bnr_credito_preaprovado_cta]` | Toque | click → select_promotion | link_id=bnr_credito_preaprovado_cta · element_type=banner_cta · promotion_id=bnr_credito_preaprovado | [ver](../docs/prints/EL-36.jpg) |
| EL-37 | Carrossel de ofertas | Banner Seguro cartão | `[data-promo=bnr_seguro_cartao]` | Aparecer 60% na tela | view_promotion | promotion_id=bnr_seguro_cartao · creative_slot=inicio_oferta_2 | [ver](../docs/prints/EL-37.jpg) |
| EL-38 | Carrossel de ofertas | Botão Contratar seguro | `[data-click=bnr_seguro_cartao_cta]` | Toque | click → select_promotion | link_id=bnr_seguro_cartao_cta · element_type=banner_cta · promotion_id=bnr_seguro_cartao | [ver](../docs/prints/EL-38.jpg) |
| EL-39 | Carrossel de ofertas | Banner Pix agendado | `[data-promo=bnr_pix_agendado]` | Aparecer 60% na tela | view_promotion | promotion_id=bnr_pix_agendado · creative_slot=inicio_oferta_3 | [ver](../docs/prints/EL-39.jpg) |
| EL-40 | Carrossel de ofertas | Botão Agendar um Pix | `[data-click=bnr_pix_agendado_cta]` | Toque | click → select_promotion → page_view | link_id=bnr_pix_agendado_cta · element_type=banner_cta · promotion_id=bnr_pix_agendado · depois page_path=/pix | [ver](../docs/prints/EL-40.jpg) |
| EL-41 | Cartão da fatura | Cartão Nuzzi Mais (fatura) | `[data-click=inicio_card_fatura]` | Toque | click → page_view | link_id=inicio_card_fatura · element_type=card · link_text=Cartão Nuzzi Mais · depois page_path=/cartoes | [ver](../docs/prints/EL-41.jpg) |
| EL-42 | Últimos lançamentos | Ver tudo | `[data-click=inicio_extrato_completo]` | Toque | click → page_view | link_id=inicio_extrato_completo · element_type=cta · link_url=/extrato · depois page_path=/extrato | [ver](../docs/prints/EL-42.jpg) |
| EL-43 | Investimentos | Cartão de investimentos | `[data-click=inicio_card_investimentos]` | Toque | click → page_view | link_id=inicio_card_investimentos · element_type=card · link_text=Investimentos · depois page_path=/investimentos | [ver](../docs/prints/EL-43.jpg) |

### /extrato

![/extrato](../docs/telas/04-extrato.png)

| ID | Área | Elemento | Seletor | Gesto | Eventos | Valores fixos | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EL-44 | Tela inteira | Extrato | `[data-page=extrato]` | Abrir | page_view | page_path=/extrato | [ver](../docs/prints/EL-44.jpg) |
| EL-45 | Filtros | Filtro Tudo | `[data-click=filtro_todos]` | Toque | click | link_id=filtro_todos · element_type=chip · page_path=/extrato | [ver](../docs/prints/EL-45.jpg) |
| EL-46 | Filtros | Filtro Entradas | `[data-click=filtro_entradas]` | Toque | click | link_id=filtro_entradas · element_type=chip · page_path=/extrato | [ver](../docs/prints/EL-46.jpg) |
| EL-47 | Filtros | Filtro Saídas | `[data-click=filtro_saidas]` | Toque | click | link_id=filtro_saidas · element_type=chip · page_path=/extrato | [ver](../docs/prints/EL-47.jpg) |

### /pix

![/pix](../docs/telas/05-pix.png)

| ID | Área | Elemento | Seletor | Gesto | Eventos | Valores fixos | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EL-48 | Tela inteira | Pix | `[data-page=pix]` | Abrir | page_view | page_path=/pix | [ver](../docs/prints/EL-48.jpg) |
| EL-49 | Topo | Seta Voltar | `[data-click=pix_voltar]` | Toque | click → page_view | link_id=pix_voltar · element_type=cta · link_url=/inicio · depois page_path=/inicio | [ver](../docs/prints/EL-49.jpg) |
| EL-50 | Etapa 1 · Dados | Campos chave, valor e mensagem | `#pix-form` | Primeiro foco num campo | form_start | form_id=pix · page_path=/pix | [ver](../docs/prints/EL-50.jpg) |
| EL-51 | Etapa 1 · Dados | Botão Continuar com erro | `[data-click=pix_continuar]` | Toque | click → form_submit | link_id=pix_continuar · element_type=cta · form_id=pix · step=recusado · error_type=chave_vazia, valor_invalido ou saldo_insuficiente | [ver](../docs/prints/EL-51.jpg) |
| EL-52 | Etapa 1 · Dados | Botão Continuar válido | `[data-click=pix_continuar]` | Toque | click → form_submit | link_id=pix_continuar · element_type=cta · form_id=pix · step=revisao · value · currency=BRL · pix_key_type | [ver](../docs/prints/EL-52.jpg) |
| EL-53 | Etapa 2 · Revisão | Botão Confirmar Pix | `[data-click=pix_confirmar]` | Toque | click → form_submit | link_id=pix_confirmar · element_type=cta · form_id=pix · step=confirmado · transaction_id · value · currency=BRL · pix_key_type | [ver](../docs/prints/EL-53.jpg) |
| EL-54 | Etapa 2 · Revisão | Botão Corrigir dados | `[data-click=pix_corrigir]` | Toque | click | link_id=pix_corrigir · element_type=cta · page_path=/pix | [ver](../docs/prints/EL-54.jpg) |
| EL-55 | Etapa 3 · Comprovante | Voltar ao início | `[data-click=pix_comprovante_inicio]` | Toque | click → page_view | link_id=pix_comprovante_inicio · element_type=cta · link_url=/inicio · depois page_path=/inicio | [ver](../docs/prints/EL-55.jpg) |
| EL-56 | Etapa 3 · Comprovante | Fazer outro Pix | `[data-click=pix_novo]` | Toque | click | link_id=pix_novo · element_type=cta · page_path=/pix | [ver](../docs/prints/EL-56.jpg) |

### /cartoes

![/cartoes](../docs/telas/06-cartoes.png)

| ID | Área | Elemento | Seletor | Gesto | Eventos | Valores fixos | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EL-57 | Tela inteira | Cartões | `[data-page=cartoes]` | Abrir | page_view | page_path=/cartoes | [ver](../docs/prints/EL-57.jpg) |
| EL-58 | Ações do cartão | Cartão virtual | `[data-click=cartao_virtual]` | Toque | click | link_id=cartao_virtual · element_type=action · page_path=/cartoes | [ver](../docs/prints/EL-58.jpg) |
| EL-59 | Ações do cartão | Bloquear | `[data-click=cartoes_bloquear]` | Toque | click | link_id=cartoes_bloquear · element_type=action · page_path=/cartoes | [ver](../docs/prints/EL-59.jpg) |
| EL-60 | Ações do cartão | Ajustar limite | `[data-click=ajustar_limite]` | Toque | click | link_id=ajustar_limite · element_type=action · page_path=/cartoes | [ver](../docs/prints/EL-60.jpg) |
| EL-61 | Oferta | Banner Troque para o Nuzzi Black | `[data-promo=bnr_upgrade_black]` | Aparecer 60% na tela | view_promotion | promotion_id=bnr_upgrade_black · creative_slot=cartoes_oferta_1 | [ver](../docs/prints/EL-61.jpg) |
| EL-62 | Oferta | Botão Pedir o Black | `[data-click=bnr_upgrade_black_cta]` | Toque | click → select_promotion → generate_lead | link_id=bnr_upgrade_black_cta · element_type=banner_cta · promotion_id=bnr_upgrade_black · lead_source=cartao_black | [ver](../docs/prints/EL-62.jpg) |
| EL-63 | Cartão adicional | Botão Pedir adicional | `[data-click=cartao_adicional]` | Toque | click → generate_lead | link_id=cartao_adicional · element_type=cta · lead_source=cartao_adicional | [ver](../docs/prints/EL-63.jpg) |

### /investimentos

![/investimentos](../docs/telas/07-investimentos.png)

| ID | Área | Elemento | Seletor | Gesto | Eventos | Valores fixos | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EL-64 | Tela inteira | Investimentos | `[data-page=investimentos]` | Abrir | page_view | page_path=/investimentos | [ver](../docs/prints/EL-64.jpg) |
| EL-65 | Renda fixa | Investir · CDB Liquidez Diária | `[data-click=investir_cdb_liquidez]` | Toque | click → select_item | link_id=investir_cdb_liquidez · element_type=product · item_list_id=renda_fixa · items[0].item_id=cdb_liquidez | [ver](../docs/prints/EL-65.jpg) |
| EL-66 | Renda fixa | Investir · LCI 90 dias | `[data-click=investir_lci_90]` | Toque | click → select_item | link_id=investir_lci_90 · element_type=product · item_list_id=renda_fixa · items[0].item_id=lci_90 | [ver](../docs/prints/EL-66.jpg) |
| EL-67 | Renda fixa | Investir · CDB 2 anos | `[data-click=investir_cdb_ipca_2a]` | Toque | click → select_item | link_id=investir_cdb_ipca_2a · element_type=product · item_list_id=renda_fixa · items[0].item_id=cdb_ipca_2a | [ver](../docs/prints/EL-67.jpg) |
| EL-68 | Renda fixa | Investir · Fundo Nuzzi DI | `[data-click=investir_fundo_di]` | Toque | click → select_item | link_id=investir_fundo_di · element_type=product · item_list_id=renda_fixa · items[0].item_id=fundo_di | [ver](../docs/prints/EL-68.jpg) |

### Telas logadas

| ID | Área | Elemento | Seletor | Gesto | Eventos | Valores fixos | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EL-69 | Barra de abas | Início | `[data-click=tab_inicio]` | Toque | click → page_view | link_id=tab_inicio · element_type=tab_bar · link_url=/inicio · depois page_path=/inicio | [ver](../docs/prints/EL-69.jpg) |
| EL-70 | Barra de abas | Extrato | `[data-click=tab_extrato]` | Toque | click → page_view | link_id=tab_extrato · element_type=tab_bar · link_url=/extrato · depois page_path=/extrato | [ver](../docs/prints/EL-70.jpg) |
| EL-71 | Barra de abas | Pix | `[data-click=tab_pix]` | Toque | click → page_view | link_id=tab_pix · element_type=tab_bar · link_url=/pix · depois page_path=/pix | [ver](../docs/prints/EL-71.jpg) |
| EL-72 | Barra de abas | Cartões | `[data-click=tab_cartoes]` | Toque | click → page_view | link_id=tab_cartoes · element_type=tab_bar · link_url=/cartoes · depois page_path=/cartoes | [ver](../docs/prints/EL-72.jpg) |
| EL-73 | Barra de abas | Investir | `[data-click=tab_investir]` | Toque | click → page_view | link_id=tab_investir · element_type=tab_bar · link_url=/investimentos · depois page_path=/investimentos | [ver](../docs/prints/EL-73.jpg) |

## page_view

**Catálogo GA4 (TagOps).** GA4 automático.

**O que é.** O cliente passou a ver uma tela do app. Cada tela é uma página virtual (rota por #hash).

**Quando dispara.** Ao abrir o app e a cada troca de #hash, depois da checagem de login. Sem #hash, abre /acesso (deslogado) ou /inicio (logado). Se a tela exige login e o cliente está deslogado, dispara para /entrar, e não para a tela pedida.

**Diferença para eventos parecidos.** Registra a tela vista. O toque que levou até ela é click (e select_promotion, quando veio de um banner).

**Uso em análise.** Base de todos os funis por tela e denominador das taxas por tela.

**Com o que se conecta.** Cliente (user_id, quando logado) · Tela (page_path) · Estado de login

**Uso pela IA**

- Para responder perguntas: Quantos clientes logados abriram a tela de Pix nesta semana?
- Para tomar decisões: Escolher o conteúdo e as ofertas da tela conforme page_type e login_status.

**Código do dataLayer**

```js
// Quando: Ao abrir o app e a cada troca de #hash, depois da checagem de login.
window.dataLayer.push({
  event: 'page_view',
  page_path: '/inicio',
  page_title: 'Início',
  page_type: 'area_logada',
  login_status: 'logged_in',
  user_id: 'u_8f2c41a9'
});
```

| Parâmetro | Tipo | Obrigatório | Significado | Valores | LGPD |
| --- | --- | --- | --- | --- | --- |
| `page_path` | string | Sim | Tela vista, no formato /rota. | /acesso, /entrar, /inicio, /extrato, /pix, /cartoes, /investimentos | Não pessoal |
| `page_title` | string | Sim | Nome da tela para leitura humana. | Acesso, Senha, Início, Extrato, Pix, Cartões, Investimentos | Não pessoal |
| `page_type` | string | Sim | Tipo de tela, para agrupar análises. | publico, login, area_logada | Não pessoal |
| `login_status` | string | Sim | Se o cliente estava logado ao ver a tela. | logged_in, logged_out | Não pessoal |
| `user_id` | string | Só logado | Identificador pseudonimizado do cliente. Liga eventos ao mesmo cliente sem expor quem ele é. Deslogado, vai como undefined. | u_ + hash | Pseudonimizado |

**Onde está no código**

- `index.html`, linha 601, route(), depois de mostrar a tela: `track('page_view', { page_path: '/' + r, page_title: ROUTES[r].title, page_type: ROUTES[r].type, login_status: S.logged ? 'logged_in' : 'logged_out', user_id: S.logged ? S.user.id : undefined })`

**Elementos no app.** EL-01, EL-04, EL-05, EL-13, EL-15, EL-16, EL-17, EL-22, EL-23, EL-26, EL-27, EL-28, EL-32, EL-33, EL-40, EL-41, EL-42, EL-43, EL-44, EL-48, EL-49, EL-55, EL-57, EL-64, EL-69, EL-70, EL-71, EL-72, EL-73 (ver Mapa por tela).


**GTM.** Acionador `CE · page_view`, tag `GA4 · page_view`. Owner: Governança de Dados Digitais.

## click

**Catálogo GA4 (TagOps).** GA4 automático.

**O que é.** O cliente tocou num botão ou link do app. Todo elemento com data-click gera click, e o link_id diz qual foi.

**Quando dispara.** No toque em qualquer elemento com data-click, na fase de captura do clique: sai antes de qualquer outro evento do mesmo toque (page_view, login, generate_lead, select_promotion, form_submit). As teclas numéricas da senha não geram click.

**Diferença para eventos parecidos.** Todo toque em botão ou link. Quando o toque também conclui uma ação, o evento de negócio sai logo depois, no mesmo toque (login, generate_lead, select_item, form_submit, select_promotion). Não confundir com o click automático do GA4 para links externos: esse vem com outbound=true; os do app vêm com outbound=false.

**Uso em análise.** Uso de cada botão e link por tela (link_id × page_path), caminhos de navegação e demanda por atalhos ainda sem fluxo.

**Com o que se conecta.** Elemento (link_id, aba Elementos) · Tela de origem (page_path) · Destino (link_url)

**Uso pela IA**

- Para responder perguntas: Qual botão do Início é mais tocado depois do login?
- Para tomar decisões: Reordenar atalhos, abas e botões pelo uso e priorizar os fluxos dos atalhos que ainda não existem.

**Código do dataLayer**

```js
// Quando: No toque em qualquer elemento com data-click, na fase de captura do clique: sai antes de qualquer outro evento do mesmo toque (page_view, login, generate_lead, select_promotion, form_submit).
window.dataLayer.push({
  event: 'click',
  link_id: 'tab_extrato',
  link_text: 'Extrato',
  link_url: '/extrato',
  element_type: 'tab_bar',
  outbound: false,
  page_path: '/inicio'
});
```

| Parâmetro | Tipo | Obrigatório | Significado | Valores | LGPD |
| --- | --- | --- | --- | --- | --- |
| `link_id` | string | Sim | Código fixo do elemento tocado. | Ver aba Elementos | Não pessoal |
| `link_text` | string | Sim | Texto do elemento, até 60 caracteres. Vem de data-click-text, aria-label ou texto visível, nessa ordem. | Texto fixo do app | Não pessoal (texto fixo) |
| `link_url` | string | Não | Destino do link, no formato /rota. Botões sem link vão como undefined. | /acesso, /entrar, /inicio, /extrato, /pix, /cartoes, /investimentos | Não pessoal |
| `element_type` | string | Sim | Tipo de elemento tocado. | cta, link, shortcut, icon, tab_bar, card, banner_cta, carousel_indicator, chip, action, product | Não pessoal |
| `outbound` | boolean | Sim | Sempre false: clique interno do app. Separa estes eventos do click automático de link externo do GA4, que vem com outbound=true. | false | Não pessoal |
| `page_path` | string | Sim | Tela onde o toque ou o formulário aconteceu. | /acesso, /entrar, /inicio, /extrato, /pix, /cartoes, /investimentos | Não pessoal |

**Onde está no código**

- `index.html`, linha 669, listener global de clique na fase de captura, [data-click]: `track('click', { link_id: c.getAttribute('data-click'), link_text: (c.getAttribute('data-click-text') || c.getAttribute('aria-label') || c.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60), link_url: href && href.charAt(0) === '#' ? '/' + href.slice(1) : undefined, element_type: c.getAttribute('data-click-type'), outbound: false, page_path: '/' + S.route })`

**Elementos no app.** EL-02, EL-03, EL-04, EL-05, EL-06, EL-07, EL-08, EL-09, EL-11, EL-13, EL-15, EL-17, EL-19, EL-20, EL-21, EL-22, EL-24, EL-25, EL-26, EL-27, EL-28, EL-29, EL-30, EL-31, EL-32, EL-33, EL-34, EL-36, EL-38, EL-40, EL-41, EL-42, EL-43, EL-45, EL-46, EL-47, EL-49, EL-51, EL-52, EL-53, EL-54, EL-55, EL-56, EL-58, EL-59, EL-60, EL-62, EL-63, EL-65, EL-66, EL-67, EL-68, EL-69, EL-70, EL-71, EL-72, EL-73 (ver Mapa por tela).


**GTM.** Acionador `CE · click`, tag `GA4 · click`. Owner: Produto Digital.

## view_promotion

**Catálogo GA4 (TagOps).** GA4 recomendado.

**O que é.** Um banner interno apareceu de fato na tela do cliente. Mede exposição, não carregamento.

**Quando dispara.** Quando ao menos 60% do banner fica visível (IntersectionObserver), inclusive ao arrastar o carrossel ou tocar num indicador. Uma vez por banner a cada page_view.

**Diferença para eventos parecidos.** Exposição do banner, não toque (select_promotion). Não conta carregamento da página: o banner precisa aparecer na tela.

**Uso em análise.** Denominador da taxa de toque de banner (CTR) por promotion_id e creative_slot.

**Com o que se conecta.** Banner (promotion_id, catálogo na aba Banners) · Posição (creative_slot) · Tela (location_id)

**Uso pela IA**

- Para responder perguntas: Qual banner da tela de acesso foi mais visto ontem, e em qual posição?
- Para tomar decisões: Decidir qual banner mostrar primeiro, usando select_promotion como resultado.

**Código do dataLayer**

```js
// Quando: Quando ao menos 60% do banner fica visível (IntersectionObserver), inclusive ao arrastar o carrossel ou tocar num indicador.
window.dataLayer.push({
  event: 'view_promotion',
  promotion_id: 'bnr_credito_preaprovado',
  promotion_name: 'Crédito pessoal pré-aprovado',
  creative_slot: 'inicio_oferta_1',
  location_id: '/inicio'
});
```

| Parâmetro | Tipo | Obrigatório | Significado | Valores | LGPD |
| --- | --- | --- | --- | --- | --- |
| `promotion_id` | string | Sim | Código do banner no catálogo de campanhas. | Ver aba Banners | Não pessoal |
| `promotion_name` | string | Sim | Nome do banner para leitura humana. | Ver aba Banners | Não pessoal |
| `creative_slot` | string | Sim | Posição do banner na tela. | Ver aba Banners | Não pessoal |
| `location_id` | string | Sim | Tela onde o banner estava. | /acesso, /inicio, /cartoes | Não pessoal |

**Onde está no código**

- `index.html`, linha 620, impression(), chamada pelo IntersectionObserver: `track('view_promotion', promoData(el))`

**Elementos no app.** EL-09, EL-10, EL-12, EL-14, EL-34, EL-35, EL-37, EL-39, EL-61 (ver Mapa por tela).


**GTM.** Acionador `CE · view_promotion`, tag `GA4 · view_promotion`. Owner: Marketing Digital.

## select_promotion

**Catálogo GA4 (TagOps).** GA4 recomendado.

**O que é.** O cliente tocou no botão de um banner interno.

**Quando dispara.** No toque em .promo-cta dentro de [data-promo], logo depois do click do mesmo botão. Sai antes da troca de tela e antes de generate_lead, quando o botão também gera lead.

**Diferença para eventos parecidos.** Só botões dentro de um banner [data-promo], sempre depois do click do mesmo botão. Use select_promotion para a taxa de toque do banner; o click é o mesmo toque visto como elemento.

**Uso em análise.** Numerador do CTR de banner e início dos funis de campanha.

**Com o que se conecta.** Banner (promotion_id) · Posição (creative_slot) · Tela (location_id) · Elemento (via click)

**Uso pela IA**

- Para responder perguntas: Qual a taxa de toque do banner de crédito pré-aprovado?
- Para tomar decisões: Pausar ou trocar banner com taxa de toque baixa.

**Código do dataLayer**

```js
// Quando: No toque em .promo-cta dentro de [data-promo], logo depois do click do mesmo botão.
window.dataLayer.push({
  event: 'select_promotion',
  promotion_id: 'bnr_credito_preaprovado',
  promotion_name: 'Crédito pessoal pré-aprovado',
  creative_slot: 'inicio_oferta_1',
  location_id: '/inicio'
});
```

| Parâmetro | Tipo | Obrigatório | Significado | Valores | LGPD |
| --- | --- | --- | --- | --- | --- |
| `promotion_id` | string | Sim | Código do banner no catálogo de campanhas. | Ver aba Banners | Não pessoal |
| `promotion_name` | string | Sim | Nome do banner para leitura humana. | Ver aba Banners | Não pessoal |
| `creative_slot` | string | Sim | Posição do banner na tela. | Ver aba Banners | Não pessoal |
| `location_id` | string | Sim | Tela onde o banner estava. | /acesso, /inicio, /cartoes | Não pessoal |

**Onde está no código**

- `index.html`, linha 688, listener global de clique, ramo .promo-cta: `track('select_promotion', promoData(promoCta.closest('[data-promo]')))`

**Elementos no app.** EL-11, EL-13, EL-15, EL-36, EL-38, EL-40, EL-62 (ver Mapa por tela).


**GTM.** Acionador `CE · select_promotion`, tag `GA4 · select_promotion`. Owner: Marketing Digital.

## form_start

**Catálogo GA4 (TagOps).** GA4 automático.

**O que é.** O cliente começou a preencher um formulário: a senha (form_id=login) ou o Pix (form_id=pix).

**Quando dispara.** No primeiro gesto de preenchimento do formulário, uma vez por abertura da tela. Login: no primeiro dígito da senha, uma vez a cada visita a /entrar. Pix: no primeiro foco num campo de #pix-form, uma vez a cada abertura do Pix.

**Diferença para eventos parecidos.** Início do preenchimento (login ou Pix). A abertura da tela é page_view; o envio é form_submit.

**Uso em análise.** Etapa 1 dos funis de login (form_id=login) e de Pix (form_id=pix).

**Com o que se conecta.** Formulário (form_id) · Tela (page_path)

**Uso pela IA**

- Para responder perguntas: Quantos clientes começam a digitar a senha ou o Pix e não terminam?
- Para tomar decisões: Identificar abandono no login e no Pix e oferecer ajuda.

**Código do dataLayer**

```js
// Quando: No primeiro gesto de preenchimento do formulário, uma vez por abertura da tela.
window.dataLayer.push({
  event: 'form_start',
  form_id: 'pix',
  page_path: '/pix'
});
```

| Parâmetro | Tipo | Obrigatório | Significado | Valores | LGPD |
| --- | --- | --- | --- | --- | --- |
| `form_id` | string | Sim | Formulário em uso. | login, pix | Não pessoal |
| `page_path` | string | Sim | Tela onde o toque ou o formulário aconteceu. | /acesso, /entrar, /inicio, /extrato, /pix, /cartoes, /investimentos | Não pessoal |

**Onde está no código**

- `index.html`, linha 723, pressKey(), primeiro dígito da senha: `track('form_start', { form_id: 'login', page_path: '/entrar' })`
- `index.html`, linha 833, listener focusin de #pix-form: `track('form_start', { form_id: 'pix', page_path: '/pix' })`

**Elementos no app.** EL-18, EL-50 (ver Mapa por tela).


**GTM.** Acionador `CE · form_start`, tag `GA4 · form_start`. Owner: Produto Digital.

## login

**Catálogo GA4 (TagOps).** GA4 recomendado.

**O que é.** O cliente entrou na área logada.

**Quando dispara.** No toque em Entrar com 6 dígitos aceitos, logo depois do click btn_entrar e antes de ir para o destino guardado (ou /inicio).

**Diferença para eventos parecidos.** Só login bem-sucedido, logo depois do form_submit step=aprovado. Tentativas recusadas são form_submit step=recusado. A saída é o click link_id=sair.

**Uso em análise.** Conversão do funil de login e início da sessão identificada.

**Com o que se conecta.** Cliente (user_id) · Segmento (customer_segment)

**Uso pela IA**

- Para responder perguntas: Quantos logins por segmento de cliente houve hoje?
- Para tomar decisões: Escolher as ofertas da área logada conforme o segmento.

**Código do dataLayer**

```js
// Quando: No toque em Entrar com 6 dígitos aceitos, logo depois do click btn_entrar e antes de ir para o destino guardado (ou /inicio).
window.dataLayer.push({
  event: 'login',
  method: 'senha_eletronica',
  user_id: 'u_8f2c41a9',
  customer_segment: 'pf_alta_renda'
});
```

| Parâmetro | Tipo | Obrigatório | Significado | Valores | LGPD |
| --- | --- | --- | --- | --- | --- |
| `method` | string | Sim | Forma de login usada. | senha_eletronica | Não pessoal |
| `user_id` | string | Sim | Identificador pseudonimizado do cliente. Liga eventos ao mesmo cliente sem expor quem ele é. | u_ + hash | Pseudonimizado |
| `customer_segment` | string | Sim | Segmento comercial do cliente. | pf_alta_renda (teste) | Não pessoal (segmento) |

**Onde está no código**

- `index.html`, linha 741, submitLogin(), ramo de sucesso: `track('login', { method: 'senha_eletronica', user_id: S.user.id, customer_segment: S.user.segment })`

**Elementos no app.** EL-22 (ver Mapa por tela).


**GTM.** Acionador `CE · login`, tag `GA4 · login`. Owner: Governança de Dados Digitais.

## form_submit

**Catálogo GA4 (TagOps).** GA4 automático.

**O que é.** O cliente enviou um formulário: a senha (form_id=login) ou o Pix (form_id=pix). O step diz o resultado: aprovado ou recusado no login; recusado, revisao ou confirmado no Pix.

**Quando dispara.** No toque no botão que envia o formulário (Entrar, Continuar ou Confirmar Pix), logo depois do click do mesmo botão. Login: step=recusado com menos de 6 dígitos (senha_incompleta) ou com 000000 (senha_incorreta); step=aprovado com 6 dígitos aceitos, antes do evento login. Pix: no toque em Continuar, logo depois do click pix_continuar, com step=recusado (sem chave, valor inválido ou acima do saldo) ou step=revisao (dados válidos); no toque em Confirmar Pix, depois de debitar o saldo, com step=confirmado.

**Diferença para eventos parecidos.** Envio de formulário com o resultado em step. Erro de validação é step=recusado (com error_type), não um evento separado. No Pix, step=revisao ainda não é Pix enviado; só step=confirmado conta como Pix concluído. Não é purchase: Pix não é receita do banco.

**Uso em análise.** Taxa de erro do login e do Pix por error_type (step=recusado); etapas 2 (revisao) e 3 (confirmado) do funil de Pix; volume e valor de Pix concluídos.

**Com o que se conecta.** Formulário (form_id) · Resultado (step, error_type) · Transação (transaction_id, só Pix confirmado) · Cliente (via login)

**Uso pela IA**

- Para responder perguntas: Qual erro mais trava o login e o Pix, e quantos Pix foram confirmados hoje?
- Para tomar decisões: Mudar a mensagem do erro mais comum e medir a conversão dos funis de login e Pix.

**Código do dataLayer**

```js
// Quando: No toque no botão que envia o formulário (Entrar, Continuar ou Confirmar Pix), logo depois do click do mesmo botão.
window.dataLayer.push({
  event: 'form_submit',
  form_id: 'pix',
  step: 'confirmado',
  error_type: undefined,
  value: 150.00,
  currency: 'BRL',
  pix_key_type: 'email',
  transaction_id: 'E1792334211000'
});
```

| Parâmetro | Tipo | Obrigatório | Significado | Valores | LGPD |
| --- | --- | --- | --- | --- | --- |
| `form_id` | string | Sim | Formulário em uso. | login, pix | Não pessoal |
| `step` | string | Sim | Resultado do envio. No Pix, só confirmado é Pix concluído. | login: aprovado, recusado · pix: recusado, revisao, confirmado | Não pessoal |
| `error_type` | string | Só em step=recusado | Motivo da recusa. Nos outros steps vai como undefined. | login: senha_incompleta, senha_incorreta · pix: chave_vazia, valor_invalido, saldo_insuficiente | Não pessoal |
| `value` | number | Só no Pix (revisao, confirmado) | Valor do Pix em reais, com ponto decimal. Não é receita: o evento não é purchase. | > 0 e ≤ saldo | Dado financeiro (não identifica o cliente sozinho) |
| `currency` | string | Só no Pix (revisao, confirmado) | Moeda do valor. | BRL | Não pessoal |
| `pix_key_type` | string | Só no Pix (revisao, confirmado) | Tipo da chave do recebedor. A chave em si nunca é enviada. | email, telefone, cpf, cnpj, aleatoria | Não pessoal |
| `transaction_id` | string | Só em step=confirmado | Identificador do Pix. Liga o evento à transação no core. Em step=revisao vai como undefined. | E + timestamp (teste) | Não pessoal (técnico) |

**Onde está no código**

- `index.html`, linha 732, loginFail(), senha recusada (step=recusado): `track('form_submit', { form_id: 'login', step: 'recusado', error_type: type, value: undefined, currency: undefined, pix_key_type: undefined, transaction_id: undefined })`
- `index.html`, linha 740, submitLogin(), senha aceita (step=aprovado): `track('form_submit', { form_id: 'login', step: 'aprovado', error_type: undefined, value: undefined, currency: undefined, pix_key_type: undefined, transaction_id: undefined })`
- `index.html`, linha 841, listener submit de #pix-form, ramo de erro (step=recusado): `track('form_submit', { form_id: 'pix', step: 'recusado', error_type: err[0], value: undefined, currency: undefined, pix_key_type: undefined, transaction_id: undefined })`
- `index.html`, linha 852, listener submit de #pix-form, ramo válido (step=revisao): `track('form_submit', { form_id: 'pix', step: 'revisao', error_type: undefined, value: v, currency: 'BRL', pix_key_type: S.pending.tipo, transaction_id: undefined })`
- `index.html`, linha 869, listener de clique de #pix-confirmar (step=confirmado): `track('form_submit', { form_id: 'pix', step: 'confirmado', error_type: undefined, value: p.v, currency: 'BRL', pix_key_type: p.tipo, transaction_id: id })`

**Elementos no app.** EL-20, EL-21, EL-22, EL-51, EL-52, EL-53 (ver Mapa por tela).


**GTM.** Acionador `CE · form_submit`, tag `GA4 · form_submit`. Owner: Produto Digital.

## generate_lead

**Catálogo GA4 (TagOps).** GA4 recomendado.

**O que é.** Alguém pediu um produto: abertura de conta (quem ainda não é cliente) ou cartão (cliente logado).

**Quando dispara.** No toque em 'Abrir conta' ou 'Quero abrir' na tela de acesso (abertura_conta) e em 'Pedir o Black' (cartao_black) ou 'Pedir adicional' (cartao_adicional) na tela Cartões. Sai depois do click e, nos banners, depois de select_promotion.

**Diferença para eventos parecidos.** Pedido de produto (conta ou cartão). Interesse em oferta de crédito ou seguro é só select_promotion, sem lead.

**Uso em análise.** Aquisição de novos clientes (abertura_conta) e pedidos de cartão por lead_source.

**Com o que se conecta.** Tipo de pedido (lead_source) · Banner (via select_promotion, quando vem do banner) · Tela (page_path)

**Uso pela IA**

- Para responder perguntas: Quantos pedidos de abertura de conta e de cartão chegam por dia, e de qual tela?
- Para tomar decisões: Enviar o lead para o fluxo de abertura de conta ou para a análise de crédito do cartão.

**Código do dataLayer**

```js
// Quando: No toque em 'Abrir conta' ou 'Quero abrir' na tela de acesso (abertura_conta) e em 'Pedir o Black' (cartao_black) ou 'Pedir adicional' (cartao_adicional) na tela Cartões.
window.dataLayer.push({
  event: 'generate_lead',
  lead_source: 'cartao_black',
  page_path: '/cartoes'
});
```

| Parâmetro | Tipo | Obrigatório | Significado | Valores | LGPD |
| --- | --- | --- | --- | --- | --- |
| `lead_source` | string | Sim | Tipo de pedido. Nome de parâmetro do GA4 para generate_lead. | abertura_conta, cartao_black, cartao_adicional | Não pessoal |
| `page_path` | string | Sim | Tela onde o toque ou o formulário aconteceu. | /acesso, /entrar, /inicio, /extrato, /pix, /cartoes, /investimentos | Não pessoal |

**Onde está no código**

- `index.html`, linha 696, listener global de clique, ramo data-action=lead: `track('generate_lead', { lead_source: item, page_path: '/' + S.route })`
- `index.html`, linha 702, listener global de clique, ramo data-action=cartao: `track('generate_lead', { lead_source: 'cartao_' + item, page_path: '/' + S.route })`

**Elementos no app.** EL-08, EL-11, EL-62, EL-63 (ver Mapa por tela).


**GTM.** Acionador `CE · generate_lead`, tag `GA4 · generate_lead`. Owner: Marketing Aquisição.

## select_item

**Catálogo GA4 (TagOps).** GA4 recomendado.

**O que é.** O cliente escolheu um produto de investimento para aplicar.

**Quando dispara.** No toque em Investir num produto da tela Investimentos, logo depois do click do mesmo botão.

**Diferença para eventos parecidos.** Intenção de aplicar, não aplicação concluída.

**Uso em análise.** Intenção por produto de investimento.

**Com o que se conecta.** Produto (items[0].item_id) · Lista (item_list_id) · Cliente (via login)

**Uso pela IA**

- Para responder perguntas: Qual produto de investimento gera mais intenção de aplicar?
- Para tomar decisões: Mostrar o produto certo para cada perfil.

**Código do dataLayer**

```js
// Quando: No toque em Investir num produto da tela Investimentos, logo depois do click do mesmo botão.
window.dataLayer.push({
  event: 'select_item',
  item_list_id: 'renda_fixa',
  item_list_name: 'Renda fixa',
  items: [{ item_id: 'cdb_liquidez', item_name: 'CDB Liquidez Diária', item_category: 'renda_fixa' }]
});
```

| Parâmetro | Tipo | Obrigatório | Significado | Valores | LGPD |
| --- | --- | --- | --- | --- | --- |
| `item_list_id` | string | Sim | Lista de produtos onde o cliente escolheu. | renda_fixa | Não pessoal |
| `item_list_name` | string | Sim | Nome da lista para leitura humana. | Renda fixa | Não pessoal |
| `items` | array | Sim | Produto escolhido, no formato de item do GA4: item_id, item_name e item_category. | item_id: cdb_liquidez, lci_90, cdb_ipca_2a, fundo_di | Não pessoal |

**Onde está no código**

- `index.html`, linha 705, listener global de clique, ramo data-action=investir: `track('select_item', { item_list_id: 'renda_fixa', item_list_name: 'Renda fixa', items: [prod] })`

**Elementos no app.** EL-65, EL-66, EL-67, EL-68 (ver Mapa por tela).


**GTM.** Acionador `CE · select_item`, tag `GA4 · select_item`. Owner: Produto Investimentos.
