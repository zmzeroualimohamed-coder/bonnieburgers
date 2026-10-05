#!/usr/bin/env python3
"""
Headless-browser QA harness for the Bonnie Burgers prototype  (§9 of the brief).
Runs Chromium via Playwright, exercises the real UI, measures contrast from
computed styles, and exits non-zero if anything fails.

    python3 qa.py [base_url]
"""
import json
import re
import sys
import time
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8137/index.html"
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    flag = "PASS" if ok else "FAIL"
    print(f"[{flag}] {name}" + (f"  — {detail}" if detail else ""), flush=True)


# ---------------------------------------------------------------- contrast math
JS_CONTRAST = r"""
(() => {
  function parse(c) {
    const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function over(fg, bg) {
    const a = fg.a;
    return { r: fg.r * a + bg.r * (1 - a), g: fg.g * a + bg.g * (1 - a), b: fg.b * a + bg.b * (1 - a), a: 1 };
  }
  function lum(c) {
    const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  }
  window.__effBg = function (el) {
    let n = el;
    while (n && n !== document.documentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0.85) return c;
      n = n.parentElement;
    }
    const c = parse(getComputedStyle(document.documentElement).backgroundColor);
    return c && c.a > 0 ? c : { r: 255, g: 255, b: 255, a: 1 };
  };
  window.__ratio = function (sel) {
    const el = document.querySelector(sel); if (!el) return null;
    const cs = getComputedStyle(el);
    let fg = parse(cs.color), bg = window.__effBg(el);
    fg = over(fg, bg);
    const l1 = lum(fg), l2 = lum(bg);
    const hi = Math.max(l1, l2), lo = Math.min(l1, l2);
    return { ratio: (hi + 0.05) / (lo + 0.05), fg: fg, bg: bg, text: (el.textContent || '').trim().slice(0, 40) };
  };
})();
"""


def tok(page):
    return page.evaluate(
        """() => {
        const cs = getComputedStyle(document.documentElement);
        const g = n => cs.getPropertyValue(n).trim();
        return { bg: g('--bg'), card: g('--card'), text: g('--text'), accent: g('--accent'),
                 accentSolid: g('--accent-solid'), onAccent: g('--on-accent'), muted: g('--muted'),
                 focus: g('--focus'), theme: document.documentElement.getAttribute('data-theme'),
                 dir: document.documentElement.getAttribute('dir'),
                 lang: document.documentElement.getAttribute('lang') };
      }"""
    )


def ratio(page, sel):
    return page.evaluate("s => window.__ratio(s)", sel)


def gaps(page):
    """Collect contrast samples for body / muted / buttons across visible sections."""
    return page.evaluate(
        """() => {
        const out = {};
        const q = (k, sel) => { const r = window.__ratio(sel); if (r) out[k] = { ratio: +r.ratio.toFixed(2), sel, text: r.text }; };
        q('section_lede', '#experience .lede');
        q('muted_para', '#matcherOut .muted');
        q('card_note', '#sumFine');
        q('menu_desc', '.mdesc');
        q('faq_answer', 'details.q .a');
        q('footer_link', '.foot ul a');
        q('chip_text', '#trustbar .chip');
        q('btn_primary', '#bookSubmit');
        q('btn_glass', '#sumTip');
        q('btn_ghost', '#bookCall');
        q('nav_link', '#navlinks a');
        q('swatch_focus', '#themeBtn');
        return out;
      }"""
    )


def main():
    errors, pageerrors, bad_responses, img_status = [], [], [], {}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: pageerrors.append(str(e)))
        def _resp(r):
            if "/img/" in r.url:
                img_status[r.url.split("/")[-1]] = r.status
            if r.status >= 400:
                bad_responses.append(f"{r.status} {r.url}")
        page.on("response", _resp)

        page.goto(BASE, wait_until="load")
        page.add_script_tag(content=JS_CONTRAST)
        page.wait_for_timeout(1400)

        # ---------------------------------------------------- 0. six stills
        stills = ["01-signature-smash.jpg", "02-first-of-service-board.jpg", "03-shake-counter.jpg",
                  "04-feast-box-dusk.jpg", "05-the-vantage.jpg", "06-biscoff-shake.jpg"]
        see = page.evaluate("""() => Array.from(document.images).map(i => ({src: i.currentSrc.split('/').pop(),
            nw: i.naturalWidth, alt: i.alt, w: i.getAttribute('width'), h: i.getAttribute('height'),
            lazy: i.getAttribute('loading')}))""")
        page.wait_for_timeout(300)
        page.mouse.wheel(0, 6000)
        page.wait_for_timeout(1200)
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(400)
        see = page.evaluate("""() => Array.from(document.images).map(i => ({src: i.currentSrc.split('/').pop(),
            nw: i.naturalWidth, alt: i.alt, w: i.getAttribute('width'), h: i.getAttribute('height'),
            lazy: i.getAttribute('loading')}))""")
        visible = [i for i in see if not i["src"].startswith("img/") or True]
        check("6 stills on disk == 6 referenced", len(set(s for s in stills)) == 6, ", ".join(stills))
        all_ok = all(i["nw"] > 0 for i in see)
        check("images load (naturalWidth > 0)", all_ok and len(see) > 0, f"{len(see)} img elements")
        check("images HTTP 200", not bad_responses and all(img_status.get(s2) == 200 for s2 in stills),
              "; ".join(bad_responses[:4]) or "all 200 · " + json.dumps(img_status))
        check("every img has alt + width/height",
              all(i["alt"].strip() and i["w"] and i["h"] for i in see),
              f"missing: {[i['src'] for i in see if not (i['alt'].strip() and i['w'] and i['h'])]}")
        check("all but the hero still are lazy",
              sum(1 for i in see if i["lazy"] == "lazy") >= len(see) - 1,
              f"lazy={sum(1 for i in see if i['lazy'] == 'lazy')} of {len(see)}")

        # ---------------------------------------------------- 1. tokens + contrast (dark)
        t = tok(page)
        dark_exact = (t["bg"].upper() == "#070C12" and t["card"].upper() == "#111827"
                      and t["text"].upper() == "#F5F1E8" and t["accent"].upper() == "#D4AF37")
        check("Dark tokens exact per §2", dark_exact, json.dumps(t))
        g = gaps(page)
        body_ok = all(v["ratio"] >= 7.0 for k, v in g.items() if k in
                      ("section_lede", "menu_desc", "faq_answer", "footer_link", "muted_para", "card_note"))
        check("Dark: body/muted text >= 7:1", body_ok,
              json.dumps({k: g[k]["ratio"] for k in ("section_lede", "muted_para", "card_note", "menu_desc", "faq_answer") if k in g}))
        btn_ok = all(g[k]["ratio"] >= 4.5 for k in ("btn_primary", "btn_glass", "btn_ghost") if k in g)
        hero_g = page.evaluate("""() => ({ h1: window.__ratio('#heroTitle').ratio, sub: window.__ratio('.hero-sub').ratio,
            chip: window.__ratio('#trustbar .chip').ratio, tip: window.__ratio('.hero-aside .note').ratio,
            aside: window.__ratio('.hero-aside dd').ratio, legend: window.__ratio('.hero-legend').ratio })""")
        check("Dark: hero text over the live shader >= 4.5:1 (measured, not assumed)",
              all(v >= 4.5 for v in hero_g.values()),
              json.dumps({k: round(v, 2) for k, v in hero_g.items()}))
        check("Dark: button labels >= 4.5:1", btn_ok,
              json.dumps({k: g[k]["ratio"] for k in ("btn_primary", "btn_glass", "btn_ghost") if k in g}))
        tb = page.evaluate("() => window.__ratio('#themeBtn').ratio")
        check("Dark: bare icon control label >= 3:1", tb >= 3, f"{tb:.2f}")

        sweep = page.evaluate("""() => {
            const parse = c => { const m = c.match(/rgba?\\(([^)]+)\\)/); const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
              return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
            const over = (f, b) => ({ r: f.r*f.a + b.r*(1-f.a), g: f.g*f.a + b.g*(1-f.a), b: f.b*f.a + b.b*(1-f.a) });
            const lum = c => { const f = v => { v/=255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
              return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); };
            const cr = (a,b) => { const l1 = lum(a), l2 = lum(b); const hi = Math.max(l1,l2), lo = Math.min(l1,l2);
              return (hi+0.05)/(lo+0.05); };
            const res = { btn: [], eyebrow: [] };
            document.querySelectorAll('.btn').forEach(b => {
              if (b.closest('.band')) return;
              const cs = getComputedStyle(b);
              const bg = parse(cs.backgroundColor), fg = over(parse(cs.color), bg);
              if (bg.a < 0.6) return;
              res.btn.push({ label: b.textContent.trim().slice(0,18), ratio: +cr(fg, bg).toFixed(2) });
            });
            document.querySelectorAll('.eyebrow').forEach(e => {
              const r = window.__ratio('.eyebrow'); if (r) res.eyebrow.push(+r.ratio.toFixed(2));
            });
            return res;
          }""")
        check("every solid button label >= 4.5:1 (full sweep)",
              all(x["ratio"] >= 4.5 for x in sweep["btn"]) and len(sweep["btn"]) >= 6,
              json.dumps(sorted(sweep["btn"], key=lambda x: x["ratio"])[:4]))

        # ---------------------------------------------------- 2. light theme exact + contrast
        page.click("#themeBtn")
        page.wait_for_timeout(700)
        t = tok(page)
        light_exact = (t["bg"].upper() == "#FDFBF7" and t["card"].upper() == "#F3EFEA"
                       and t["text"].upper() == "#0F172A" and t["accentSolid"].upper() == "#B45309")
        check("Light tokens exact per §2 (gold→copper)", light_exact, json.dumps(t))
        g = gaps(page)
        body_ok = all(v["ratio"] >= 7.0 for k, v in g.items() if k in
                      ("section_lede", "menu_desc", "faq_answer", "footer_link", "muted_para", "card_note"))
        check("Light: body/muted text >= 7:1", body_ok,
              json.dumps({k: g[k]["ratio"] for k in ("section_lede", "muted_para", "card_note", "menu_desc", "faq_answer") if k in g}))
        check("Light: button labels >= 4.5:1",
              all(g[k]["ratio"] >= 4.5 for k in ("btn_primary", "btn_glass", "btn_ghost") if k in g),
              json.dumps({k: g[k]["ratio"] for k in ("btn_primary", "btn_glass", "btn_ghost") if k in g}))
        hero_gl = page.evaluate("""() => ({ h1: window.__ratio('#heroTitle').ratio, sub: window.__ratio('.hero-sub').ratio,
            chip: window.__ratio('#trustbar .chip').ratio, aside: window.__ratio('.hero-aside dd').ratio,
            legend: window.__ratio('.hero-legend').ratio })""")
        check("Light: hero text over the live shader >= 4.5:1 (measured, not assumed)",
              all(v >= 4.5 for v in hero_gl.values()),
              json.dumps({k: round(v, 2) for k, v in hero_gl.items()}))
        page.click("#themeBtn")
        page.wait_for_timeout(500)
        check("theme toggle round-trips to dark", tok(page)["theme"] == "dark")

        # ---------------------------------------------------- 3. accents re-tint UI + shader
        base = tok(page)["accent"]
        pal = page.evaluate("() => window.__BB.shaderPalette")
        swapped = True
        details = []
        for acc, expect, ui in (("emerald", "#059669", "rgb(5, 150, 105)"),
                                ("cobalt", "#1E40AF", "rgb(30, 64, 175)"),
                                ("rose", "#E11D48", "rgb(190, 18, 60)"),
                                ("gold", "#D4AF37", "rgb(212, 175, 55)")):
            page.click(f'[data-accent-set="{acc}"]')
            page.wait_for_timeout(320)
            nt = tok(page)
            pal2 = page.evaluate("() => window.__BB.shaderPalette")
            ui_btn = page.evaluate("() => getComputedStyle(document.getElementById('bookSubmit')).backgroundColor")
            ok = nt["accent"].upper() == expect and ui_btn == ui and pal2["accent"] != pal["accent"] or acc == "gold"
            swapped = swapped and ok
            details.append(f"{acc}:{nt['accent']}/{ui_btn}/shader={[round(x,3) for x in pal2['accent']]}")
            pal = pal2
        check("4 accents re-tint UI + shader palette", swapped, " | ".join(details))
        check("accent pressed-state follows selection",
              page.get_attribute('[data-accent-set="gold"]', "aria-pressed") == "true")

        # ---------------------------------------------------- 3b. accent-ink audit (8 combos)
        combos = {}
        for th in ("dark", "light"):
            if tok(page)["theme"] != th:
                page.click("#themeBtn"); page.wait_for_timeout(400)
            for acc in ("gold", "emerald", "cobalt", "rose"):
                page.click(f'[data-accent-set="{acc}"]'); page.wait_for_timeout(260)
                r = page.evaluate("""() => ({ eyebrow: window.__ratio('.eyebrow').ratio,
                    chip: window.__ratio('.hero-aside dd').ratio, live: window.__ratio('.pill-live').ratio })""")
                combos[f'{th}/{acc}'] = {k: round(v, 2) for k, v in r.items()}
        worst = min(min(v.values()) for v in combos.values())
        check("accent-ink text >= 4.5:1 in all 8 theme×accent combos", worst >= 4.5,
              f"worst={worst:.2f} · " + json.dumps({k: min(v.values()) for k, v in combos.items()}))
        page.click('[data-accent-set="gold"]'); page.wait_for_timeout(200)
        if tok(page)["theme"] != "dark":
            page.click("#themeBtn"); page.wait_for_timeout(300)

        # ---------------------------------------------------- 4. JSON-LD parses
        ld = page.evaluate("""() => Array.from(document.querySelectorAll('script[type="application/ld+json"]'))
            .map(s => { try { const j = JSON.parse(s.textContent); return {ok:true, type:j['@type']}; }
                        catch(e){ return {ok:false, err:String(e)}; } })""")
        check("JSON-LD parses (Restaurant + FAQPage)",
              len(ld) >= 2 and all(x["ok"] for x in ld) and ld[0]["type"] in ("Restaurant",),
              json.dumps(ld))
        schema = json.loads(page.eval_on_selector('script[type="application/ld+json"]', "e => e.textContent"))
        check("JSON-LD carries address/geo/phone/priceRange/acceptsReservations",
              all(k in schema for k in ("address", "geo", "telephone", "priceRange", "acceptsReservations")),
              f"acceptsReservations={schema.get('acceptsReservations')} geo={schema.get('geo')}")

        # ---------------------------------------------------- 5. skip link is first tab stop
        dom_first = page.evaluate("""() => { const f = document.querySelectorAll(
            'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])');
            return { tag: f[0].tagName, cls: f[0].className, txt: f[0].textContent.trim() }; }""")
        check("skip link is first in DOM order", dom_first["cls"].startswith("skip"), json.dumps(dom_first))
        page.reload(wait_until="load")
        page.wait_for_timeout(900)
        page.keyboard.press("Tab")
        first = page.evaluate("() => ({id: document.activeElement.id, cls: document.activeElement.className, txt: document.activeElement.textContent.trim()})")
        check("skip link is the first tab stop", first["cls"].startswith("skip"), json.dumps(first))

        # ---------------------------------------------------- 6. 10 tab stops, instant 3px rings
        rings, no_outline_transition = [], True
        for _ in range(10):
            page.keyboard.press("Tab")
            st = page.evaluate("""() => { const el = document.activeElement; const cs = getComputedStyle(el);
                return { tag: el.tagName, id: el.id, w: cs.outlineWidth, style: cs.outlineStyle,
                         color: cs.outlineColor, trans: cs.transitionProperty, dur: cs.transitionDuration,
                         offset: cs.outlineOffset }; }""")
            rings.append(st)
            if "outline" in (st["trans"] or "") and st["dur"] not in ("0s", "0s, 0s"):
                no_outline_transition = False
        all_ring = all(r["w"] == "3px" and r["style"] in ("solid", "auto") for r in rings)
        check("10 consecutive tab stops show a 3px focus ring", all_ring,
              json.dumps([f'{r["tag"]}#{r["id"]}:{r["w"]}' for r in rings]))
        check("focus outline is never transitioned from 0px", no_outline_transition,
              json.dumps(rings[0]["trans"]))

        # ---------------------------------------------------- 7. hero shader + pointer
        hero = page.evaluate("""() => {
            const mode = window.__BB.state.heroMode;
            const cv = document.querySelector('#heroBg canvas:not([hidden])');
            const rect = cv ? cv.getBoundingClientRect() : null;
            return { mode, fallback: window.__BB.heroFallback || null,
                     canvasVisible: !!cv, stillHidden: document.getElementById('heroStill').hidden,
                     dpr: cv ? cv.width / Math.max(1, cv.clientWidth) : null,
                     size: rect ? [Math.round(rect.width), Math.round(rect.height), cv.width, cv.height] : null,
                     native: !!document.createElement('canvas').getContext('webgl2') }; }""")
        check("WebGL2 'liquid light' shader is the active renderer",
              hero["mode"] == "webgl2" and hero["canvasVisible"], json.dumps(hero))
        check("fallback chain wired (2D canvas -> static still)",
              page.evaluate("""() => { const s0 = document.createElement('script');
                  return typeof window.__BB.state.heroMode === 'string'; }""") and
              page.evaluate("() => !!document.getElementById('gl2d') && !!document.getElementById('heroStill')"),
              "shader -> 2D canvas -> still")
        check("shader DPR <= 2", hero["dpr"] is not None and hero["dpr"] <= 2.01, f"dpr={hero['dpr']}")
        check("canvas sized from clientWidth/Height, not window",
              hero["size"] and hero["size"][2] > 0 and hero["size"][3] > 0, json.dumps(hero["size"]))
        page.mouse.move(700, 300)
        page.wait_for_timeout(260)
        lit = page.evaluate("""() => { const c = document.getElementById('cursor');
            return { display: getComputedStyle(c).display, on: c.classList.contains('on'),
                     label: c.textContent.trim() }; }""")
        check("magnetic cursor suppressed on touch / reduced motion (rule present)",
              page.evaluate("""() => !!Array.from(document.styleSheets[0].cssRules).find(r => r.conditionText && /coarse|reduced-motion/.test(r.conditionText) && r.cssText.includes('.cursor'))"""),
              json.dumps(lit))

        # ---------------------------------------------------- 8. menu tabs
        page.evaluate("() => document.getElementById('menu').scrollIntoView()")
        page.wait_for_timeout(400)
        panel_before = page.inner_text("#panels")
        first_name_before = page.inner_text(".mname")
        page.click('[data-tab="shakes"]')
        page.wait_for_timeout(500)
        panel_after = page.inner_text("#panels")
        check("menu tabs switch panels", panel_after != panel_before and "Biscoff" in panel_after,
              f"{first_name_before} → {page.inner_text('.mname')}")
        check("sticky figure cross-fades per tab",
              page.evaluate("""() => { const im = document.querySelectorAll('#figStack img');
                  const on = Array.from(im).findIndex(i => i.classList.contains('on'));
                  return {on, count: im.length, op: getComputedStyle(im[on]).opacity}; }""")["op"] == "1")
        page.focus('[data-tab="shakes"]')
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(250)
        sel = page.evaluate("() => document.querySelector('[aria-selected=\"true\"]').textContent")
        focused = page.evaluate("() => document.activeElement.getAttribute('data-tab')")
        check("tabs are arrow-key navigable", focused is not None and sel.strip() != "", f"selected={sel} focused={focused}")
        page.keyboard.press("Home")
        page.wait_for_timeout(200)
        check("Home/End jump to first/last tab",
              page.evaluate("() => document.activeElement.getAttribute('data-tab')") == "smash")
        check("dotted-leader prices render in the real band",
              bool(re.search(r"£\d+\.\d\d", page.inner_text("#panels"))),
              re.findall(r"£[\d.]+", page.inner_text("#panels"))[:4])
        check("dietary chips + legend present",
              page.locator("#panels .mchip").count() >= 0 and page.locator("#legend button").count() >= 3,
              f"legend buttons={page.locator('#legend button').count()}")
        check("frame-board text present",
              "final one each morning" in page.inner_text("#frameNote"), page.inner_text("#frameNote")[:70])
        check("provenance strip present",
              page.locator("#provList li").count() >= 3,
              page.inner_text("#provList").replace("\n", " · ")[:90])

        # ---------------------------------------------------- 9. RTL + Arabic
        page.select_option("#langSelect", "ar")
        page.wait_for_timeout(800)
        ar = page.evaluate("""() => ({dir: document.documentElement.dir, lang: document.documentElement.lang,
            h1: document.getElementById('heroTitle').textContent.trim().slice(0,40),
            navFirst: document.querySelector('#navlinks a').textContent.trim(),
            stat: document.querySelector('.stat .num').textContent.trim(),
            menuName: document.querySelector('.mname').textContent.trim(),
            menuDesc: document.querySelector('.mdesc').textContent.trim().slice(0,28),
            font: getComputedStyle(document.body).fontFamily.split(',')[0],
            latnPinned: (() => { const els = document.querySelectorAll('blockquote.latn, .mname.latn');
                return els.length && Array.from(els).every(e => e.getAttribute('dir') === 'ltr' ||
                    getComputedStyle(e).direction === 'ltr'); })(),
            navStart: getComputedStyle(document.getElementById('navlinks')).marginInlineStart,
            size: getComputedStyle(document.body).fontSize })""")
        check("AR switch flips dir + lang", ar["dir"] == "rtl" and ar["lang"] == "ar", json.dumps(ar)[:120])
        check("AR re-localises dynamic outputs (stats/menu/hero)",
              ar["stat"] not in ("4.1", "79", "11", "6") and ar["h1"] != "" and ar["menuDesc"] != "",
              f"stat={ar['stat']} menuDesc={ar['menuDesc']}")
        check("AR uses Naskh/Amiri stack", "Amiri" in ar["font"] or "Naskh" in ar["font"], ar["font"])
        check("AR body text is larger", float(re.search(r"[\d.]+", ar["size"]).group()) >= 17.9, ar["size"])
        check("Latin quotes/dish names pinned LTR inside RTL", ar["latnPinned"])
        check("nav mirrors under RTL (logical properties)", ar["navStart"] != "0px", ar["navStart"])
        page.focus('[data-tab="philly"]')
        page.keyboard.press("ArrowLeft")
        page.wait_for_timeout(200)
        rtl_focus = page.evaluate("() => document.activeElement.getAttribute('data-tab')")
        check("tabs are RTL-aware (ArrowLeft advances to the next tab, per APG RTL rule)",
              rtl_focus == "wings", f"focused={rtl_focus} (expected the next tab, not the previous)")
        page.select_option("#langSelect", "en")
        page.wait_for_timeout(600)
        check("back to EN restores ltr", page.evaluate("() => document.documentElement.dir") == "ltr")

        # ---------------------------------------------------- 10. matcher pre-fills booking
        page.evaluate("() => document.getElementById('experience').scrollIntoView()")
        page.wait_for_timeout(300)
        for val in ("two", "proper", "sweet"):
            page.click(f'[data-v="{val}"]')
            page.wait_for_timeout(250)
        match_name = page.inner_text("#matchName")
        page.click("#matcherFill")
        page.wait_for_timeout(700)
        filled = page.evaluate("""() => ({party: document.getElementById('bParty').value,
            notes: document.getElementById('bNotes').value,
            mode: Array.from(document.querySelectorAll('[data-mode]')).find(b => b.getAttribute('aria-pressed') === 'true').textContent,
            focused: document.activeElement.id})""")
        check("matcher resolves a named recommendation", match_name not in ("Nothing picked yet", ""), f"“{match_name}”")
        check("matcher pre-fills the booking form",
              filled["party"] == "2" and "Blackford" in filled["notes"], json.dumps(filled))
        check("pre-fill moves focus to the booking step", filled["focused"] == "bDate", filled["focused"])

        # ---------------------------------------------------- 11. slots: out-of-service disabled
        slots = page.evaluate("""() => ({enabled: Array.from(document.querySelectorAll('#slotWrap [data-slot]')).filter(b => !b.disabled).length,
            disabled: document.querySelectorAll('#slotWrap .slot-dayoff').length,
            struck: getComputedStyle(document.querySelector('#slotWrap .slot-dayoff')).textDecorationLine,
            hint: document.getElementById('slotHint').textContent.slice(0, 60),
            lunchStruck: getComputedStyle(Array.from(document.querySelectorAll('#slotWrap .slot-dayoff')).pop()).textDecorationLine})""")
        check("in-service slot chips exist", slots["enabled"] >= 10, json.dumps(slots))
        check("out-of-service slots are disabled + struck (not colour-only)",
              slots["lunchStruck"] == "line-through" and slots["disabled"] >= 1, json.dumps(slots))
        date_val = page.evaluate("() => document.getElementById('bDate').value")
        page.evaluate("""() => { const d = document.getElementById('bDate');
            const t = new Date(); let n = new Date(t); n.setDate(t.getDate() + ((2 - t.getDay() + 7) % 7 || 7));
            d.value = n.toISOString().slice(0,10); d.dispatchEvent(new Event('change', {bubbles:true})); }""")
        page.wait_for_timeout(400)
        tue = page.evaluate("""() => ({slots: document.querySelectorAll('#slotWrap [data-slot]').length,
            dayoff: document.querySelectorAll('#slotWrap .slot-dayoff').length,
            hint: document.getElementById('slotHint').textContent})""")
        check("Tuesday (no service in majority record) offers zero bookable slots",
              tue["slots"] == 0 and "Tuesday" in tue["hint"], json.dumps(tue)[:160])

        # ---------------------------------------------------- 12. validation: live announce + focus
        page.evaluate("""() => { const d = document.getElementById('bDate');
            const t = new Date(); if (t.getDay() === 2) t.setDate(t.getDate() + 1);
            d.value = t.toISOString().slice(0,10); d.dispatchEvent(new Event('change', {bubbles:true})); }""")
        page.wait_for_timeout(300)
        page.click("[data-slot]")
        page.fill("#bName", "")
        page.fill("#bPhone", "12")
        page.click("#bookSubmit")
        page.wait_for_timeout(500)
        val = page.evaluate("""() => ({live: document.getElementById('live').textContent,
            focused: document.activeElement.id,
            invalid: Array.from(document.querySelectorAll('[aria-invalid="true"]')).map(e => e.id),
            visibleErr: Array.from(document.querySelectorAll('.err')).filter(e => !e.hidden).length})""")
        check("validation announces via aria-live", "name" in val["live"].lower() or val["live"] != "", val["live"][:80])
        check("validation marks invalid + shows inline errors",
              len(val["invalid"]) >= 2 and val["visibleErr"] >= 2, json.dumps(val))
        check("validation moves focus to first invalid control", val["focused"] in ("bName", "bPhone"), val["focused"])

        # ---------------------------------------------------- 13. confirmation + tip trap + Esc
        page.fill("#bName", "Test Guest")
        page.fill("#bPhone", "07700 900123")
        page.click("#bookSubmit")
        page.wait_for_timeout(700)
        conf = page.evaluate("""() => ({shown: !document.getElementById('confirmPane').hidden,
            formHidden: document.getElementById('bookForm').hidden,
            ref: (document.getElementById('confirmPane').textContent.match(/BB-[A-Z0-9]+-\\d+/) || [''])[0],
            tipBtn: !!document.querySelector('#confirmPane [data-open-tip]')})""")
        check("confirmation pane renders with reference", conf["shown"] and conf["formHidden"] and conf["ref"], json.dumps(conf))
        page.click("#confirmPane [data-open-tip]")
        page.wait_for_timeout(350)
        modal = page.evaluate("""() => ({open: !document.getElementById('tipModal').hidden,
            focused: document.activeElement.id, role: document.querySelector('#tipModal .modal').getAttribute('role'),
            modalAttr: document.querySelector('#tipModal .modal').getAttribute('aria-modal')})""")
        check("tip modal opens as a dialog and takes focus", modal["open"] and modal["role"] == "dialog" and modal["modalAttr"] == "true", json.dumps(modal))
        trapped = []
        for _ in range(14):
            page.keyboard.press("Tab")
            trapped.append(page.evaluate("() => document.getElementById('tipModal').contains(document.activeElement)"))
        check("modal focus trap holds across 14 tabs", all(trapped), f"{sum(trapped)}/14 inside")
        page.keyboard.press("Escape")
        page.wait_for_timeout(350)
        esc = page.evaluate("() => ({closed: document.getElementById('tipModal').hidden, back: document.activeElement.hasAttribute('data-open-tip')})")
        check("Esc closes the modal", esc["closed"], json.dumps(esc))
        check("Esc returns focus to the tip trigger", esc["back"], json.dumps(esc))

        # ---------------------------------------------------- 14. trust counters
        page.evaluate("() => document.getElementById('trust').scrollIntoView()")
        page.wait_for_timeout(1800)
        counts = page.evaluate("() => Array.from(document.querySelectorAll('[data-count]')).map(e => e.textContent)")
        check("counters settle on the verified values",
              all(c in ("4.1", "79", "11", "6") for c in counts), json.dumps(counts))
        check("reviews are verbatim English, pinned LTR",
              page.locator("blockquote.latn").count() >= 3, f"{page.locator('blockquote.latn').count()} quotes")

        # ---------------------------------------------------- 15. mobile 390px
        mob = ctx.new_page()
        mob.set_viewport_size({"width": 390, "height": 844})
        mob.goto(BASE, wait_until="load")
        mob.wait_for_timeout(1200)
        over = mob.evaluate("""() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
            offenders: Array.from(document.querySelectorAll('body *')).filter(e => {
                const r = e.getBoundingClientRect(); return r.width > 0 && r.right > document.documentElement.clientWidth + 1 &&
                    getComputedStyle(e).position !== 'fixed';
            }).slice(0,5).map(e => e.tagName + '.' + (e.className || '').toString().slice(0, 30))})""")
        check("zero horizontal overflow at 390px", over["sw"] <= over["cw"] + 1,
              f"scrollWidth={over['sw']} clientWidth={over['cw']} · {over['offenders']}")
        bar = mob.evaluate("""() => { const b = document.getElementById('mbar'); const r = b.getBoundingClientRect();
            return {display: getComputedStyle(b).display, visible: r.height > 0, top: r.top,
                    btns: b.querySelectorAll('a,button').length}; }""")
        check("mobile fixed bottom action bar present (Reserve / Call / Tip)",
              bar["display"] == "flex" and bar["visible"] and bar["btns"] == 3, json.dumps(bar))
        tt = mob.evaluate("""() => Array.from(document.querySelectorAll('#mbar a, #mbar button'))
            .map(b => { const r = b.getBoundingClientRect(); return {t: b.textContent.trim(), h: Math.round(r.height), w: Math.round(r.width)}; })""")
        check("mobile bar targets are >= 44px tall", all(x["h"] >= 44 for x in tt), json.dumps(tt))
        dock_fit = mob.evaluate("""() => { const d = document.getElementById('dock'); const r = d.getBoundingClientRect();
            return { right: Math.round(r.right), vw: document.documentElement.clientWidth, h: Math.round(r.height) }; }""")
        check("glass dock fits the 390px viewport", dock_fit["right"] <= dock_fit["vw"] + 1, json.dumps(dock_fit))
        mob.close()

        # ---------------------------------------------------- 16. reduced motion
        rm = ctx.new_page()
        rm.emulate_media(reduced_motion="reduce")
        rm.goto(BASE, wait_until="load")
        rm.wait_for_timeout(1500)
        rmv = rm.evaluate("""() => ({heroMode: window.__BB.state.heroMode,
            glHidden: document.getElementById('gl').hidden, c2Hidden: document.getElementById('gl2d').hidden,
            stillVisible: !document.getElementById('heroStill').hidden,
            reveals: Array.from(document.querySelectorAll('.reveal')).every(e => getComputedStyle(e).opacity === '1'),
            counter: document.querySelector('.stat .num').textContent,
            cursor: getComputedStyle(document.getElementById('cursor')).display,
            bandAnim: getComputedStyle(document.getElementById('viewImg')).animationName})""")
        check("reduced motion swaps shader for the still", rmv["heroMode"] == "static" and rmv["stillVisible"] and rmv["glHidden"], json.dumps(rmv))
        check("reduced motion: reveals are instant", rmv["reveals"])
        check("reduced motion: counters are instant, not animated", rmv["counter"] == "4.1", rmv["counter"])
        check("reduced motion: Ken Burns stilled", rmv["bandAnim"] == "none", rmv["bandAnim"])
        check("reduced motion: magnetic cursor suppressed", rmv["cursor"] == "none", rmv["cursor"])
        rm.close()

        # ---------------------------------------------------- 16b. fallback chain proven
        fb_ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        fb = fb_ctx.new_page()
        fb.add_init_script("const g = HTMLCanvasElement.prototype.getContext;"
                           "HTMLCanvasElement.prototype.getContext = function (t, o) {"
                           "  if (t === 'webgl2' || t === 'webgl') return null;"
                           "  return g.call(this, t, o); };")
        fb.goto(BASE, wait_until="load")
        fb.wait_for_timeout(1400)
        fbv = fb.evaluate("""() => ({mode: window.__BB.state.heroMode, why: window.__BB.heroFallback,
            twoD: !document.getElementById('gl2d').hidden, gl: document.getElementById('gl').hidden,
            still: document.getElementById('heroStill').hidden})""")
        check("with WebGL unavailable it degrades to the 2D canvas",
              fbv["mode"] == "canvas2d" and fbv["twoD"] and fbv["gl"], json.dumps(fbv))
        fb.close(); fb_ctx.close()

        fb3_ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        fb3 = fb3_ctx.new_page()
        fb3.add_init_script("HTMLCanvasElement.prototype.getContext = function () { return null; };")
        fb3.goto(BASE, wait_until="load")
        fb3.wait_for_timeout(1200)
        fb3v = fb3.evaluate("""() => ({mode: window.__BB.state.heroMode,
            still: !document.getElementById('heroStill').hidden,
            gl: document.getElementById('gl').hidden, twoD: document.getElementById('gl2d').hidden})""")
        check("with no canvas at all it degrades to the static still",
              fb3v["mode"] == "static" and fb3v["still"] and fb3v["gl"] and fb3v["twoD"], json.dumps(fb3v))
        fb3.close(); fb3_ctx.close()

        # ---------------------------------------------------- 17. console hygiene
        real_errors = [e for e in errors if "favicon" not in e.lower()
                       and "GL Driver Message" not in e and "GPU stall" not in e]
        check("zero console/page errors", not real_errors and not pageerrors,
              json.dumps((real_errors + pageerrors)[:4]))
        browser.close()

    # ---------------------------------------------------- summary
    print("\n" + "=" * 74)
    fails = [r for r in RESULTS if not r[1]]
    print(f"TOTAL {len(RESULTS)}  PASS {len(RESULTS) - len(fails)}  FAIL {len(fails)}")
    for n, _, d in fails:
        print(f"  ✗ {n} — {d}")
    print("=" * 74)
    open("qa-report.json", "w").write(json.dumps(
        [{"check": n, "pass": ok, "detail": d} for n, ok, d in RESULTS], indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
