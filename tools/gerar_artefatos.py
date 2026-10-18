#!/usr/bin/env python3
"""Gera os artefatos derivados do tracking plan (fonte única: tracking-plan/tracking-plan.json).

Uso: python3 tools/gerar_artefatos.py

Saídas:
- gtm/container-banco-nuzzi.json     contêiner para importar no Google Tag Manager
- tracking-plan/eventos.md           documentação legível, um bloco por evento
- docs/plano-de-tagueamento-banco-nuzzi.xlsx  planilha (requer openpyxl)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
plan = json.loads((ROOT / "tracking-plan" / "tracking-plan.json").read_text(encoding="utf-8"))
events = plan["trackingPlan"]


# ----------------------------------------------------------------- GTM
def gtm_container():
    ids = iter(range(1, 10000))
    variables, triggers, tags = [], [], []
    var_names = {}

    def tpl(key, value):
        return {"type": "TEMPLATE", "key": key, "value": value}

    variables.append({"variableId": str(next(ids)), "name": "GA4 · ID de métricas", "type": "c",
                      "parameter": [tpl("value", "G-XXXXXXXXXX")],
                      "notes": "Troque pelo ID de métricas da sua propriedade GA4."})
    params = sorted({p["name"] for e in events for p in e["eventProperties"]})
    for p in params:
        name = f"DLV · {p}"
        var_names[p] = name
        variables.append({"variableId": str(next(ids)), "name": name, "type": "v",
                          "parameter": [{"type": "INTEGER", "key": "dataLayerVersion", "value": "2"},
                                        {"type": "BOOLEAN", "key": "setDefaultValue", "value": "false"},
                                        tpl("name", p)]})

    tags.append({"tagId": str(next(ids)), "name": "GA4 · Google tag", "type": "googtag",
                 "parameter": [tpl("tagId", "{{GA4 · ID de métricas}}"),
                               {"type": "LIST", "key": "configSettingsTable", "list": [
                                   {"type": "MAP", "map": [tpl("parameter", "send_page_view"), tpl("parameterValue", "false")]}]}],
                 "firingTriggerId": ["2147479573"], "tagFiringOption": "ONCE_PER_EVENT",
                 "notes": "send_page_view=false: o app envia o próprio page_view a cada troca de tela (#hash)."})

    for e in events:
        trig_id = str(next(ids))
        triggers.append({"triggerId": trig_id, "name": e["gtm"]["trigger"], "type": "CUSTOM_EVENT",
                         "customEventFilter": [{"type": "EQUALS", "parameter": [
                             tpl("arg0", "{{_event}}"), tpl("arg1", e["eventName"])]}],
                         "notes": e["description"]["trigger"]})
        rows = [{"type": "MAP", "map": [tpl("parameter", p["name"]), tpl("parameterValue", "{{" + var_names[p["name"]] + "}}")]}
                for p in e["eventProperties"]]
        parameter = [{"type": "BOOLEAN", "key": "sendEcommerceData", "value": "false"},
                     tpl("eventName", e["eventName"]),
                     tpl("measurementIdOverride", "{{GA4 · ID de métricas}}")]
        if rows:
            parameter.append({"type": "LIST", "key": "eventSettingsTable", "list": rows})
        tags.append({"tagId": str(next(ids)), "name": e["gtm"]["tag"], "type": "gaawe", "parameter": parameter,
                     "firingTriggerId": [trig_id], "tagFiringOption": "ONCE_PER_EVENT",
                     "notes": e["description"]["behavior"]})

    return {
        "exportFormatVersion": 2,
        "exportTime": plan["updatedAt"] + " 12:00:00",
        "containerVersion": {
            "path": "accounts/0/containers/0/versions/0", "accountId": "0", "containerId": "0", "containerVersionId": "0",
            "name": f"Banco Nuzzi · tracking plan {plan['version']}",
            "container": {"path": "accounts/0/containers/0", "accountId": "0", "containerId": "0",
                          "name": "Banco Nuzzi", "publicId": "GTM-XXXXXXX", "usageContext": ["WEB"]},
            "tag": tags, "trigger": triggers, "variable": variables,
            "builtInVariable": [{"accountId": "0", "containerId": "0", "type": "EVENT", "name": "Event"}],
        },
    }


# ----------------------------------------------------------------- Markdown
def eventos_md():
    out = [f"# Eventos do Banco Nuzzi", "",
           f"Versão {plan['version']} · atualizado em {plan['updatedAt']} · gerado de `tracking-plan.json` por `tools/gerar_artefatos.py`.", "",
           plan["documentationPrinciple"], "",
           "| Evento | Categoria | Quando dispara | Status |", "| --- | --- | --- | --- |"]
    for e in events:
        out.append(f"| [`{e['eventName']}`](#{e['eventName']}) | {e['category']} | {e['description']['trigger'].split('. ')[0].rstrip('.')}. | {e['status']} |")
    out.append("")
    out += ["## Mapa por tela", "", "Cada elemento do app e os eventos que ele dispara, em ordem. Imagens das telas em `docs/telas/`.", ""]
    current = None
    for m in plan["catalogs"]["tagMap"]:
        if m["screen"] != current:
            current = m["screen"]
            shot = next((s["screenshot"] for s in plan["catalogs"]["screens"] if s["page_path"] == current), None)
            out += ["", f"### {current}", ""] + ([f"![{current}](../{shot})", ""] if shot else []) + [
                "| Área | Elemento | Seletor | Gesto | Eventos | Valores fixos |", "| --- | --- | --- | --- | --- | --- |"]
        out.append(f"| {m['area']} | {m['element']} | `{m['selector']}` | {m['gesture']} | {m['events']} | {m['fixed_values']} |")
    out.append("")
    for e in events:
        d = e["description"]
        out += [f"## {e['eventName']}", "",
                f"**O que é.** {d['behavior']}", "",
                f"**Quando dispara.** {d['trigger']}", "",
                f"**Diferença para eventos parecidos.** {d['disambiguation']}", "",
                f"**Uso em análise.** {d['useCases']}", "",
                f"**Com o que se conecta.** {e['connectsTo']}", "",
                "**Uso pela IA**", "",
                f"- Para responder perguntas: {e['aiUses']['answerQuestions']}",
                f"- Para tomar decisões: {e['aiUses']['makeDecisions']}", "",
                "**Código do dataLayer**", "", "```js", e["dataLayerPush"], "```", ""]
        if e["eventProperties"]:
            out += ["| Parâmetro | Tipo | Obrigatório | Significado | Valores | LGPD |", "| --- | --- | --- | --- | --- | --- |"]
            for p in e["eventProperties"]:
                out.append(f"| `{p['name']}` | {p['type']} | {p['required']} | {p['description']} | {p['possibleValues']} | {p['lgpd']} |")
            out.append("")
        out += ["**Onde está no código**", ""]
        for loc in e["implementationLocations"]:
            out.append(f"- `{loc['filePath']}`, linha {loc['originalLineNumberPreChanges']}, {loc['codeContext']}: `{loc['trackingCode']}`")
        out += ["", f"**GTM.** Acionador `{e['gtm']['trigger']}`, tag `{e['gtm']['tag']}`. Owner: {e['owner']}.", ""]
    return "\n".join(out)


# ----------------------------------------------------------------- XLSX
def xlsx(path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    head_fill, head_font = PatternFill("solid", fgColor="0E3B41"), Font(name="Arial", bold=True, color="FFFFFF", size=10)
    body, mono = Font(name="Arial", size=10), Font(name="Courier New", size=9)
    side = Side(style="thin", color="D6E0DF")
    border = Border(left=side, right=side, top=side, bottom=side)
    wb = Workbook()

    def sheet(title, headers, rows, widths, mono_cols=()):
        ws = wb.create_sheet(title)
        ws.append(headers)
        for r in rows:
            ws.append(r)
        for c in ws[1]:
            c.font, c.fill, c.border = head_font, head_fill, border
            c.alignment = Alignment(wrap_text=True, vertical="center")
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.font = mono if headers[c.column - 1] in mono_cols else body
                c.alignment, c.border = Alignment(wrap_text=True, vertical="top"), border
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.freeze_panes = "C2"
        ws.auto_filter.ref = ws.dimensions

    eh = ["ID", "Evento (event)", "Categoria", "O que o evento significa", "Quando deve disparar (gatilho exato)",
          "Código do dataLayer (dataLayer.push)", "Diferença para eventos parecidos", "Uso em análise (funil ou métrica)", "Tela (page_path)", "Elemento / seletor",
          "Com o que se conecta", "Parâmetros enviados", "Uso pela IA: responder perguntas", "Uso pela IA: tomar decisões",
          "Contém dado pessoal?", "Gatilho no GTM", "Owner", "Status", "Descrição completa para a IA"]
    rows = [[e["id"], e["eventName"], e["category"], e["description"]["behavior"], e["description"]["trigger"],
             e["dataLayerPush"], e["description"]["disambiguation"], e["description"]["useCases"], e["screens"], e["selector"], e["connectsTo"],
             ", ".join(p["name"] for p in e["eventProperties"]) or "(nenhum)", e["aiUses"]["answerQuestions"],
             e["aiUses"]["makeDecisions"], e["containsPersonalData"], f"Acionador {e['gtm']['trigger']} · Tag {e['gtm']['tag']}",
             e["owner"], e["status"], e["aiDescription"]] for e in events]
    sheet("Eventos", eh, rows, [8, 18, 12, 36, 44, 46, 40, 34, 18, 26, 32, 30, 34, 34, 28, 28, 22, 12, 60],
          mono_cols=("Código do dataLayer (dataLayer.push)",))
    ph = ["Evento", "Parâmetro", "Tipo", "Exemplo", "Obrigatório", "O que o valor significa", "Valores possíveis", "Origem do valor", "Classificação LGPD"]
    prow = [[e["eventName"], p["name"], p["type"], p["example"], p["required"], p["description"], p["possibleValues"], p["source"], p["lgpd"]]
            for e in events for p in e["eventProperties"]]
    sheet("Parâmetros", ph, prow, [20, 18, 10, 22, 14, 44, 40, 22, 26])
    c = plan["catalogs"]
    sheet("Banners", ["promotion_id", "promotion_name", "creative_slot", "Tela", "Texto do botão", "Destino ou ação", "Eventos no toque", "Exposição"],
          [list(b.values()) for b in c["banners"]], [24, 30, 18, 12, 20, 32, 44, 32])
    sheet("Telas", ["page_path", "page_title", "page_type", "Exige login", "Banners na tela", "Eventos que podem disparar", "Imagem da tela"],
          [list(t.values()) for t in c["screens"]], [16, 14, 14, 26, 50, 70, 30])
    sheet("Mapa de tagueamento", ["Tela", "Área da tela", "Elemento (o que o cliente vê)", "Seletor no código", "Gesto",
                                  "Eventos disparados, em ordem", "Valores fixos enviados", "Observação"],
          [list(m.values()) for m in c["tagMap"]], [16, 22, 30, 40, 22, 36, 52, 40])
    sheet("Jornadas", ["Jornada", "Passo", "Ação do cliente", "Evento esperado", "Parâmetros a conferir", "Resultado no teste"],
          [list(j.values()) for j in c["journeys"]], [24, 7, 38, 40, 52, 22])
    sheet("Elementos", ["item_id (data-track)", "content_type", "Texto enviado (link_text)", "Onde fica", "Destino"],
          [list(x.values()) for x in c["elements"]], [26, 14, 24, 30, 20])
    del wb["Sheet"]
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def refresh_locations():
    """Atualiza linha e trackingCode de cada evento a partir do index.html, mantendo o codeContext."""
    import re
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for e in events:
        found = []
        for m in re.finditer(r"track\('" + re.escape(e["eventName"]) + r"'", html):
            i, depth = m.start() + len("track"), 0
            for j in range(i, len(html)):
                if html[j] == "(":
                    depth += 1
                elif html[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
            found.append((html.count("\n", 0, m.start()) + 1, re.sub(r"\s+", " ", html[m.start():j + 1])))
        old = e["implementationLocations"]
        e["implementationLocations"] = [
            {"filePath": "index.html", "originalLineNumberPreChanges": line,
             "codeContext": old[k]["codeContext"] if k < len(old) else "preencher",
             "trackingCode": code}
            for k, (line, code) in enumerate(found)]
    (ROOT / "tracking-plan" / "tracking-plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    refresh_locations()
    (ROOT / "gtm").mkdir(exist_ok=True)
    (ROOT / "gtm" / "container-banco-nuzzi.json").write_text(json.dumps(gtm_container(), ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "tracking-plan" / "eventos.md").write_text(eventos_md(), encoding="utf-8")
    try:
        xlsx(ROOT / "docs" / "plano-de-tagueamento-banco-nuzzi.xlsx")
    except ImportError:
        print("openpyxl não instalado: planilha não gerada")
    print("artefatos gerados")
