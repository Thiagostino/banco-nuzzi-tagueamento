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
                "| ID | Área | Elemento | Seletor | Gesto | Eventos | Valores fixos | Print |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        out.append(f"| {m['id']} | {m['area']} | {m['element']} | `{m['selector']}` | {m['gesture']} | {m['events']} | {m['fixed_values']} | [ver](../{m['print']}) |")
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
        out += ["", "**Elementos no app.** " + (", ".join(elements_of(e["eventName"])) or "nenhum") + " (ver Mapa por tela).", ""]
        out += ["", f"**GTM.** Acionador `{e['gtm']['trigger']}`, tag `{e['gtm']['tag']}`. Owner: {e['owner']}.", ""]
    return "\n".join(out)


def elements_of(event_name):
    import re
    return [m["id"] for m in plan["catalogs"]["tagMap"] if event_name in re.split(r"\s*→\s*", m["events"])]


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
          "Contém dado pessoal?", "Gatilho no GTM", "Owner", "Status", "Descrição completa para a IA",
          "Elementos no app (IDs do Mapa de tagueamento)"]
    rows = [[e["id"], e["eventName"], e["category"], e["description"]["behavior"], e["description"]["trigger"],
             e["dataLayerPush"], e["description"]["disambiguation"], e["description"]["useCases"], e["screens"], e["selector"], e["connectsTo"],
             ", ".join(p["name"] for p in e["eventProperties"]) or "(nenhum)", e["aiUses"]["answerQuestions"],
             e["aiUses"]["makeDecisions"], e["containsPersonalData"], f"Acionador {e['gtm']['trigger']} · Tag {e['gtm']['tag']}",
             e["owner"], e["status"], e["aiDescription"], ", ".join(elements_of(e["eventName"]))] for e in events]
    sheet("Eventos", eh, rows, [8, 18, 12, 36, 44, 46, 40, 34, 18, 26, 32, 30, 34, 34, 28, 28, 22, 12, 60, 40],
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
    mh = ["ID", "Tela", "Área da tela", "Elemento (o que o cliente vê)", "Seletor no código", "Gesto",
          "Eventos disparados, em ordem", "Valores fixos enviados", "Observação", "Arquivo do print", "Print (elemento destacado)"]
    mrows = [[m["id"], m["screen"], m["area"], m["element"], m["selector"], m["gesture"], m["events"],
              m["fixed_values"], m["note"], m["print"], ""] for m in c["tagMap"]]
    sheet("Mapa de tagueamento", mh, mrows, [8, 14, 20, 26, 34, 18, 30, 44, 30, 24, 30], mono_cols=("Seletor no código",))
    from openpyxl.drawing.image import Image as XLImage
    ws = wb["Mapa de tagueamento"]
    for i, m in enumerate(c["tagMap"], start=2):
        img_path = ROOT / m["print"]
        if not img_path.exists():
            continue
        img = XLImage(str(img_path))
        img.width, img.height = 200, int(200 * img.height / img.width)
        ws.add_image(img, f"K{i}")
        ws.row_dimensions[i].height = img.height * 0.75 + 6
    ws.freeze_panes = "B2"
    sheet("Jornadas", ["Jornada", "Passo", "Ação do cliente", "Evento esperado", "Parâmetros a conferir", "Resultado no teste"],
          [list(j.values()) for j in c["journeys"]], [24, 7, 38, 40, 52, 22])
    sheet("Elementos", ["item_id (data-track)", "content_type", "Texto enviado (link_text)", "Onde fica", "Destino"],
          [list(x.values()) for x in c["elements"]], [26, 14, 24, 30, 20])
    del wb["Sheet"]
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


DL_CSS = """
/* ---------- Painel do dataLayer (só no index-datalayer.html) ---------- */
.stage { gap: 28px; }
.dlp { display: none; flex-direction: column; gap: 10px; width: 420px; height: min(820px, calc(100vh - 48px)); min-height: 600px; background: var(--white); border: 1px solid var(--navy-12); border-radius: 24px; padding: 16px; color: var(--navy); }
.dlp-head { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.dlp-head strong { font-family: var(--font-mono); font-size: 15px; }
.dlp-head .n { font-family: var(--font-mono); font-size: 12px; background: var(--navy); color: var(--white); border-radius: 999px; padding: 1px 8px; }
.dlp-btns { margin-left: auto; display: flex; gap: 6px; }
.dlp-btns button { border: 1px solid var(--navy-12); background: var(--gray); color: var(--navy); border-radius: 8px; padding: 6px 10px; font-size: 12.5px; font-weight: 700; }
.dlp-note { font-size: 12.5px; color: var(--navy-70); background: var(--gray); border-radius: 10px; padding: 8px 10px; }
.dlp-list { list-style: none; margin: 0; padding: 0; overflow: auto; flex: 1; min-height: 0; display: grid; gap: 8px; align-content: start; }
.dlp-list li { border: 1px solid var(--navy-12); border-radius: 12px; padding: 10px 12px; display: grid; gap: 6px; min-width: 0; }
.dlp-list li.new { animation: dlpin .5s ease-out; }
@keyframes dlpin { from { background: var(--gray); } to { background: var(--white); } }
.dlp-ev { display: flex; justify-content: space-between; gap: 8px; align-items: baseline; }
.dlp-ev b { font-family: var(--font-mono); font-size: 13px; }
.dlp-ev time { font-family: var(--font-mono); font-size: 11.5px; color: var(--navy-70); }
.dlp-when { font-size: 12.5px; line-height: 1.45; }
.dlp-when span { font-weight: 800; }
.dlp-els { display: flex; flex-wrap: wrap; gap: 4px; }
.dlp-els i { font-style: normal; font-family: var(--font-mono); font-size: 11px; background: var(--gray); border-radius: 6px; padding: 1px 6px; }
.dlp-list pre { margin: 0; font-family: var(--font-mono); font-size: 11.5px; line-height: 1.5; white-space: pre-wrap; overflow-wrap: anywhere; background: var(--gray); border-radius: 8px; padding: 8px; }
.dlp-empty { color: var(--navy-70); font-size: 13px; }
.dlp-toggle { position: fixed; z-index: 60; right: calc(16px + env(safe-area-inset-right, 0px)); bottom: calc(96px + env(safe-area-inset-bottom, 0px)); padding: 10px 14px; border-radius: 999px; border: 0; background: var(--navy); color: var(--white); font-family: var(--font-mono); font-size: 12.5px; box-shadow: 0 8px 24px var(--navy-12); }
#dlp-fallback { width: 100%; height: 110px; font-family: var(--font-mono); font-size: 11.5px; border-radius: 8px; border: 1px solid var(--navy-12); }
@media (min-width: 1000px) { .dlp { display: flex; } .dlp-toggle, #dlp-close { display: none; } }
@media (max-width: 999px) {
  .dlp.open { display: flex; position: fixed; z-index: 70; inset: 0; width: auto; height: auto; min-height: 0; border-radius: 0; padding: calc(16px + env(safe-area-inset-top, 0px)) max(16px, env(safe-area-inset-right, 0px)) calc(16px + env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px)); }
}
"""

DL_PANEL = """
  <aside class="dlp" id="dlp" aria-label="Eventos do dataLayer">
    <div class="dlp-head">
      <strong>dataLayer</strong><span class="n" id="dlp-n">0</span>
      <div class="dlp-btns">
        <button type="button" id="dlp-copy">Copiar JSON</button>
        <button type="button" id="dlp-clear">Limpar</button>
        <button type="button" id="dlp-close">Fechar</button>
      </div>
    </div>
    <p class="dlp-note">Cada push aparece aqui no momento em que dispara, o mais recente no topo, com a regra de disparo do plano e o elemento do mapa (EL-xx) que gerou o push. Parâmetros enviados como undefined aparecem como undefined.</p>
    <textarea id="dlp-fallback" readonly hidden aria-label="JSON do dataLayer para copiar"></textarea>
    <ol class="dlp-list" id="dlp-list"><li class="dlp-empty">Nenhum evento ainda. Use o app ao lado.</li></ol>
  </aside>
"""

DL_SCRIPT = """
<script>
  // Painel do dataLayer: intercepta cada push e mostra no momento do disparo.
  (function () {
    var META = __META__;
    var dl = window.dataLayer = window.dataLayer || [];
    var queue = [], log = [];
    var orig = dl.push;
    dl.push = function () {
      var out = orig.apply(dl, arguments);
      for (var i = 0; i < arguments.length; i++) queue.push({ time: new Date(), p: arguments[i] });
      if (document.readyState !== 'loading') flush();
      return out;
    };
    function pad(n) { return String(n).padStart(2, '0'); }
    // Escolhe no mapa os elementos cujos valores fixos batem com o push (ex.: item_id, promotion_id, page_path).
    function pick(rows, p) {
      var best = 0, out = [];
      rows.forEach(function (r) {
        var keys = Object.keys(r.t), score = 0, clash = false;
        keys.forEach(function (k) { if (k in p) { if (String(p[k]) === r.t[k]) score++; else clash = true; } });
        if (clash) return;
        if (score > best) { best = score; out = [r.id]; } else if (score === best) out.push(r.id);
      });
      return out;
    }
    function show(v) {
      var keys = Object.keys(v);
      return '{\\n' + keys.map(function (k) {
        var x = v[k];
        return '  "' + k + '": ' + (x === undefined ? 'undefined' : JSON.stringify(x));
      }).join(',\\n') + '\\n}';
    }
    function flush() {
      var list = document.getElementById('dlp-list');
      if (!list) return;
      while (queue.length) {
        var item = queue.shift(); log.unshift(item);
        if (list.firstChild && list.firstChild.className === 'dlp-empty') list.innerHTML = '';
        var m = Object.assign({}, META[item.p.event] || {});
        var li = document.createElement('li'); li.className = 'new';
        var head = document.createElement('div'); head.className = 'dlp-ev';
        var b = document.createElement('b'); b.textContent = item.p.event || '(sem event)';
        var t = document.createElement('time'); t.textContent = pad(item.time.getHours()) + ':' + pad(item.time.getMinutes()) + ':' + pad(item.time.getSeconds());
        head.appendChild(b); head.appendChild(t); li.appendChild(head);
        if (m.when) { var w = document.createElement('p'); w.className = 'dlp-when'; var s = document.createElement('span'); s.textContent = 'Quando dispara: '; w.appendChild(s); w.appendChild(document.createTextNode(m.when)); li.appendChild(w); }
        m.els = pick(m.rows || [], item.p);
        if (m.els && m.els.length) { var e = document.createElement('div'); e.className = 'dlp-els'; m.els.forEach(function (id) { var c = document.createElement('i'); c.textContent = id; e.appendChild(c); }); li.appendChild(e); }
        var pre = document.createElement('pre'); pre.textContent = show(item.p); li.appendChild(pre);
        list.insertBefore(li, list.firstChild);
      }
      document.getElementById('dlp-n').textContent = log.length;
    }
    document.addEventListener('DOMContentLoaded', function () {
      flush();
      var panel = document.getElementById('dlp'), tog = document.getElementById('dlp-toggle');
      tog.addEventListener('click', function () { panel.classList.add('open'); tog.hidden = true; });
      document.getElementById('dlp-close').addEventListener('click', function () { panel.classList.remove('open'); tog.hidden = false; });
      document.getElementById('dlp-clear').addEventListener('click', function () { log.length = 0; document.getElementById('dlp-list').innerHTML = '<li class="dlp-empty">Painel limpo. Os próximos eventos aparecem aqui.</li>'; document.getElementById('dlp-n').textContent = '0'; });
      document.getElementById('dlp-copy').addEventListener('click', function () {
        var btn = this, text = '[\\n' + dl.filter(function (x) { return x && x.event; }).map(show).join(',\\n') + '\\n]';
        function fallback() { var ta = document.getElementById('dlp-fallback'); ta.value = text; ta.hidden = false; ta.focus(); ta.select(); btn.textContent = 'Selecione e copie'; }
        try { navigator.clipboard.writeText(text).then(function () { btn.textContent = 'Copiado'; setTimeout(function () { btn.textContent = 'Copiar JSON'; }, 1800); }, fallback); } catch (err) { fallback(); }
      });
    });
  })();
</script>
"""


def datalayer_html():
    """index-datalayer.html = index.html + painel lateral do dataLayer (gerado, não editar à mão)."""
    import re
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    meta = {}
    for e in events:
        rows = []
        for m in plan["catalogs"]["tagMap"]:
            if e["eventName"] not in re.split(r"\s*→\s*", m["events"]):
                continue
            tokens = {}
            for part in m["fixed_values"].split(" · "):
                if part.startswith("depois") or "=" not in part:
                    continue
                k, v = part.split("=", 1)
                if " " not in v.strip():
                    tokens[k.strip()] = v.strip()
            rows.append({"id": m["id"], "t": tokens})
        meta[e["eventName"]] = {"when": e["description"]["trigger"], "rows": rows}
    script = DL_SCRIPT.replace("__META__", json.dumps(meta, ensure_ascii=False))
    html = html.replace("<title>Banco Nuzzi</title>", "<title>Banco Nuzzi dataLayer</title>", 1)
    html = html.replace("</script>\n<!-- Cole aqui", "</script>" + script + "<!-- Cole aqui", 1)
    html = html.replace("</style>\n</head>", DL_CSS + "</style>\n</head>", 1)
    marker = '    <div class="toast" id="toast" role="status" aria-live="polite" hidden></div>\n  </div>\n'
    assert marker in html, "estrutura do index.html mudou"
    html = html.replace(marker, marker + DL_PANEL, 1)
    app_script = "<script>\n(function () {\n  var dl = window.dataLayer"
    assert app_script in html, "script do app não encontrado"
    html = html.replace(app_script, '<button class="dlp-toggle" id="dlp-toggle" type="button">dataLayer</button>\n\n' + app_script, 1)
    html = html.replace("<!doctype html>", "<!doctype html>\n<!-- Gerado por tools/gerar_artefatos.py a partir do index.html. Não edite à mão. -->", 1)
    (ROOT / "index-datalayer.html").write_text(html, encoding="utf-8")


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
    datalayer_html()
    (ROOT / "gtm").mkdir(exist_ok=True)
    (ROOT / "gtm" / "container-banco-nuzzi.json").write_text(json.dumps(gtm_container(), ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "tracking-plan" / "eventos.md").write_text(eventos_md(), encoding="utf-8")
    try:
        xlsx(ROOT / "docs" / "plano-de-tagueamento-banco-nuzzi.xlsx")
    except ImportError:
        print("openpyxl não instalado: planilha não gerada")
    print("artefatos gerados")
