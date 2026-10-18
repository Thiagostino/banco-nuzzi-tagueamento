#!/usr/bin/env python3
"""Confere o tracking plan contra o código do app.

Uso: python3 tools/validar_plano.py

Verifica:
- todo track('evento', {...}) do index.html está no plano, e vice-versa;
- os parâmetros enviados em cada chamada são os documentados no plano;
- todo data-track e todo data-promo do HTML estão nos catálogos;
- o trackingCode e a linha registrados no plano batem com o código atual.
Sai com código 1 se encontrar divergência.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html = (ROOT / "index.html").read_text(encoding="utf-8")
plan = json.loads((ROOT / "tracking-plan" / "tracking-plan.json").read_text(encoding="utf-8"))
problems = []


def calls():
    for m in re.finditer(r"track\('([a-z_]+)'", html):
        i, depth = m.start() + len("track"), 0
        for j in range(i, len(html)):
            if html[j] == "(":
                depth += 1
            elif html[j] == ")":
                depth -= 1
                if depth == 0:
                    break
        code = re.sub(r"\s+", " ", html[m.start():j + 1])
        arg = code.split(",", 1)[1] if "," in code else ""
        helper = re.match(r"\s*([A-Za-z_]\w*)\(", arg)
        if helper:  # parâmetros montados por uma função auxiliar, ex.: promoData(el)
            body = re.search(r"function " + helper.group(1) + r"\([^)]*\)\s*\{\s*return\s*(\{.*?\});", html, re.S)
            arg = body.group(1) if body else ""
        keys = re.findall(r"[{,]\s*([a-z_]+)\s*:", arg)
        yield m.group(1), html.count("\n", 0, m.start()) + 1, code, keys


code_events = {}
for name, line, code, keys in calls():
    code_events.setdefault(name, []).append((line, code, keys))

plan_events = {e["eventName"]: e for e in plan["trackingPlan"]}

for name in sorted(set(code_events) - set(plan_events)):
    problems.append(f"evento no código sem documentação: {name}")
for name in sorted(set(plan_events) - set(code_events)):
    problems.append(f"evento documentado que não existe no código: {name}")

for name, occurrences in code_events.items():
    ev = plan_events.get(name)
    if not ev:
        continue
    documented = {p["name"] for p in ev["eventProperties"]}
    for line, code, keys in occurrences:
        sent = set(keys)
        for k in sorted(sent - documented):
            problems.append(f"{name} (linha {line}): parâmetro enviado sem documentação: {k}")
        for k in sorted(documented - sent):
            problems.append(f"{name} (linha {line}): parâmetro documentado que não é enviado: {k}")
    registered = {(loc["originalLineNumberPreChanges"], loc["trackingCode"]) for loc in ev["implementationLocations"]}
    actual = {(line, code) for line, code, _ in occurrences}
    if registered != actual:
        problems.append(f"{name}: implementationLocations desatualizado (rode o gerador do plano)")

items = set(re.findall(r'data-track="([a-z_]+)"', html))
documented_items = {e["item_id"] for e in plan["catalogs"]["elements"]}
for i in sorted(items - documented_items):
    problems.append(f"data-track sem documentação: {i}")
for i in sorted(documented_items - items):
    problems.append(f"elemento documentado que não existe no HTML: {i}")

promos = set(re.findall(r'data-promo="([a-z_]+)"', html))
documented_promos = {b["promotion_id"] for b in plan["catalogs"]["banners"]}
for i in sorted(promos ^ documented_promos):
    problems.append(f"banner divergente entre HTML e catálogo: {i}")

# mapa de tagueamento: eventos e seletores
tag_map = plan["catalogs"].get("tagMap", [])
mapped_events = set()
for row in tag_map:
    for ev in re.split(r"\s*→\s*", row["events"]):
        mapped_events.add(ev)
        if ev not in plan_events:
            problems.append(f"mapa ({row['screen']} · {row['element']}): evento inexistente no plano: {ev}")
    for attr, val in re.findall(r"\[(data-[a-z-]+)=([a-z_]+)\]", row["selector"]):
        if f'{attr}="{val}"' not in html:
            problems.append(f"mapa ({row['screen']} · {row['element']}): seletor não encontrado no HTML: [{attr}={val}]")
    for el_id in re.findall(r"#([a-z][a-z0-9-]*)", row["selector"]):
        if f'id="{el_id}"' not in html:
            problems.append(f"mapa ({row['screen']} · {row['element']}): id não encontrado no HTML: #{el_id}")
for ev in sorted(set(plan_events) - mapped_events):
    problems.append(f"evento sem nenhum elemento no mapa de tagueamento: {ev}")
mapped_selectors = " ".join(r["selector"] for r in tag_map)
for i in sorted(items):
    if f"data-track={i}]" not in mapped_selectors:
        problems.append(f"data-track fora do mapa de tagueamento: {i}")
for i in sorted(promos):
    if f"data-promo={i}]" not in mapped_selectors:
        problems.append(f"banner fora do mapa de tagueamento: {i}")

if problems:
    print(f"{len(problems)} divergência(s):")
    for p in problems:
        print(" -", p)
    sys.exit(1)
print(f"OK: {len(plan_events)} eventos, {sum(len(v) for v in code_events.values())} chamadas, "
      f"{len(items)} elementos, {len(promos)} banners e {len(tag_map)} linhas do mapa batem com o plano.")
