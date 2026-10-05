# Bonnie Burgers حلال — Digital Experience Pitch

**Venue** Bonnie Burgers حلال · 61 Mayfield Road, Blackford, Edinburgh EH9 3AA
**Category** Halal smash burgers, Philly cheesesteaks, wings, loaded fries & shakes (public register: *takeaway/sandwich shop*)
**Deliverable** Single-file working prototype (`index.html`) + six generated stills + this pitch
**Verified at time of writing** 4.1 ★ from 79 Google reviews · evening kitchen from ~17:10 · Tuesday closed
**Prepared** October 2026 · every non-verified claim is marked **PLACEHOLDER** and listed in the appendix

> **Grounding note.** The pin resolved to a real venue with a real, addressable digital problem. Nothing on the
> property was invented: the vantage line, the neighbourhood framing, the dish names, the prices, the review
> quotes and the hours conflict are all traceable to public sources listed in the appendix. Where the public
> record disagrees — and it does, five ways, on opening hours — this pitch says so out loud rather than picking
> a number that flatters the design.

---

## 1. Brand Diagnosis (What They Are + What's Not Working)

**What they are.** A genuinely well-liked halal smash-burger kitchen on Mayfield Road, in the Blackford /
Mayfield pocket of south Edinburgh, five minutes from the King's Buildings and nine minutes below the summit
of Blackford Hill and the Royal Observatory. It cooks everything to order, it is not on any tourist route, and
its regulars are students, hospital and university staff, and south-side families. Its food reputation is real:
4.1 ★ across 79 reviews, with *"friendly staff"* mentioned 21 times, *"milkshakes"* 8, *"cheese steak"* 3 and
*"smash burger"* 2 in the review keyword cloud. Its delivery partners rate it higher still (Deliveroo 4.4 from 72).

**What is not working.** The venue is stronger than its digital footprint in four specific, fixable ways.

### Weakness 1 — Five public sources disagree about the opening hours

- **What's wrong.** The public record is genuinely contradictory. The FSA register and Just Eat both list
  `17:10–21:50, Sunday–Monday and Wednesday–Saturday`; Uber Eats lists `17:15–21:45` on the same days;
  Mapcarta/OpenStreetMap lists `16:00–22:30`; and the venue's own website lists `12pm–10pm Monday to Friday`
  and `5pm–10pm Saturday and Sunday` — i.e. it advertises **weekday lunchtimes and a Tuesday service** that
  three other sources say do not exist. Google's place page currently tells a searcher *"Closed · Opens 5 PM Wed"*.
  Whichever version is true, the customer cannot know it, and the venue cannot be found by the hours it
  actually keeps.
- **Why it hurts bookings.** Someone walks up at 12:40 on a Wednesday because the website said 12pm. The shutter
  is down. That customer does not check the site again — they check Deliveroo next time. Tuesday is worse: the
  site implies service, three aggregators say otherwise, and a family that drives over on a Tuesday posts the
  review that starts *"I'd check before you go"*. This single ambiguity leaks covers every week and cannot be
  fixed by better design alone.
- **The change.** One machine-readable source of truth (`GET /api/hours`, ISR-cached, edited by the kitchen),
  surfaced as: a hero-side facts panel that states the service window and the day off; **booking time chips that
  are disabled by design and struck through** with a plain-language reason; a footer that prints the conflict
  and the phone number rather than hiding it; `openingHoursSpecification` in the Restaurant schema; and a
  one-page corrections push to Google Business Profile, the FSA record and all three aggregators on day one.
  The prototype demonstrates exactly this: 27 bookable evening slots, a struck-out daytime row, and **zero
  bookable Tuesday slots**.

### Weakness 2 — Booking is phone-only, and the only digital path is a third party's

- **What's wrong.** There is no owned reservation or ordering flow anywhere. The site's two calls to action are
  *SEE OUR MENU* (a PDF hosted in the WordPress uploads folder) and *ORDER ONLINE*, which hands the customer to
  `bonnieburgersonline.co.uk` — the website vendor's ordering subdomain. Group enquiries are routed to a phone
  number ("*want to order for a party… call on the number below*") with no form, no sizes, no lead time, no
  record. There is no booking engine, no deposit logic, no confirmation trail and no customer data.
- **Why it hurts bookings.** Every digital order pays commission and arrives without a name attached, so the
  venue cannot market to its own regulars, cannot fill a quiet Wednesday, and cannot up-sell the tray orders
  that carry the best margin per minute of kitchen time. Group business — birthdays, society nights, Friday
  offices from the King's Buildings — is exactly the revenue a phone-only policy quietly turns away, because the
  organiser has to *call during service* to plan something three weeks out.
- **The change.** A twenty-second, no-card booking portal that ends in a held slot and a reference; a live
  summary; on-device memory of party size, service and dietary notes; and **nine crowd routes** (match-day feed,
  office Friday drop, birthday table, society night, graduation day and so on) that pre-fill the form in one tap.
  Phone becomes the warm fallback, not the only door — dial-pad and *"or call the counter"* sit beside every step.

### Weakness 3 — The menu is a PDF, so search engines and assistants cannot read it

- **What's wrong.** The full menu — every dish, every price, every dietary mark — exists only as a
  multi-page PDF (`LCP39213-Bonnie-Burgers-1.pdf`) plus two flattened JPEG images of the same artwork.
  There is no HTML menu, no dietary marking on the page, no allergen path, and no structured data. What *is*
  in the page source is worse: a JSON-LD block describing the site not as Bonnie Burgers but as
  **"Low Cost Menus"**, the template vendor, whose name also carries the footer copyright.
- **Why it hurts bookings.** Nobody can be found for *"halal burger Edinburgh"*, *"gluten free takeaway
  Edinburgh"* or *"smash burger near King's Buildings"* if the words and prices live inside an image and a PDF.
  Google cannot surface a menu it cannot parse; voice assistants read the wrong business name; allergy-sensitive
  customers — a halal-adjacent audience that shops carefully — get nothing to hold on to and go elsewhere. In a
  category where a competitor with a proper HTML menu wins the local pack on relevance alone, this is the
  cheapest lost traffic in the whole estate.
- **The change.** A real HTML menu board: five tabs (smash burgers / Philly & wraps / wings & loaded fries /
  shakes & sides / feeds a crowd), **dotted-leader prices taken from the published band** (£1.00–£12.50),
  V/VG/GF dietary chips whose legend cross-links straight into the booking form's dietary step, a sticky
  cross-fading figure, the honest frame-board line *"Indicative — the kitchen writes the final one each
  morning,"* and a provenance strip. Behind it, `Restaurant` + `Menu` + `FAQPage` structured data with the
  correct business identity, geo, phone, price range and `acceptsReservations`.

### Weakness 4 — Tiny, unamplified proof, hidden behind a generic above-the-fold

- **What's wrong.** The evidence is strong and completely unused. The hero says *"Delicious, freshly cooked
  food"* over an AI-looking burger shot, with *"20% off your first order"* as the loudest element on the page.
  The rating never appears as a number; the 79 reviews never appear as quotes; the halal claim — which is in the
  **business name itself** (Bonnie Burgers حلال) and in the Facebook bio — appears nowhere in the site's copy.
  And the single most cinematic asset within walking distance is never mentioned: the nine-minute climb from
  the counter to the top of Blackford Hill, where the rooftops below open onto Arthur's Seat and the
  Salisbury Crags. The property page therefore shows a *marque* only, not a *place*.
- **Why it hurts bookings.** A 4.1 is an honest score that needs context — reviewers whose complaint is a
  delayed Just Eat delivery are scoring the courier, not the smash patty — but a page that never shows the
  number cannot frame it. Meanwhile the halal audience, the student audience and the visitor audience are all
  being asked to trust a hero line any burger shop in Britain could have used. There is no reason on the page
  to choose tonight over any other night, and no reason to choose *this* counter over the one two streets on.
- **The change.** Lead with the honest number and the verified facts: a trust bar of chips (4.1 ★ · 79 reviews ·
  halal kitchen · 61 Mayfield Road · hours under verification), a right-rail *Checked against the public record*
  panel, a trust wall with counter-animated verified figures (4.1 / 79 / 11 wing finishes / 6 service days), six
  **verbatim** review cards — *including the critical one*, because a page that keeps the bad review is a page
  telling the truth — and a candid headline that reads *"Seventy-nine reviews. We would rather earn the eightieth
  than buy one."* Then give the place its cinematic moment: a full-bleed **Vantage** band with a location-true
  line, *"Walk nine minutes up from the counter and the whole city falls away north."*

---

## 2. Luxury Pivot Strategy (How We Upgrade Perception + Conversions)

The move is not to pretend a takeaway counter is a hotel restaurant. It is to treat a **fast-food kitchen with
a real local reputation as a place with provenance** — and to let the honesty do the luxury work, because
honesty is the one luxury a chain cannot copy.

1. **Make the evening an occasion without inventing a room.** The site says out loud that there is no private
   dining room. What it sells instead is the *feast*: boxes opened on a dark table at dusk, nine crowd routes,
   trays built for ten to forty. Luxury here reads as *confidence*, not velvet.
2. **Put the sunset on the poster.** Blackford Hill, the Royal Observatory, Arthur's Seat and the Salisbury
   Crags are the venue's free, unrivalled asset. The Vantage band turns a suburban counter into a vantage point
   — and gives visitors a reason to eat before or after the climb.
3. **Lead with the honest number.** Trust bar, counters and candid headline. A 4.1 stated plainly converts
   better than a 4.1 hidden, and it is the only rating claim this kitchen can defend in a court of public reviews.
4. **Give the halal claim its due, in the site's own voice.** It is in the business name; it belongs in the
   hero chips, the FAQ and the structured data, so the audience searching for it can actually confirm it.
5. **Own the ordering relationship.** Twenty seconds to a held slot, on-device memory, crowd routes that
   pre-fill themselves, and a tip that goes to the floor team. The aggregators stay for reach; the site becomes
   the place regulars come back to.
6. **Price the experience in restraint.** Editorial stills, a champagne-gold accent chosen by the guest,
   dark/light per time of day, and a two-colour, ten-words-to-a-line discipline. Perception is set in the first
   1,400 pixels and defended in the details.

**Conversion mechanics, stated plainly:** fewer steps to a held slot (2 steps, 0 cards); no dead ends (every
disabled slot explains itself and offers the phone); no unanswered objection (six FAQs match the six things
people actually ask); no wasted trust (a tip that is optional and visibly goes to the team); and no hidden
prices (the real band, published).

---

## 3. Landing Page IA (Section-by-Section Blueprint)

Each section below is implemented in `index.html`; the two-column reading is **purpose → layout / headline
direction / CTAs**.

### A · HERO — *"The smash burger south Edinburgh actually queues for."*
- **Purpose.** Position the counter as the premier choice in the entered location (Mayfield / Blackford / south
  Edinburgh) in one breath, and prove it with verified facts in the same viewport.
- **Layout.** Full-height WebGL2 "liquid light" field behind a directional scrim; copy left (locked RTL
  container in Arabic), a **glass facts panel** right on ≥1180 px carrying the four verifiable numbers:
  4.1 ★ · 79 · kitchen service 17:10–21:50 · no Tuesday service · ≈ 9 minutes to Blackford Hill. Trust-bar chips
  along the foot of the hero, then the tip micro-line.
- **CTAs.** **Reserve a table** (primary) · **Explore the menu** (glass secondary) · phone as a quiet text link.
- **Tip micro-CTA.** *"Entirely optional, never expected — every penny of a tip goes to the floor team."*

### B · EXPERIENCE — *"Smashed, stacked, fried — and made to order."*
- **Purpose.** Turn four dishes into four reasons, then hand the guest a recommendation.
- **Layout.** Four tilt cards (≤ 9°, pointer-fine only) from the real board — the signature smash, wings with
  their eleven finishes, the Philly counter, the shakes reviewers keep photographing. Each carries a real price
  range chip. Below it, a **3-question Matcher** (who's eating / how hungry / heat or sweet) with a progress bar
  and a live result panel that names the order — *The Mayfield Straight*, *The Blackford Double*, *The
  Observatory Tower* — and its £ items.
- **CTAs.** **Carry this into my booking** → pre-fills party size, service mode and notes, then moves focus to
  the date field. *"Plan this route"* on each route card does the equivalent for groups.

### B2 · SECTOR MENU BOARD — *"What the counter is running today."*
- **Purpose.** Make the menu readable by humans, search engines and screen readers — the thing a PDF can never be.
- **Layout.** Five tabs derived from the sectors this kitchen actually cooks: **Smash burgers / Philly & wraps /
  Wings & loaded fries / Shakes & sides / Feeds a crowd.** Accessible `role="tablist"` — arrows, Home/End,
  RTL-aware direction. Dotted-leader prices in the published band. V/VG/GF chips with a legend that filters the
  board *and* cross-links into the booking form's dietary step. A **sticky photography figure** cross-fades per
  tab. A provenance strip ("Within the mile": King's Buildings ≈ 0.5 km, Hermitage of Braid ≈ 0.6 km, Blackford
  Hill & the Royal Observatory ≈ 0.9 km, Newington & Cameron Toll ≈ 1.2 km).
- **Frame-board text (restaurant variant).** *"Indicative — the kitchen writes the final one each morning."*
- **Seasonal ribbon.** **Omitted deliberately** — no verified seasonal offer exists, and inventing one would
  undermine the honesty the rest of the page is trading on.
- **CTAs.** Dietary chip → booking; each panel foot → *Reserve* / *Call the counter*.

### C · VIEW BAND — *"Walk nine minutes up from the counter and the whole city falls away north."*
- **Purpose.** Give the venue a place, not just a product, using only what is genuinely visible from up there.
- **Layout.** Full-bleed still of the Blackford-rooftops view toward Arthur's Seat and the Salisbury Crags at
  golden hour, slow Ken Burns (statically stilled under reduced motion), a bottom-up scrim for AA text, one
  location-true line of copy naming the real geography: Observatory Road, the Hermitage of Braid, Blackford Hill.
  No Calton Hill monuments, no castle skyline — an earlier render put them in frame and was rejected as untrue.
- **CTAs.** **Reserve a table** · **Gift voucher**.

### D · BOOKING PORTAL — *"Twenty seconds, no card."*
- **Purpose.** Remove every reason not to hold a slot.
- **Layout.** Left: **Step 1 — the slot** (date, party size, how you're eating, time chips) and **Step 2 —
  anything we should know** (name, mobile, dietary, celebration, access needs, crowd route, notes). Right:
  a **sticky live summary** that updates as you type. Time chips outside the published window are **disabled
  by design** — struck through, described in text, never colour-only — and Tuesday is closed by guard, with the
  reason printed underneath. Smart defaults are remembered on-device.
- **Confirmation.** A reference (e.g. `BB-D4F0-5`), the held slot restated, and **"Thank the team"** as a
  first-class action beside *Call* and *Change something*.
- **9+ crowd routes.** Match-day feed, office Friday drop, birthday table, society night, move-in feed,
  post-hill supper, kids' party box, graduation day, late film-night platter. Each fills party size, mode and
  notes in one tap. **No private room is claimed**; the section says so in the headline.
- **CTAs.** **Confirm my slot** · **Or call the counter** (warm fallback, `+44 131 374 4464`) · *Start again*.

### E · TRUST WALL — *"Seventy-nine reviews. We would rather earn the eightieth than buy one."*
- **Purpose.** Convert scepticism with numbers a reader can check.
- **Layout.** Four animated counters from verified facts only (4.1 ★ · 79 reviews · 11 wing finishes · 6 service
  days; counters settle instantly under reduced motion), then six review cards — **verbatim**, attributed, Latin
  text pinned LTR inside the Arabic layout, and the criticism kept in: *"Portions are a little smaller than
  competitors, but still filling enough."*
- **CTAs.** *Reserve* · *Read the reviews on Google*.

### F · FAQ + FINAL CTA — *"Answered before you call."*
- **Purpose.** Kill the last six objections, then close.
- **Layout.** Six `<details>` objections with clear answers: **(1)** membership/permission, **(2)** real
  hours/availability, **(3)** dietary needs and children, **(4)** private functions, **(5)** parking and walk
  distance, **(6)** cancellation. Then the final CTA card (Reserve / Gift voucher / Thank the team), the quiet
  tip strip, and a footer carrying **address, per-day hours with the conflict noted, Google Maps deep link,
  accessibility note, partner links and the aggregation line**.
- **Mobile.** Fixed bottom action bar: **Reserve · Call · Tip** (targets ≥ 44 px, safe-area aware).

---

## 4. Theme & Color Engine (Light/Dark + Accent Selector + i18n/RTL)

**The dock.** A floating glassmorphism control in the sticky header containing, in order: **theme toggle**,
**four accent swatches**, **language select**. It collapses to a full-width bar at ≤ 560 px so it never causes
horizontal overflow at 390 px, and every control is reachable by keyboard with a 3 px ring.

| Mode | Background | Cards | Accent | Text |
|---|---|---|---|---|
| **Dark — Evening / High-Opulence** | `#070C12` | `#111827` | `#D4AF37` gold | `#F5F1E8` oyster |
| **Light — Daytime Minimalist** | `#FDFBF7` linen | `#F3EFEA` sand | `#B45309` copper | `#0F172A` navy |

**Four ambiance accents** — Executive Gold `#D4AF37`, Emerald `#059669`, Royal Cobalt `#1E40AF`, Velvet Rose
`#E11D48` — each with a light-theme counterpart that resolves to a compliant *ink* (gold becomes copper
`#B45309`, with the text ink darkened to `#664A08` to hold 7.2 : 1 on the sand card). Selecting a swatch
re-tints **buttons, links, borders, glows, card hover states, focus rings and the WebGL shader palette** through
one set of CSS custom properties — the shader samples `--accent` and `--bg` at runtime, so the hero light
changes colour with the room.

**Measured contrast** (from the harness, on live computed styles): body 17.41 : 1 dark / 17.27 : 1 light · muted
8.12 : 1 / 8.49 : 1 · primary button label 9.20 : 1 / 5.02 : 1 · glass button label 15.74 : 1 / 15.60 : 1 ·
**worst accent-ink text across all eight theme × accent combinations 5.31 : 1** (light/emerald; the gold-in-light
case measures 7.97 : 1) · focus rings always ≥ 4.4 : 1 against their surface. Targets met: body ≥ 7 : 1,
labels ≥ 4.5 : 1, muted ≥ 4.5 : 1, focus ≥ 3 : 1.

**i18n / RTL.** Header switcher with browser auto-detect and on-device persistence. **Full English + full
Arabic** ship in the prototype; six more locales are staged as disabled rows (production: 100+). Arabic sets
`dir="rtl"` on `<html>`, uses logical properties everywhere (`padding-inline`, `inset-inline`, `margin-inline`),
mirrors directional icons via `transform: scaleX(-1)`, flips the hero scrim gradient, mirrors the nav, and makes
the menu board's arrow keys **RTL-aware** (in Arabic, Left advances to the next tab, per the APG's RTL rule).
Dish names and all review quotes stay in Latin script — wine-list style — pinned with `lang="en" dir="ltr"` so
they don't corrupt the Arabic line. Arabic body copy is set in an **Amiri / Noto Naskh** stack at ~1.12× size and
1.9 line-height, because Naskh needs more room than a grotesk.

---

## 5. Interactive/WebGL Experience Plan

**Hero — "liquid light" (WebGL2).** A full-viewport fragment shader: two fBm fields warp a pair of thin
interference filaments over a soft liquid sheet, a sparse starfield twinkles above, and a pointer-tracked glow
bathes whichever corner the cursor is in. Accent and background colours are injected from CSS custom properties,
so the field re-tints with the theme *and* the accent swatch. The shader is tuned twice: night gets a deeper
vignette and the starfield; daylight gets quieter, warmer caustics and no stars.

**Guardrails.** DPR capped at **2**; the render loop pauses when the hero leaves the viewport and when the tab
is hidden; `prefers-reduced-motion` collapses everything to **one static still frame**; a `webglcontextlost`
handler steps down gracefully; shader compile/link failures log loudly rather than silently falling back.

**Fallback chain, proven.** `WebGL2 → 2D canvas → static still`. The harness disables WebGL and confirms the 2D
canvas takes over; then disables canvas entirely and confirms the still does. Reduced-motion users get the still
plus instant reveals and instantly settled counters.

**Magnetic labelled cursor.** A small accent ring that eases toward the pointer and pulls to labelled targets
(Reserve, Menu, Gift), displaying its label inside the ring. **Disabled on touch (`pointer: coarse`) and
suppressed under `prefers-reduced-motion`** — no cursor theatre on a phone.

**Motion discipline.** 0.9 s reveals staggered at 90 ms, one axis at a time; tilt cards capped at 9°; a 26-second
Ken Burns on the Vantage still; nothing that moves while the user is reading. Every animation is transform- or
opacity-based, and every one of them is removed under reduced motion.

**Playful honesty.** The Matcher, the crowd routes, the dietary-filter-to-booking hand-off, the on-device
booking memory and the struck-out slots are interactions that *do something* — they are not decoration. That is
the difference between an experience and an effect.

---

## 6. Tech & Accessibility Plan (Next.js/Tailwind/Framer Motion + WCAG)

**Stack.** Next.js 14 App Router with server components for content and small client islands for state;
Tailwind CSS with tokens mapped to the same CSS custom properties the prototype uses (so the theme engine is one
source of truth in both); **Framer Motion** for the staggered reveals, tilt and modal choreography; `next/image`
for the stills; `next-intl` with `middleware.ts` locale detection for the 100+ locales.

**Route handlers.** `POST /api/reserve` (server-side validation mirroring the client, idempotency key, SMS/email
confirmation), `POST /api/tip` → **PayPal Orders v2** create and `POST /api/tip/capture` on approval, plus a
signature-verified `POST /api/paypal/webhook`. **No card data ever touches our infrastructure** — the guest
approves in PayPal's own flow. `GET /api/hours` becomes the single source of truth that fixes Weakness 1.
The full port map, environment variables and revalidation strategy are in `README.md §4`.

**WCAG 2.1 AA commitments.**
- Skip link is the **first tab stop** (verified) and jumps to `<main>`.
- **3 px visible focus ring everywhere**, instant — `outline` is never transitioned from 0 px, so keyboard users
  never lose their place. Verified across 10 consecutive tab stops.
- Modal focus trap with Esc-to-close and **focus restored to the trigger**.
- **Disabled-by-design** time guards that are struck through *and* explained in text — never colour-only.
- Full keyboard paths with no traps: tabs (arrows/Home/End, RTL-aware), chips, matcher, booking, tip.
- AA contrast in both themes and in **all eight theme × accent combinations**, measured not assumed.
- `aria-live` announcements for validation failures, with **focus moved to the first invalid control**.
- Real alt text on all six stills; `lang`/`dir` correctly scoped so mixed-script text reads properly.
- JSON-LD for the venue and the FAQ set, with the correct business identity.

**Performance.** LCP < 2.5 s budget with the hero still preloaded and everything else lazy and intrinsically
sized; shader paused off-screen and on tab-hide; no third-party scripts above the fold; ISR caching for menu and
hours; the trust wall synced nightly so the rating never goes stale.

**Mobile.** Bottom action bar with safe-area padding, ≥ 44 px targets, zero horizontal overflow at 390 px, and a
dock that reflows instead of scrolling sideways.

---

## 7. How This Redesign Wins the Decision (Client Summary)

**What changes against the current state (improvements, in the order a guest meets them).**

| Now | After |
|---|---|
| *"Delicious, freshly cooked food"* over a stock burger | A location-true promise, plus a glass panel of four checkable facts |
| Rating and review count invisible | 4.1 ★ · 79 in the hero, in the counters and in schema |
| Hours that contradict three other sources | One statement of the service window, struck-out slots, and the conflict printed with a phone number |
| Menu as a PDF and two JPEGs | An HTML board with real prices, dietary chips and structured data |
| *"ORDER ONLINE"* → the vendor's subdomain | A 20-second owned booking flow, no card, on-device memory |
| Group enquiries → *call during service* | Nine crowd routes that pre-fill the booking in one tap |
| Halal only in the business name | Halal kitchen as a hero chip, an FAQ answer and schema |
| No place, no vantage | A full-bleed Vantage band naming Blackford Hill, the Royal Observatory and the skyline |
| Nothing asking for a tip, no path to give one | "Thank the team" in five placements, optional, straight to the floor |

**Why bookings rise.** Four mechanisms, in order of expected size. **(1) Hours certainty** — removing the
mis-booked walk-up and the wasted Tuesday is the single largest recoverable volume, and it costs nothing but
truth. **(2) Discoverability** — an HTML menu with schema converts searches that currently can't reach the
kitchen at all. **(3) Friction removal** — 2 steps, 0 cards, remembered defaults and self-explaining disabled
slots lift completion on the traffic that already arrives. **(4) Group business** — nine routes turn a phone
call into a form, which is the highest-margin revenue a counter can add without adding a room. Each mechanism
is measurable on its own (slot-clicks per session, menu-tab engagement, form completion, crowd-route bookings),
so the redesign is also a reporting instrument.

**Where the PayPal tip fits, naturally.** Not as a toll — as gratitude, in the five places a guest actually feels
it: the hero micro-line, the confirmation screen the moment a slot is held, the live summary, the final CTA, and
the mobile bar. Suggested amounts are one tap (£1 / £2 / £5 / £10) with a custom field, the copy states plainly
that it is *"entirely optional, never expected"* and goes to the floor team, and the payment runs through
**PayPal Orders v2** server-side — the guest approves in PayPal, no card data is ever handled, and the tip is
reversible before collection. It is a two-line addition to an already-built confirmation screen, which is
exactly why it will actually get used.

**Core vs optional scope.**

| | Core (what the prototype proves) | Optional (phase two) |
|---|---|---|
| **Build** | Single-page experience: hero + shader, experience & matcher, HTML menu board, Vantage band, booking portal with slots and crowd routes, trust wall, six FAQs, footer, mobile bar | Per-dish pages, gift-voucher storefront, loyalty for the King's Buildings crowd, deliverable "track my order" view |
| **Systems** | Hours single source of truth, `Restaurant` + `FAQPage` schema, reserve route handler, on-device defaults | `POST /api/reserve` SMS automation, POS integration (Square/Toast), review-sync worker, seasonal offer engine |
| **Money** | — | PayPal Orders v2 tips + gift vouchers, deposits on crowd orders of 20+ |
| **Locales** | English + Arabic (both complete in the prototype) | The remaining 98+ locales, ordered by actual traffic |
| **Content** | Six editorial stills, all provenance-led | A quarterly shoot pass, including a genuine site visit for accessibility and the vantage

---

## Appendix — Evidence Log

Every claim used in the prototype and in this pitch, with its source. Nothing here is inferred from vibes;
nothing invented is presented as verified.

| # | Claim as used | Source | Status |
|---|---|---|---|
| 1 | Name: **Bonnie Burgers حلال**; 61 Mayfield Rd, Edinburgh EH9 3AA; tel **+44 131 374 4464**; category *fast food restaurant* | Google Maps place page (the supplied pin) | **Verified** |
| 2 | Coordinates **55.9306092, −3.1761176** | Google Maps place URL | **Verified** |
| 3 | Rating **4.1 ★ from 79 reviews** | Google Maps place page | **Verified** |
| 4 | Verbatim quotes: *"The loaded fries and milkshakes are amazing and the staff are really friendly."* / *"High quality food, fast, friendly service, good value too."* / *"Really enjoyed the buttermilk chicken and Philly Cheesesteak!"* / *"Food was of great quality and tasted lovely…"* (Abdul Ahmad) / *"Burger was really good. Tasty & melt in the mouth…"* (lorna andrew) / *"Portions are a little smaller than competitors, but still filling enough."* | Google Maps reviews and review summary | **Verified** (quoted verbatim; the critical quote is deliberately retained) |
| 5 | Review keyword counts: *friendly staff* 21, *milkshakes* 8, *wait time* 8, *cheese steak* 3, *smash burger* 2, *lava burger* 2 | Google Maps review keyword cloud | **Verified** |
| 6 | **Hours conflict — 5 variants.** FSA register & Just Eat: `Su–Mo 17:10–21:50`, `We–Sa 17:10–21:50` (**no Tuesday**). Uber Eats: `17:15–21:45` Sun, Mon, Wed–Sat. Mapcarta/OSM: `16:00–22:30`. Google Maps: `5–10 PM`, Tuesday closed. **Own website: `12pm–10pm Mon–Fri`, `5pm–10pm Sat–Sun`, "Open all Bank Holidays" (implies weekday lunch and Tuesday service)** | FSA register · Just Eat listing · Uber Eats store page · Mapcarta (OSM) · Google Maps · bonnieburgers.co.uk | **Conflict — verified as conflicting.** Prototype adopts the majority record and strikes out what it cannot verify |
| 7 | Business classification: **"Takeaway/sandwich shop"** (address 61 Mayfield Road, EH9 3AA); FHIS rating *Pass* | Food Standards Agency ratings register (business 1707893); Uber Eats | **Verified** — which is why the page never claims a dining room or a private room |
| 8 | Menu: dish names, descriptions, dietary marks **(V)/(VG)**, prices **£1.00–£12.50** (Bonnie Smash £6.95 → Bonnie Tower £12.50; shakes £5.25; wings x6/x12 £4.95/£6.95; dips £1.00–£1.50; kids from £4.95) | Venue menu PDF `LCP39213-Bonnie-Burgers-1.pdf` (Sept 2025) | **Verified** |
| 9 | **11 wing finishes** — 6 crispy (Bonnie's Fire, Buffalo, Garlic Parmesan, Lemon Pepper, Korean Gochujang, Smoky BBQ) + 5 peri (Mild, Medium, Hot, Lemon Garlic, Chilli Lime Crema) | Counted on the menu PDF | **Verified by count** |
| 10 | Delivery partner ratings: Deliveroo **4.4 (72)**; Uber Eats **4.0 (54)** | Deliveroo and Uber Eats store pages | **Verified** |
| 11 | Website is **live, not parked** — but it is a brochure: no booking engine, no HTML menu, one *Contact* form, `SEE OUR MENU` → PDF, `ORDER ONLINE` → `bonnieburgersonline.co.uk` | bonnieburgers.co.uk | **Verified (diagnosis signal, not design analysis)** |
| 12 | **Domain/identity defect:** the site's own JSON-LD names the business **"Low Cost Menus"** (the template vendor), `inLanguage: en-GB`; footer reads *"Copyright 2026 – Low Cost Menus"* | Page source of bonnieburgers.co.uk | **Verified** |
| 13 | Address discrepancy: the Uber Eats listing shows **"62 Mayfield Road, EH9 2"** and a different phone (+44 7545 639816) | Uber Eats store page | **Verified** — flagged for correction |
| 14 | Neighbourhood: **Blackford / Mayfield**, south Edinburgh; delivery listings place it in *The Grange and Blackford* | Deliveroo listing; Google Maps | **Verified** |
| 15 | Landmarks & walk distances: **King's Buildings ≈ 0.5 km**, **Hermitage of Braid ≈ 0.6 km**, **Blackford Hill & Royal Observatory ≈ 0.9 km**, **Newington & Cameron Toll ≈ 1.2 km** | Google Maps geometry for the pin | **Approximate** (straight-line walking estimates) |
| 16 | The Vantage: Blackford Hill **164 m**, observatory domes completed **1896**, views north to **Arthur's Seat, the Salisbury Crags, the Pentland Hills**, occasionally the Firth of Forth and Fife; Hermitage of Braid & Blackford Hill reserve **60.3 ha** | Royal Observatory Edinburgh (roe.ac.uk directions/visitor info) · Wikipedia *Blackford Hill* · Curious Edinburgh | **Verified** — this is why the band shows tenement rooftops, Arthur's Seat and the Crags, and **no** Calton Hill monuments or castle skyline |
| 17 | Halal | Business name (حلال) and the venue's Facebook bio (*"📍Edinburgh \| حلال"*) | **Verified** |
| 18 | Social presence: Facebook page (`bonnieburgersofficial`, ~15 likes, no reviews) and a TikTok handle | Facebook page | **Verified** | 
| 19 | "Eat in" seating exists at the counter | — | **PLACEHOLDER** — FSA classifies the premises as a takeaway/sandwich shop; the prototype offers the option and annotates it as unconfirmed |
| 20 | Weekday **lunchtime** service | Own website only, contradicted by three sources | **UNVERIFIED** — daytime slots are rendered *disabled by design* with the reason stated |
| 21 | Named local suppliers in the provenance strip | — | **PLACEHOLDER** — none verified; the strip ships with distance facts instead and says the names await confirmation |
| 22 | Crowd-tray prices (£34 / £82 / £95) and the nine crowd routes | Built from published board prices | **PLACEHOLDER** — illustrative bundles and lead times |
| 23 | Gift vouchers | — | **PLACEHOLDER** — new capability, not an existing product |
| 24 | Accessibility details (step-free threshold, counter height, toilet) | — | **PLACEHOLDER** — requires a site visit |
| 25 | Cancellation/deposit policy (2 hours for tables; deposit on 20+) | — | **PLACEHOLDER** — proposed terms pending the kitchen's policy |
| 26 | Tip via **PayPal Orders v2**, amounts £1/£2/£5/£10 + custom | — | **New build** — the prototype's button is wired to a simulated endpoint and labelled as such on screen |
| 27 | Six further locales staged in the switcher; production ships 100+ | — | **Prototype scope** — English and Arabic are complete; the rest are disabled rows, not fake translations |

**QA evidence.** `python3 qa.py` → **74 checks, 74 pass, 0 fail** (`qa-report.json`), covering: exact theme
tokens and measured contrast in both themes; the accent swap re-tinting UI **and** shader palette; the
Arabic switch flipping `dir`, mirroring the nav, re-localising dynamic outputs and keeping Latin quotes pinned;
matcher → booking pre-fill; out-of-service and Tuesday slots disabled; validation announcing and focusing the
first invalid control; the confirmation pane, tip focus trap and Esc-restore; counters settling (instantly under
reduced motion); tab panels switching and arrow-navigating in both text directions; all six stills HTTP 200 with
alt text and dimensions; JSON-LD parsing; the skip link as first tab stop; ten consecutive tab stops with an
instant 3 px ring; the mobile bar at 390 px with zero horizontal overflow; and the full fallback chain
(WebGL2 → 2D canvas → static still) proven by disabling each layer in turn.
