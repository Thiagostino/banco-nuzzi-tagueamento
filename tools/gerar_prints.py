#!/usr/bin/env python3
"""Gera um print de cada elemento do mapa de tagueamento, com o elemento destacado.

Uso: python3 tools/gerar_prints.py        (requer: pip install playwright pillow && playwright install chromium)

Lê catalogs.tagMap do tracking-plan.json, coloca o app no estado certo para cada linha
(deslogado, logado, banner do carrossel, etapa do Pix, erro de senha), destaca o elemento
e salva em docs/prints/<ID>.jpg.
"""
import io
import json
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
plan = json.loads((ROOT / "tracking-plan" / "tracking-plan.json").read_text(encoding="utf-8"))
URL = (ROOT / "index.html").resolve().as_uri()
OUT = ROOT / "docs" / "prints"
OUT.mkdir(parents=True, exist_ok=True)

SCROLL_JS = """
(sel) => {
  const el = [...document.querySelectorAll(sel)].find(e => e.getClientRects().length > 0 && !e.closest('[hidden]'));
  if (!el) return false;
  const track = el.closest('.track');
  const slide = el.closest('.slide');
  if (track && slide) track.scrollLeft = slide.offsetLeft - track.offsetLeft;
  el.scrollIntoView({ block: 'center', inline: 'nearest' });
  return true;
}
"""

HIGHLIGHT_JS = """
([sel, label, whole]) => {
  document.querySelectorAll('.__hl').forEach(n => n.remove());
  const app = document.querySelector('#app').getBoundingClientRect();
  const visible = el => el.getClientRects().length > 0 && !el.closest('[hidden]');
  let els = [...document.querySelectorAll(sel)].filter(visible);
  if (!els.length) return 0;
  const box = (r, i) => {
    const d = document.createElement('div');
    d.className = '__hl';
    const pad = whole ? -6 : 4;
    Object.assign(d.style, { position: 'fixed', zIndex: 9999, pointerEvents: 'none',
      left: (r.left - pad) + 'px', top: (r.top - pad) + 'px', width: (r.width + 2 * pad) + 'px', height: (r.height + 2 * pad) + 'px',
      border: '3px solid #E5484D', borderRadius: whole ? '30px' : '12px', boxShadow: '0 0 0 4px rgba(229,72,77,.25)' });
    document.body.appendChild(d);
    if (i === 0) {
      const t = document.createElement('div');
      t.className = '__hl';
      t.textContent = label;
      const top = Math.max(app.top + 6, r.top - pad - 26);
      const left = Math.min(Math.max(app.left + 6, r.left - pad), app.right - 70);
      Object.assign(t.style, { position: 'fixed', zIndex: 10000, left: left + 'px', top: top + 'px', background: '#E5484D',
        color: '#fff', font: '800 12px system-ui, sans-serif', padding: '3px 8px', borderRadius: '6px', letterSpacing: '.04em' });
      document.body.appendChild(t);
    }
  };
  els.forEach((el, i) => box(whole ? app : el.getBoundingClientRect(), i));
  return els.length;
}
"""


def main():
    rows = plan["catalogs"]["tagMap"]
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 440, "height": 900}, device_scale_factor=1.5)
        n = 0

        def fresh(hash_=""):
            nonlocal n
            n += 1
            page.goto(f"{URL}?r={n}#{hash_}" if hash_ else f"{URL}?r={n}")
            page.add_style_tag(content="*{scroll-behavior:auto!important;transition:none!important;animation:none!important}.toast{display:none!important}")
            page.wait_for_timeout(250)

        def login(target):
            fresh("entrar")
            for k in "123456":
                page.click(f'[data-key="{k}"]')
            page.click("#btn-entrar")
            page.wait_for_timeout(150)
            page.evaluate(f"location.hash = '{target}'")
            page.wait_for_timeout(250)

        def pix_fill():
            page.fill("#pix-chave", "ana@exemplo.com")
            page.fill("#pix-valor", "150,00")

        for row in rows:
            screen, el, sel = row["screen"], row["element"], row["selector"]
            if screen == "/acesso":
                fresh()
            elif screen == "/entrar":
                fresh("entrar")
                if "menos de 6" in el:
                    page.click('[data-key="1"]'); page.click('[data-key="2"]'); page.click("#btn-entrar")
                elif "000000" in el:
                    for _ in range(6):
                        page.click('[data-key="0"]')
                    page.click("#btn-entrar")
                elif "6 dígitos" in el:
                    for k in "123456":
                        page.click(f'[data-key="{k}"]')
            elif screen == "/pix":
                login("pix")
                if "com erro" in el:
                    page.click("#pix-form [type=submit]")
                elif "válido" in el:
                    pix_fill()
                elif row["area"].startswith("Etapa 2"):
                    pix_fill(); page.click("#pix-form [type=submit]")
                elif row["area"].startswith("Etapa 3"):
                    pix_fill(); page.click("#pix-form [type=submit]"); page.click("#pix-confirmar")
            elif screen == "Telas logadas":
                login("inicio")
            else:
                login(screen.strip("/"))
            page.wait_for_timeout(200)
            whole = sel.startswith("[data-page=")
            if not whole:
                page.evaluate(SCROLL_JS, sel)
                page.wait_for_timeout(450)
            count = page.evaluate(HIGHLIGHT_JS, [sel, row["id"], whole])
            if not count:
                raise SystemExit(f"{row['id']}: elemento não encontrado ({sel})")
            page.wait_for_timeout(120)
            png = page.locator("#app").screenshot()
            Image.open(io.BytesIO(png)).convert("RGB").save(OUT / f"{row['id']}.jpg", quality=82, optimize=True)
            print(row["id"], el)
        browser.close()


if __name__ == "__main__":
    main()
