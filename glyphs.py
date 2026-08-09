#!/usr/bin/env python3
"""SVG glyph library for the study companion.

All glyphs share a 0 0 100 100 viewBox and use `currentColor` for strokes so
the page CSS can tint them (breath-teal / amber). Line art is deliberately
minimal and consistent in weight — an anatomical-atlas vocabulary, not clip art.

Three families:
  ASANA_GLYPH   – one line-figure per canonical asana (visual pose gallery)
  TOPIC_GLYPH   – a small mark per teaching topic (card anchor)
  CONCEPT       – full section-hero diagrams (the thesis, drawn)
"""

# a filled head + shared stroke class 'gl' (CSS: fill:none;stroke:currentColor)
def _fig(body, head=None):
    h = f'<circle class="gh" cx="{head[0]}" cy="{head[1]}" r="{head[2]}"/>' if head else ""
    return f'<g class="glyph-fig">{h}{body}</g>'

# ---------------------------------------------------------------- ASANAS ----
ASANA_GLYPH = {
 # inversions
 "Sirsasana": _fig(
   '<path class="gl" d="M50 70 L42 84 M50 70 L58 84"/>'          # forearms base
   '<path class="gl" d="M46 84 H54"/>'                            # crown line
   '<path class="gl" d="M50 70 L50 40"/>'                         # torso up
   '<path class="gl" d="M50 40 L44 16 M50 40 L56 16"/>',         # legs up
   head=(50,64,6)),
 "Sarvangasana": _fig(
   '<path class="gl" d="M24 82 H52"/>'                            # shoulders on floor
   '<path class="gl" d="M50 80 L54 46"/>'                         # torso up (slight)
   '<path class="gl" d="M54 46 L52 18 M54 46 L60 18"/>',         # legs up
   head=(22,80,6)),
 "Halasana": _fig(
   '<path class="gl" d="M20 78 H46"/>'                            # shoulders
   '<path class="gl" d="M44 76 Q64 44 78 40"/>'                   # torso arcs over
   '<path class="gl" d="M78 40 L86 60"/>',                        # legs to floor behind
   head=(18,76,6)),
 # seated
 "Paschimottanasana": _fig(
   '<path class="gl" d="M26 66 H82"/>'                            # legs along floor
   '<path class="gl" d="M30 66 Q34 44 44 40"/>'                   # torso folding
   '<path class="gl" d="M44 40 Q64 44 78 62"/>',                  # reach to feet
   head=(30,40,6)),
 "Virasana": _fig(
   '<path class="gl" d="M50 40 L50 62"/>'                         # torso upright
   '<path class="gl" d="M50 62 Q40 66 34 78 M50 62 Q60 66 66 78"/>'  # folded shins
   '<path class="gl" d="M50 46 L40 56 M50 46 L60 56"/>',         # arms/thighs
   head=(50,34,6)),
 "Padmasana": _fig(
   '<path class="gl" d="M50 42 L50 60"/>'                         # torso
   '<path class="gl" d="M30 74 Q50 58 70 74"/>'                   # crossed legs base
   '<path class="gl" d="M50 48 L36 60 M50 48 L64 60"/>',         # knees to hands
   head=(50,36,6)),
 "Baddha Konasana": _fig(
   '<path class="gl" d="M50 42 L50 60"/>'                         # torso
   '<path class="gl" d="M50 60 L32 76 L50 70 L68 76 Z"/>',       # soles together diamond
   head=(50,36,6)),
 # standing
 "Tadasana": _fig(
   '<path class="gl" d="M50 34 L50 66"/>'                         # spine
   '<path class="gl" d="M50 40 L40 58 M50 40 L60 58"/>'          # arms down
   '<path class="gl" d="M50 66 L44 88 M50 66 L56 88"/>',         # legs
   head=(50,26,6)),
 "Uttanasana": _fig(
   '<path class="gl" d="M50 30 L50 60"/>'                         # legs (standing)
   '<path class="gl" d="M50 30 Q50 16 44 12"/>'                   # torso folded down
   '<path class="gl" d="M50 60 L46 86 M50 60 L54 86"/>',         # legs to floor
   head=(42,10,5)),
 "Prasarita Padottanasana": _fig(
   '<path class="gl" d="M26 86 L44 40 M74 86 L56 40"/>'          # wide legs
   '<path class="gl" d="M44 40 Q50 30 56 40"/>'                   # pelvis
   '<path class="gl" d="M50 36 L50 20"/>',                        # torso folds down (head low)
   head=(50,16,5)),
 "Trikonasana": _fig(
   '<path class="gl" d="M22 86 L40 44 M78 86 L56 44"/>'          # wide legs
   '<path class="gl" d="M40 44 L64 26"/>'                         # torso tilted
   '<path class="gl" d="M52 35 L44 60 M52 35 L60 12"/>',         # arms line (down/up)
   head=(66,24,5)),
 # arm balance / prone
 "Bakasana": _fig(
   '<path class="gl" d="M40 76 L40 60 M60 76 L60 60"/>'          # arms to floor
   '<path class="gl" d="M40 60 Q50 52 60 60"/>'                   # shoulders
   '<path class="gl" d="M46 58 Q66 54 70 40"/>',                  # tucked body/legs up
   head=(38,56,5)),
 "Adho Mukha Svanasana": _fig(
   '<path class="gl" d="M18 82 L50 34"/>'                         # arms+back
   '<path class="gl" d="M50 34 L82 82"/>',                        # legs — the inverted V
   head=None),
 "Urdhva Mukha Svanasana": _fig(
   '<path class="gl" d="M30 78 L30 54"/>'                         # arm straight
   '<path class="gl" d="M30 54 Q46 44 62 50 Q78 56 86 78"/>',    # chest up, legs back
   head=(30,48,5)),
 "Backbends": _fig(
   '<path class="gl" d="M26 78 Q50 20 74 78"/>'                   # arch
   '<path class="gl" d="M26 78 L22 86 M74 78 L78 86"/>',
   head=(50,30,5)),
 "Parivritta / Twists": _fig(
   '<path class="gl" d="M34 78 H66"/>'                            # seated base
   '<path class="gl" d="M50 74 L50 44"/>'                         # spine
   '<path class="gl" d="M50 52 Q66 48 64 62"/>'                   # twisting arm
   '<path class="gl" d="M50 52 Q36 50 40 40"/>',
   head=(50,38,6)),
 "Shavasana": _fig(
   '<path class="gl" d="M20 60 H74"/>'                            # body lying
   '<path class="gl" d="M74 60 L82 55 M74 60 L82 65"/>',         # feet
   head=(16,60,6)),
 "Sarvangasana (Shoulderstand)": None,  # alias handled below
}

# symbolic marks for locks / breath / cleansing / concepts ------------------
def _torso_outline():
    return '<path class="gl gl-dim" d="M38 22 Q50 16 62 22 L60 78 Q50 84 40 78 Z"/>'

ASANA_GLYPH.update({
 "Mula Bandha": _fig(
   _torso_outline() +
   '<path class="gl ga" d="M44 74 L50 66 L56 74"/>'              # upward lock chevron at root
   '<path class="gl ga" d="M50 66 L50 54"/>'),                    # lift line
 "Uddiyana Bandha": _fig(
   _torso_outline() +
   '<path class="gl ga" d="M40 52 Q50 44 60 52"/>'               # concave belly (vacuum in)
   '<path class="gl ga" d="M50 40 L50 50 M46 46 L50 50 L54 46"/>'),  # inward arrow
 "Jalandhara Bandha": _fig(
   _torso_outline() +
   '<path class="gl ga" d="M42 30 Q50 36 58 30"/>',              # chin lock at throat
   head=(50,20,6)),
 "Nauli": _fig(
   _torso_outline() +
   '<path class="gl ga" d="M50 44 V72"/>'                        # central column isolated
   '<path class="gl gl-dim" d="M44 46 V70 M56 46 V70"/>'),
 "Agnisara Dhauti": _fig(
   '<path class="gl ga" d="M50 78 Q36 60 50 44 Q64 60 50 78 Z"/>'  # flame
   '<path class="gl ga" d="M50 66 Q44 58 50 50 Q56 58 50 66"/>'),
 "Shatkarma": _fig(
   '<path class="gl ga" d="M50 24 A26 26 0 1 1 24 50"/>'         # cleansing spiral
   '<path class="gl ga" d="M24 50 A26 26 0 0 0 62 72"/>'),
})

# breath practices — waveforms
def _wave(amp, n, sharp=False):
    step = 60/ n
    d = "M20 50"
    x = 20
    up = True
    for i in range(n):
        if sharp:
            d += f" L{x+step/2:.0f} {50-amp if up else 50+amp:.0f} L{x+step:.0f} 50"
        else:
            d += f" Q{x+step/2:.0f} {50-amp if up else 50+amp:.0f} {x+step:.0f} 50"
        x += step; up = not up
    return f'<path class="gl ga" d="{d}"/>'

for name, amp, n, sharp in [
    ("Pranayama", 20, 3, False),
    ("Ujjayi", 16, 3, False),
    ("Viloma", 16, 5, True),
    ("Nadi Shodhana", 18, 2, False),
    ("Surya Bhedana", 20, 2, False),
    ("Kapalabhati", 22, 6, True),
    ("Bhastrika", 24, 6, True),
]:
    ASANA_GLYPH[name] = _fig(_wave(amp, n, sharp))

# structural / anatomy concept asanas
ASANA_GLYPH.update({
 "Hip-Joint Mobility": _fig(
   '<circle class="gl" cx="50" cy="46" r="10"/>'                 # socket
   '<path class="gl" d="M50 46 L74 78"/>'                        # femur
   '<path class="gl gl-dim" d="M50 46 L30 76"/>'),               # range arc
 "Spinal Alignment": _fig(
   '<path class="gl" d="M50 18 Q44 34 50 50 Q56 66 50 84"/>'     # S-curve spine
   '<path class="gl gl-dim" d="M44 26 H56 M44 50 H56 M44 74 H56"/>'),
 "Asymmetrical Asanas": _fig(
   '<path class="gl" d="M50 20 V80"/>'                           # midline
   '<path class="gl ga" d="M50 40 L74 34"/>'                     # one side
   '<path class="gl gl-dim" d="M50 60 L28 66"/>'),               # other side
 "Surya Namaskar": _fig(
   '<circle class="gl ga" cx="50" cy="50" r="16"/>'              # sun
   '<path class="gl ga" d="M50 22 V14 M50 78 V86 M22 50 H14 M78 50 H86 '
   'M30 30 L24 24 M70 30 L76 24 M30 70 L24 76 M70 70 L76 76"/>'),
})

# splits share a construction: a low pelvis with legs stretched apart
ASANA_GLYPH["Hanumanasana"] = _fig(
   '<path class="gl gl-dim" d="M14 82 H86"/>'                    # floor line
   '<path class="gl" d="M50 66 L18 82 M50 66 L82 82"/>'         # front + back leg to floor
   '<path class="gl" d="M50 66 L50 46"/>'                        # torso up from pelvis
   '<path class="gl" d="M50 52 L40 60 M50 52 L60 60"/>',        # arms
   head=(50,40,6))
ASANA_GLYPH["Samakonasana"] = _fig(
   '<path class="gl gl-dim" d="M50 64 V84"/>'                    # drop line to floor
   '<path class="gl" d="M50 64 L14 72 M50 64 L86 72"/>'         # legs splayed wide, low
   '<path class="gl" d="M50 64 L50 44"/>'                        # torso up
   '<path class="gl" d="M50 50 L40 58 M50 50 L60 58"/>',        # arms
   head=(50,38,6))

# ---------------------------------------------------------------- TOPICS ----
TOPIC_GLYPH = {
 "philosophy":  '<circle class="gl" cx="50" cy="50" r="26"/><circle class="gh" cx="50" cy="50" r="5"/>',
 "anatomy":     '<path class="gl" d="M50 20 Q42 40 50 50 Q58 60 50 80"/><path class="gl gl-dim" d="M40 34 L60 34 M40 66 L60 66"/>',
 "practice-method": '<path class="gl" d="M24 68 L44 40 L56 56 L76 30"/><circle class="gh" cx="76" cy="30" r="4"/>',
 "asana-technique": '<rect class="gl" x="30" y="30" width="40" height="40" rx="4"/><path class="gl gl-dim" d="M30 50 H70 M50 30 V70"/>',
 "bandhas":     '<path class="gl" d="M38 50 V42 A12 12 0 0 1 62 42 V50"/><rect class="gl" x="34" y="50" width="32" height="26" rx="3"/>',
 "breath":      '<path class="gl" d="M22 54 Q34 34 46 54 Q58 74 70 54 Q76 44 80 50"/>',
}

# --------------------------------------------------------------- CONCEPTS ---
# Full section-hero diagrams. Larger canvases, self-contained.

# contract-not-stretch + joint-as-tone + the chain, as one anatomy plate
CONCEPT_ANATOMY = '''<svg viewBox="0 0 640 175" role="img" class="concept" aria-label="Diagram: muscles contract (they never stretch), a joint is held by muscular tone, and muscles work in chains like a tank tread.">
  <!-- panel 1: contraction -->
  <g>
    <text x="90" y="24" class="c-cap" text-anchor="middle" data-i18n="dgm_a1">contraction, not stretch</text>
    <line class="c-bone" x1="30" y1="60" x2="30" y2="150"/>
    <line class="c-bone" x1="150" y1="60" x2="150" y2="150"/>
    <path class="c-musc" d="M30 105 Q90 90 150 105"/>
    <path class="c-flow" d="M150 105 Q90 96 30 105"/>
    <path class="c-arrow" d="M64 99 L54 103 L64 107"/>
    <path class="c-arrow" d="M116 99 L126 103 L116 107"/>
  </g>
  <!-- panel 2: joint held by tone -->
  <g transform="translate(210 0)">
    <text x="100" y="30" class="c-cap" text-anchor="middle" data-i18n="dgm_a2">a joint is held by tone</text>
    <circle class="c-bone" cx="70" cy="70" r="16" fill="none"/>
    <circle class="c-bone" cx="130" cy="130" r="16" fill="none"/>
    <line class="c-bone" x1="70" y1="86" x2="70" y2="150"/>
    <line class="c-bone" x1="130" y1="114" x2="130" y2="50"/>
    <path class="c-musc" d="M78 78 Q100 100 122 122"/>
    <path class="c-musc" d="M62 90 Q100 108 138 118" opacity=".6"/>
  </g>
  <!-- panel 3: the chain (tank tread) -->
  <g transform="translate(430 0)">
    <text x="100" y="30" class="c-cap" text-anchor="middle" data-i18n="dgm_a3">everything moves in chains</text>
    <path class="c-flow" d="M30 150 Q30 60 100 60 Q170 60 170 150"/>
    <circle class="c-node" cx="30" cy="150" r="7"/>
    <circle class="c-node" cx="52" cy="82" r="7"/>
    <circle class="c-node" cx="100" cy="60" r="7"/>
    <circle class="c-node" cx="148" cy="82" r="7"/>
    <circle class="c-node" cx="170" cy="150" r="7"/>
  </g>
</svg>'''

# the three bandhas + diaphragm, on a single body column
CONCEPT_BANDHA = '''<svg viewBox="0 0 300 360" role="img" class="concept" aria-label="Diagram: the body's central column with the three locks — jalandhara at the throat, uddiyana at the navel, mula bandha at the pelvic floor — and the diaphragm between.">
  <path class="c-body" d="M120 30 Q150 18 180 30 L172 320 Q150 336 128 320 Z"/>
  <!-- jalandhara -->
  <line class="c-lock" x1="120" y1="70" x2="180" y2="70"/>
  <circle class="c-dot" cx="150" cy="70" r="5"/>
  <text x="196" y="74" class="c-lbl" data-i18n="dgm_b1">Jalandhara · throat</text>
  <!-- diaphragm -->
  <path class="c-diaph" d="M124 150 Q150 172 176 150"/>
  <text x="196" y="152" class="c-lbl c-lbl-breath" data-i18n="dgm_bd">diaphragm · the conductor</text>
  <!-- uddiyana -->
  <path class="c-lock" d="M128 210 Q150 196 172 210"/>
  <circle class="c-dot" cx="150" cy="206" r="5"/>
  <text x="196" y="212" class="c-lbl" data-i18n="dgm_b2">Uddiyana · navel</text>
  <!-- mula -->
  <path class="c-lock" d="M134 300 L150 288 L166 300"/>
  <circle class="c-dot" cx="150" cy="292" r="5"/>
  <text x="196" y="300" class="c-lbl" data-i18n="dgm_b3">Mula · pelvic floor</text>
  <!-- central lift line -->
  <line class="c-lift" x1="150" y1="300" x2="150" y2="80" stroke-dasharray="3 6"/>
</svg>'''

# pelvis: trapezoid vs square (nutation) — reused idea from index, standalone
CONCEPT_METHOD = '''<svg viewBox="0 0 560 240" role="img" class="concept" aria-label="Diagram: balancing two muscular chains (50/50), and the pelvis turning from a trapezoid into a square.">
  <!-- 50/50 balance -->
  <g>
    <text x="130" y="28" class="c-cap" text-anchor="middle" data-i18n="dgm_m1">balance the two chains — 50 / 50</text>
    <line class="c-bone" x1="40" y1="150" x2="220" y2="150" stroke-dasharray="4 6"/>
    <polygon class="c-bone" points="130,110 116,150 144,150" fill="none"/>
    <line class="c-beam" x1="60" y1="90" x2="200" y2="90"/>
    <path class="c-flow" d="M50 70 h30 l-8 20 h-14 z"/>
    <path class="c-amber" d="M180 70 h30 l-8 20 h-14 z"/>
  </g>
  <!-- pelvis trapezoid -> square -->
  <g transform="translate(300 0)">
    <text x="130" y="28" class="c-cap" text-anchor="middle" data-i18n="dgm_m2">trapezoid → square (nutation)</text>
    <polygon class="c-bad" points="60,60 120,60 140,140 40,140"/>
    <path class="c-arrow-big" d="M150 100 h30 m-10 -8 l10 8 l-10 8"/>
    <rect class="c-good" x="200" y="60" width="90" height="80"/>
  </g>
</svg>'''

# the founding refusals, drawn: yoga serves you / body→state / comfort from within
CONCEPT_PHILOSOPHY = '''<svg viewBox="0 0 640 175" role="img" class="concept" aria-label="Diagram: yoga serves you (energy flows into the practitioner), the body is the instrument and the state is the goal, and comfort expands outward from within.">
  <!-- panel 1: yoga serves you -->
  <g>
    <text x="100" y="24" class="c-cap" text-anchor="middle" data-i18n="dgm_p1">yoga serves you</text>
    <circle class="c-node" cx="100" cy="66" r="11"/>
    <line class="c-bone" x1="100" y1="77" x2="100" y2="120"/>
    <line class="c-bone" x1="100" y1="90" x2="80" y2="110"/>
    <line class="c-bone" x1="100" y1="90" x2="120" y2="110"/>
    <line class="c-bone" x1="100" y1="120" x2="86" y2="152"/>
    <line class="c-bone" x1="100" y1="120" x2="114" y2="152"/>
    <path class="c-flow" d="M34 74 Q66 80 84 96"/>
    <path class="c-arrow" d="M74 88 L86 96 L74 100"/>
    <path class="c-flow" d="M166 74 Q134 80 116 96"/>
    <path class="c-arrow" d="M126 88 L114 96 L126 100"/>
  </g>
  <!-- panel 2: body is the instrument, the state is the goal -->
  <g transform="translate(220 0)">
    <text x="100" y="24" class="c-cap" text-anchor="middle" data-i18n="dgm_p2">body → state</text>
    <circle class="c-bone" cx="46" cy="66" r="10" fill="none"/>
    <line class="c-bone" x1="46" y1="76" x2="46" y2="116"/>
    <line class="c-bone" x1="46" y1="88" x2="30" y2="104"/>
    <line class="c-bone" x1="46" y1="88" x2="62" y2="104"/>
    <line class="c-bone" x1="46" y1="116" x2="34" y2="150"/>
    <line class="c-bone" x1="46" y1="116" x2="58" y2="150"/>
    <path class="c-arrow-big" d="M86 100 h34 m-10 -8 l10 8 l-10 8"/>
    <circle class="c-flow" cx="168" cy="100" r="30" opacity=".35"/>
    <circle class="c-flow" cx="168" cy="100" r="19" opacity=".6"/>
    <circle class="c-node" cx="168" cy="100" r="7"/>
  </g>
  <!-- panel 3: comfort expands from within -->
  <g transform="translate(430 0)">
    <text x="100" y="24" class="c-cap" text-anchor="middle" data-i18n="dgm_p3">expand from within</text>
    <circle class="c-node" cx="100" cy="100" r="6"/>
    <circle class="c-flow" cx="100" cy="100" r="24" opacity=".7"/>
    <circle class="c-flow" cx="100" cy="100" r="42" opacity=".3" stroke-dasharray="3 6"/>
    <path class="c-arrow" d="M100 100 L128 72 M120 74 L130 70 L128 80"/>
    <path class="c-arrow" d="M100 100 L72 72 M80 74 L70 70 L72 80"/>
    <path class="c-arrow" d="M100 100 L128 128 M120 126 L130 130 L128 120"/>
    <path class="c-arrow" d="M100 100 L72 128 M80 126 L70 130 L72 120"/>
  </g>
</svg>'''

CONCEPT = {
 "phil": CONCEPT_PHILOSOPHY,
 "anat": CONCEPT_ANATOMY,
 "breath": CONCEPT_BANDHA,
 "method": CONCEPT_METHOD,
}

def asana_glyph(en_name):
    g = ASANA_GLYPH.get(en_name)
    if g:
        return g
    # generic fallback: a seated figure mark
    return _fig('<path class="gl" d="M36 76 H64"/><path class="gl" d="M50 72 L50 46"/>'
                '<path class="gl gl-dim" d="M50 54 L38 48 M50 54 L62 48"/>', head=(50,40,6))
