# Bonnie Burgers حلال — Prototype & Production Plan

A dependency-free, single-file working prototype of the proposed experience for **Bonnie Burgers حلال**,
61 Mayfield Road, Blackford, Edinburgh EH9 3AA — plus the QA harness that proves it, and the production
port map for the Next.js 14 build.

> **Grounding rule observed throughout:** every public fact used here is cited in the pitch appendix
> (`PITCH-Bonnie-Burgers.md`). Anything we could not verify is labelled **PLACEHOLDER** on the page itself —
> including the hours, which genuinely conflict across five public sources. Nothing about the venue was invented.

---

## 1. Run it

The prototype is one file plus six stills. No build step, no dependencies, no network calls.

```bash
# recommended — any static server
python3 -m http.server 8137 --bind 0.0.0.0
# then open http://localhost:8137/index.html
```

Also works by double-clicking `index.html` (nothing is fetched over the network except the six local images).

```
index.html                 single-file prototype (markup + tokens + i18n + WebGL + booking logic)
img/                       exactly six generated stills (see §7 register below)
qa.py                      headless-browser QA harness (Playwright/Chromium)
qa-report.json             machine-readable result of the last run
docs/app.js                the prototype's JS module, extracted verbatim — for lifting into components
docs/SHOT-LIST.md          what each of the six stills shows, and its honesty constraint
screens/                   screenshots captured during the visual QA pass
```

### QA harness

```bash
pip install playwright && python3 -m playwright install chromium
python3 qa.py                       # against http://127.0.0.1:8137/index.html
python3 qa.py http://host/page.html # or any URL
```

**Current result: 74 checks, 74 pass, 0 fail** (`qa-report.json`). It measures rather than assumes:
contrast is computed from live computed styles with alpha compositing, the shader is asserted to be the
*active* renderer, and the fallback chain is proven by disabling WebGL and then canvas entirely in
sandboxed browser contexts.

---

## 2. What the prototype actually implements

| Area | Implemented |
|---|---|
| **Theme engine** | Dark (`#070C12` / `#111827` / `#D4AF37` / `#F5F1E8`) and Light (`#FDFBF7` / `#F3EFEA` / `#0F172A` / `#B45309`). Toggle in the nav dock; persisted on-device. |
| **Accent engine** | 4 swatches — Executive Gold, Emerald, Royal Cobalt, Velvet Rose — re-tinting buttons, links, borders, glows, focus rings, card hovers **and the shader palette**, via CSS custom properties (`--accent`, `--accent-ink`, `--accent-solid`, `--on-accent`, `--accent-soft`, `--glow`). |
| **i18n / RTL** | Full English + full Arabic. Browser auto-detect, on-device persistence, `dir="rtl"` on `<html>`, logical properties throughout, mirrored directional icons, RTL-aware tab arrow keys, Latin quotes and dish names pinned `lang="en" dir="ltr"`, Arabic in a Naskh/Amiri stack at ~1.12× size. Six further locales are staged in the switcher as disabled rows (production ships 100+). |
| **WebGL2 hero** | "Liquid light": fBm-warped filaments + liquid sheet, sparse starfield, pointer glow. DPR capped at 2, paused off-screen and on tab-hide, `prefers-reduced-motion` collapses to a single still. Fallback chain **WebGL2 → 2D canvas → static still**, including a `webglcontextlost` handler. |
| **Motion** | 0.9 s reveals staggered at 90 ms; tilt cards ≤ 9°; Ken Burns on the view band; magnetic labelled cursor (disabled on touch, suppressed under reduced motion). |
| **Booking portal** | Two-step, no card. Date / party / service mode / time chips → dietary, occasion, access needs, notes. Live summary that updates as you type. Smart defaults remembered on-device. Time slots are **disabled-by-design** (struck through + explained) outside the published service window, and Tuesday is closed by guard. Validation announces via `aria-live` and moves focus to the first invalid control. |
| **Menu board** | Five tabs derived from what the kitchen actually cooks, accessible `role="tablist"` with arrow/Home/End keys and RTL-aware direction, dotted-leader prices from the published band, V/VG/GF dietary chips filtered from the legend straight into the booking form, sticky cross-fading figure, provenance strip, honest frame-board line. |
| **Crowd routes** | 9+ routes (no private room exists — stated plainly), each pre-filling the booking. |
| **Trust wall** | Counters built from verified facts only (4.1 ★, 79 reviews, 11 wing finishes, 6 service days), six verbatim reviews **including the critical one**, and a candid headline about the honest review count. |
| **Tip** | "Thank the team" in five placements (hero micro-line, summary, confirmation, final CTA, mobile bar). Modal with a real focus trap and Esc-restores-focus. Production path is PayPal Orders v2 server-side; the prototype simulates and says so. |
| **SEO** | `Restaurant` JSON-LD (address, geo, phone, priceRange, `acceptsReservations`, opening hours) + `FAQPage` JSON-LD for the six objections. |
| **Mobile** | Fixed bottom action bar (Reserve / Call / Tip), zero horizontal overflow at 390 px, targets ≥ 44 px, dock reflows to full width. |

### Hard-won engineering rules obeyed (and checked)

- Focus rings are **never** transitioned from `0px`; `:focus-visible` sets an instant 3 px ring plus a halo.
- Only named properties are transitioned. `outline` is never animated.
- `[hidden]{display:none !important}` is declared, so inline-styled elements hide correctly.
- Shared boot state (`window.__BB_BOOT`) is defined **before** any module reads it — no TDZ crashes.
- No node we hold a reference to is replaced via `outerHTML`; only `innerHTML` swaps.
- Canvases are sized from `clientWidth`/`clientHeight` at init **and** by a `ResizeObserver`, not just on `window.resize`.
- Shader compile/link failures log loudly to the console instead of silently degrading (this caught a real bug).

---

## 3. Measured contrast (not assumed)

Values are computed in the harness from live computed styles, compositing alpha against the real backdrop.

| Pair | Theme | Measured |
|---|---|---|
| Body text on background | dark / light | **17.41 : 1** / **17.27 : 1** |
| Muted text on card | dark / light | **8.12 : 1** / **8.49 : 1** |
| Hero H1 over the live shader | dark / light | **17.41 : 1** / **17.27 : 1** |
| Hero sub-headline over the shader | dark / light | **8.98 : 1** / **9.40 : 1** |
| Primary button label | dark / light | **9.20 : 1** / **5.02 : 1** |
| Glass button label | dark / light | **15.74 : 1** / **15.60 : 1** |
| Accent ink (eyebrows, chips) — worst of 8 theme × accent combos | all | **5.31 : 1** (light/emerald); gold light = **7.97 : 1** |
| Focus ring (`--accent-ink`) vs card surface | worst combo | **≥ 4.4 : 1** (bar is 3 : 1) |

Targets: body ≥ 7 : 1 · button labels ≥ 4.5 : 1 · muted ≥ 4.5 : 1 · focus ring ≥ 3 : 1. All green.
One value was amber during development — light-theme gold ink measured **4.42 : 1** on the sand card — and was
re-tuned to `#664A08` (**7.20 : 1**) rather than argued about.

---

## 4. Production port map — Next.js 14 / Tailwind / Framer Motion

The prototype mirrors the production UI logic one-for-one; below is how it maps and what listens where.

### Route & component map

| Prototype | Production |
|---|---|
| inline `STR` object | `i18n/{en,ar,...}.json` + `next-intl` (100+ locales), `middleware.ts` for locale detection/redirect |
| inline `DATA` | `/data/menu.ts`, `/data/venue.ts`, `/data/reviews.ts` (typed, CMS-synced) |
| `renderTabs/renderPanels` | `components/MenuBoard.tsx` (server component; tab state in a small client island) |
| hero `<canvas>` + shader source | `components/HeroLiquidLight.tsx` (`"use client"`, dynamic import, `ssr:false`, IntersectionObserver pause) |
| `renderExperience` + matcher | `components/Experience.tsx`, `components/Matcher.tsx` (Framer Motion stagger 0.09 s, tilt transformed in a rAF loop) |
| booking form + `onSubmit` | `components/BookingPortal.tsx` → `POST /api/reserve` |
| tip modal | `components/TipDialog.tsx` → `POST /api/tip` then `/api/tip/capture` |
| `--accent*` custom properties | `tailwind.config.ts` token map: `colors.accent.{DEFAULT,ink,solid,soft,glow}` bound to CSS vars; theme switched by a `data-theme` attribute on `<html>` |
| focus ring styles | one `:focus-visible` utility in `globals.css`, imported before any component CSS |

### Services and ports

| Service | Dev | Prod | Notes |
|---|---|---|---|
| Web app (Next.js 14, App Router) | `3000` | `443` (TLS at the edge) | single origin; browser calls **relative** URLs only |
| Static assets / stills | served by Next | CDN | `next/image`, AVIF/WebP, `sizes` set, LCP image preloaded |
| `POST /api/reserve` | `3000` | `443` | server-side validation mirroring the client, idempotency key, SMS/email confirmation |
| `POST /api/tip` → PayPal **Orders v2** create | `3000` | `443` | returns `approve` link; **no card data ever touches us** |
| `POST /api/tip/capture` | `3000` | `443` | capture on approval return; writes the tip to the shift ledger |
| `POST /api/paypal/webhook` | `3000` | `443` | signature-verified reconciliation |
| `GET /api/hours` | `3000` | `443` | **the single source of truth** for the hours problem; cached, `revalidate: 300` |
| Menu data revalidation | — | ISR | `revalidate: 3600`, on-demand tag purge when the kitchen rewrites the board |
| Google Place / FSA sync | — | cron worker | nightly rating + review count refresh so the trust wall never goes stale |

No cross-service `localhost` calls are made from the browser: the web app proxies every backend interaction
through its own route handlers, so the same build runs on `localhost:3000`, a preview URL, or production.

### Environment

```
NEXT_PUBLIC_SITE_URL        canonical origin
PAYPAL_CLIENT_ID            Orders v2 (server-only)
PAYPAL_CLIENT_SECRET
PAYPAL_ENV                  sandbox | live
PLACE_ID / FSA_BUSINESS_ID  rating + review-count sync
SMS_PROVIDER_KEY            reservation confirmations
```

### Performance budget

LCP < 2.5 s · INP < 200 ms · CLS < 0.1 · shader DPR ≤ 2 and paused off-screen · hero still preloaded,
all other stills `loading="lazy"` with intrinsic `width`/`height` · zero third-party scripts above the fold.

---

## 5. The six stills (§7 register)

Generated editorial hospitality photography; soft window light, muted midnight/linen palette with
champagne-gold highlights, shallow depth of field, no text, no watermarks, no people.

| File | Subject | Honesty constraint |
|---|---|---|
| `01-signature-smash.jpg` | Signature plate — smashed patty, cheese, house sauce | Matches the board's "Bonnie Smash" description |
| `02-first-of-service-board.jpg` | Wings, onion rings, fries, two shakes | **No people** — a takeaway counter, not a dining-room scene |
| `03-shake-counter.jpg` | Counter shelf — shakes and chilled bottles | No branded appliance or packaging (verified: no lettering) |
| `04-feast-box-dusk.jpg` | The crowd spread — subs, loaded fries, tenders | Delivery boxes, because that is how most of it leaves |
| `05-the-vantage.jpg` | **THE VANTAGE** — Blackford-rooftops view toward Arthur's Seat and the Salisbury Crags | **No Calton Hill monuments, no castle on the skyline** — an earlier render put the wrong landmarks in frame and was rejected; only what is genuinely visible from up there is shown |
| `06-biscoff-shake.jpg` | Biscoff shake, dessert close | The shake reviewers actually mention |

First image is `fetchpriority="high"`; every other image is lazy with real alt text and explicit dimensions.

---

## 6. Still open (PLACEHOLDER — needs the client)

1. **Real opening hours.** The public record disagrees five ways; the prototype uses the majority record
   (evening service ~17:10–21:50, Tuesday closed) and disables what it cannot verify.
2. **Dine-in seating.** The FSA register classifies the business as *Takeaway/sandwich shop*. "Eat in" is
   offered but annotated as unconfirmed.
3. **Named local suppliers** for the provenance strip.
4. **Crowd tray prices and lead times** (current figures are built from the published board).
5. **Gift vouchers** — a new capability, not an existing product.
6. **Accessibility details** — require a site visit.
7. **Final cancellation/deposit policy** for crowd orders.
8. **Six further locales** staged in the switcher; production ships 100+.
