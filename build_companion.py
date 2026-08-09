#!/usr/bin/env python3
"""Generate companion.html — a VISUAL bilingual (EN/RU) study companion.

Design intent: an anatomical atlas to index.html's notebook. The page leads
with pictures, not paragraphs —
  * every section opens with a hand-drawn SVG concept diagram (the thesis);
  * the asana library is a pose GALLERY of line-art glyphs that expand on tap;
  * each teaching card shows a topic glyph + one bold principle, and tucks the
    "why" / "common mistake" / source into a native <details> — text on demand.

Mirrors index.html's design system (Space Grotesk / Spectral / IBM Plex Mono;
ink-teal + breath + amber + coral; blueprint grid) and its lossless apply()
EN<->RU toggle with RU default. English lives inline (JS-off fallback); Russian
lives in the RU{} dict keyed by data-i18n.
"""
import json, html, os
import glyphs as G

BASE = "/Users/gblazer/workspace/voice"
corpus = json.load(open(os.path.join(BASE, "captions/distilled/corpus.json"), encoding="utf-8"))["teachings"]

def esc(s):
    return html.escape(s or "", quote=False)

TOPIC = {
    "philosophy":      ("Философия",  "Philosophy",  "breath"),
    "anatomy":         ("Анатомия",   "Anatomy",     "amber"),
    "practice-method": ("Метод",      "Method",      "breath"),
    "asana-technique": ("Техника",    "Technique",   "amber"),
    "bandhas":         ("Бандхи",     "Bandhas",     "coral"),
    "breath":          ("Дыхание",    "Breath",      "breath"),
}

def norm_asana(a):
    if not a: return None
    key = a.strip().lower().replace(" ", "").replace("/", "").replace("-", "")
    fam = [
      ("mulabandha","Mula Bandha","Мула-бандха"),
      ("uddiyana","Uddiyana Bandha","Уддияна-бандха"),
      ("nauli","Nauli","Наули"),
      ("jalandhara","Jalandhara Bandha","Джаландхара-бандха"),
      ("sirsasana","Sirsasana","Ширшасана · стойка на голове"),
      ("headstand","Sirsasana","Ширшасана · стойка на голове"),
      ("sarvangasana","Sarvangasana","Сарвангасана · берёзка"),
      ("shoulderstand","Sarvangasana","Сарвангасана · берёзка"),
      ("halasana","Halasana","Халасана · плуг"),
      ("paschimottanasana","Paschimottanasana","Пашчимоттанасана"),
      ("hanumanasana","Hanumanasana","Хануманасана · продольный шпагат"),
      ("frontsplit","Hanumanasana","Хануманасана · продольный шпагат"),
      ("samakonasana","Samakonasana","Самаконасана · поперечный шпагат"),
      ("transversesplit","Samakonasana","Самаконасана · поперечный шпагат"),
      ("padmasana","Padmasana","Падмасана · лотос"),
      ("baddhakonasana","Baddha Konasana","Баддха Конасана · бабочка"),
      ("butterfly","Baddha Konasana","Баддха Конасана · бабочка"),
      ("trikonasana","Trikonasana","Триконасана · треугольник"),
      ("parivritta","Parivritta / Twists","Паривритта · скручивания"),
      ("parivrtta","Parivritta / Twists","Паривритта · скручивания"),
      ("twist","Parivritta / Twists","Паривритта · скручивания"),
      ("bakasana","Bakasana","Бакасана · ворона"),
      ("virasana","Virasana","Вирасана · герой"),
      ("adhomukha","Adho Mukha Svanasana","Адхо Мукха Шванасана · собака вниз"),
      ("downwarddog","Adho Mukha Svanasana","Адхо Мукха Шванасана · собака вниз"),
      ("urdhvamukha","Urdhva Mukha Svanasana","Урдхва Мукха Шванасана · собака вверх"),
      ("uttanasana","Uttanasana","Уттанасана · наклон стоя"),
      ("forwardfold","Uttanasana","Уттанасана · наклон стоя"),
      ("prasarita","Prasarita Padottanasana","Прасарита Падоттанасана"),
      ("tadasana","Tadasana","Тадасана · гора / баланс"),
      ("handstand","Tadasana","Тадасана · гора / баланс"),
      ("shavasana","Shavasana","Шавасана"),
      ("suryanamaskar","Surya Namaskar","Сурья Намаскар"),
      ("hindupushup","Surya Namaskar","Сурья Намаскар"),
      ("kapalabhati","Kapalabhati","Капалабхати"),
      ("bhastrika","Bhastrika","Бхастрика"),
      ("nadishodhana","Nadi Shodhana","Нади Шодхана"),
      ("suryabhedana","Surya Bhedana","Сурья Бхедана"),
      ("ujjayi","Ujjayi","Уджайи"),
      ("viloma","Viloma","Вилома-пранаяма"),
      ("pranayama","Pranayama","Пранаяма · общее"),
      ("agnisara","Agnisara Dhauti","Агнисара Дхаути"),
      ("shatkarma","Shatkarma","Шаткарма · очищение"),
      ("backbend","Backbends","Прогибы · общее"),
      ("hipjoint","Hip-Joint Mobility","Тазобедренный сустав"),
      ("hipopening","Hip-Joint Mobility","Тазобедренный сустав"),
      ("spinalalignment","Spinal Alignment","Выстраивание позвоночника"),
      ("asymmetric","Asymmetrical Asanas","Асимметричные асаны"),
    ]
    for frag, en, ru in fam:
        if frag in key: return (en, ru)
    return (a.strip(), a.strip())

general  = [t for t in corpus if not t.get("asana")]
specific = [t for t in corpus if t.get("asana")]
for t in specific:
    t["_a_en"], t["_a_ru"] = norm_asana(t["asana"])

RU = {}

def svg_glyph(inner, cls):
    return f'<svg viewBox="0 0 100 100" class="glyph {cls}" aria-hidden="true">{inner}</svg>'

def card(t):
    """Visual card: topic glyph + bold principle; prose folded into <details>."""
    i = t["id"]; topic = t["topic"]
    ru_lbl, en_lbl, accent = TOPIC.get(topic, ("", topic, "breath"))
    RU[f"badge_{topic}"] = ru_lbl
    tg = svg_glyph(G.TOPIC_GLYPH.get(topic, ""), f"tg-{accent}")
    RU[f"t{i}_p"] = esc(t["principle_ru"])
    body = [f'<article class="tcard reveal">',
            f'<div class="tc-top">{tg}'
            f'<span class="badge b-{accent}" data-i18n="badge_{topic}">{esc(en_lbl)}</span></div>',
            f'<p class="t-principle" data-i18n="t{i}_p">{esc(t["principle_en"])}</p>']
    detail = []
    if t.get("why_en"):
        RU[f"t{i}_w"] = esc(t.get("why_ru",""))
        detail.append(f'<p class="t-why"><span class="lbl" data-i18n="lbl_why">Why</span> '
                      f'<span data-i18n="t{i}_w">{esc(t["why_en"])}</span></p>')
    if t.get("mistake_en"):
        RU[f"t{i}_m"] = esc(t.get("mistake_ru",""))
        detail.append(f'<p class="t-mistake"><span class="lbl" data-i18n="lbl_mistake">Common mistake</span> '
                      f'<span data-i18n="t{i}_m">{esc(t["mistake_en"])}</span></p>')
    srcs = t.get("source_titles") or []
    if srcs:
        detail.append(f'<p class="t-src"><span class="lbl" data-i18n="lbl_source">Source</span> '
                      + " · ".join(esc(s) for s in srcs) + '</p>')
    if detail:
        body.append('<details class="t-more"><summary><span class="s-open" data-i18n="lbl_more">why · mistake</span>'
                    '<span class="s-close" data-i18n="lbl_less">hide</span></summary>'
                    '<div class="t-detail">' + "".join(detail) + '</div></details>')
    body.append('</article>')
    return "\n".join(body)

def topic_cards(topics):
    return "\n".join(card(t) for t in general if t["topic"] in topics)

def section(num, key, en_title, ru_title, en_lead, ru_lead, cards_html, diagram=""):
    RU[f"{key}_h2"] = ru_title
    RU[f"{key}_lead"] = ru_lead
    dg = f'<div class="concept-wrap reveal">{diagram}</div>' if diagram else ""
    return f'''<section id="{key}" class="wrap">
  <div class="sec-head reveal">
    <span class="sec-num">{num}</span>
    <h2 data-i18n="{key}_h2">{esc(en_title)}</h2>
  </div>
  <p class="lead reveal" data-i18n="{key}_lead">{esc(en_lead)}</p>
  {dg}
  <div class="tgrid">
{cards_html}
  </div>
</section>'''

sec_phil = section("01", "phil", "First principles",
    "С чего всё начинается",
    "Before any pose, a handful of refusals — the ground everything stands on: yoga is for you, not the reverse; the body is the instrument, the state is the goal.",
    "Ещё до любой асаны — несколько отказов, фундамент всего: йога для вас, а не вы для йоги; тело — инструмент, а цель — состояние.",
    topic_cards({"philosophy"}), diagram=G.CONCEPT["phil"])

sec_anat = section("02", "anat", "The logic of the body",
    "Логика тела",
    "His anatomy is a way of thinking, not a chart to memorize: muscles contract — never stretch; a joint is held by tone, not opened; everything moves in chains.",
    "Его анатомия — это способ мышления, а не схема для заучивания: мышцы сокращаются, а не растягиваются; сустав держится тонусом; всё движется цепочками.",
    topic_cards({"anatomy"}), diagram=G.CONCEPT["anat"])

sec_method = section("03", "method", "The method of practice",
    "Метод практики",
    "How to actually work on the mat: wholeness over isolation, balance over force, and earning the nervous system's trust rep by rep until it stops protecting you from yourself.",
    "Как на самом деле работать на коврике: целостность вместо изоляции, баланс вместо силы, доверие нервной системы, заработанное повтор за повтором.",
    topic_cards({"practice-method", "asana-technique"}), diagram=G.CONCEPT["method"])

sec_breath = section("04", "breath", "Breath and the locks",
    "Дыхание и бандхи",
    "Breath is the conductor; the locks are the fine tuning — the deep, quiet control that connects the center of the body to everything else.",
    "Дыхание — дирижёр; бандхи — тонкая настройка: глубокий тихий контроль, соединяющий центр тела со всем остальным.",
    topic_cards({"breath", "bandhas"}), diagram=G.CONCEPT["breath"])

# ---- asana library as a pose gallery -------------------------------------
groups = {}
for t in specific:
    groups.setdefault((t["_a_en"], t["_a_ru"]), []).append(t)
ordered = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0][0]))

tiles = []
for (a_en, a_ru), items in ordered:
    gid = "asana_" + "".join(c for c in a_en.lower() if c.isalnum())
    RU[gid] = a_ru
    cnt = len(items)
    glyph = svg_glyph(G.asana_glyph(a_en), "pose-glyph")
    RU["lbl_points"] = "техн."
    tiles.append(f'''<details class="pose reveal">
    <summary>
      <div class="pose-art">{glyph}</div>
      <div class="pose-meta">
        <span class="pose-name" data-i18n="{gid}">{esc(a_en)}</span>
        <span class="pose-count mono">{cnt} <span data-i18n="lbl_points">points</span></span>
      </div>
      <span class="pose-chev" aria-hidden="true">+</span>
    </summary>
    <div class="tgrid pose-cards">
{"".join(card(t) for t in items)}
    </div>
  </details>''')

RU["lib_h2"] = "Библиотека асан"
RU["lib_lead"] = ("Каждая асана, которую разбирает Анатолий, — рисунком. Нажми на позу, "
                  "чтобы раскрыть конкретные техники. Упорядочено по тому, сколько внимания он уделяет каждой.")
lib_section = f'''<section id="lib" class="wrap">
  <div class="sec-head reveal">
    <span class="sec-num">05</span>
    <h2 data-i18n="lib_h2">The asana library</h2>
  </div>
  <p class="lead reveal" data-i18n="lib_lead">Every asana Anatoly breaks down, drawn. Tap a pose to open its specific technique. Ordered by how much attention he gives each.</p>
  <div class="pose-gallery">
{"".join(tiles)}
  </div>
</section>'''

# ---- static UI + diagram strings -----------------------------------------
RU.update({
  "lbl_why":"Почему","lbl_mistake":"Частая ошибка","lbl_source":"Источник",
  "lbl_more":"почему · ошибка","lbl_less":"скрыть",
  "navBrand":"Метод · расшифровка","navHome":"Одна идея",
  "nav1":"Основы","nav2":"Тело","nav3":"Метод","nav4":"Дыхание","nav5":"Асаны",
  "heroEyebrow":"Учебный компаньон · Ишвара-йога",
  "heroSig":"145 видео → 219 наставлений · Анатолий Зенченко",
  "heroH1":'Тело — <span class="flow">инструмент</span>.<br>Цель — <span class="leg">состояние</span>.',
  "heroSub":'Всё, чему Анатолий учит на протяжении 145 занятий, держится на нескольких отказах: не тянуть, не «раскрывать» сустав силой, не воевать с телом. Двигайся балансом и сокращением, заслужи доверие нервной системы — и форма придёт сама.',
  "scrollCue":"↓ к наставлениям",
  "beamA":"Цепь A","beamB":"Цепь B","beamPivot":"баланс, а не сила",
  "s0h2":"Одна нить через всё",
  "s0lead1":'Пересмотри видео подряд — и сквозь все темы проходит одна мысль: <em>тело нужно не заставлять, а понимать.</em> Ни одно наставление не про то, как дотянуться дальше. Все — про то, как двигаться так, чтобы нервная система разрешила движение.',
  "s0thesis":'Не тяни. Не «раскрывай». <b>Балансируй</b> — и тело <s>перестанет защищаться</s> откроется само.',
  "s0lead2":'219 наставлений ниже — расшифровка канала Анатолия: основы и логика тела, метод практики, дыхание и бандхи, и библиотека техник по каждой асане. Переключай язык кнопкой вверху справа.',
  # concept diagram captions
  "dgm_p1":"йога служит вам","dgm_p2":"тело → состояние","dgm_p3":"расширяйся изнутри",
  "dgm_a1":"сокращение, а не растяжение","dgm_a2":"сустав держится тонусом","dgm_a3":"всё движется цепочками",
  "dgm_b1":"Джаландхара · горло","dgm_bd":"диафрагма · дирижёр","dgm_b2":"Уддияна · пупок","dgm_b3":"Мула · тазовое дно",
  "dgm_m1":"уравновесь две цепочки — 50 / 50","dgm_m2":"трапеция → квадрат (нутация)",
  "footerBody":('<b>Источник</b> · 145 видео с YouTube-канала Анатолия Зенченко (Ишвара Йога), расшифрованы локально.<br>'
                '<b>Метод</b> · субтитры и Whisper large-v3 → 219 наставлений, сведённых по темам и асанам.<br>'
                '<b>Примечание</b> · это учебное прочтение слов твоего учителя — не медицинская рекомендация. Если сомневаешься — спроси Анатолия на коврике.'),
})

RU_JSON = json.dumps(RU, ensure_ascii=True, indent=0)

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Тело — инструмент. Цель — состояние. — Anatoly Zenchenko's method, decoded</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Spectral:ital,wght@0,300;0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{{
    --ink:#0A1E24; --ink-2:#0E262E; --ink-3:#123039;
    --breath:#63C2CE; --amber:#E9A23B; --coral:#E56B4E;
    --paper:#F3EDE1; --paper-ink:#1A2A2E; --mute:#89A2A8; --mute-2:#5C777D;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html{{scroll-behavior:smooth}}
  body{{background:var(--ink);color:#DCE7E8;font-family:"Spectral",Georgia,serif;font-weight:400;
    font-size:clamp(16px,1.05vw,18px);line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
  .mono{{font-family:"IBM Plex Mono",monospace}}
  h1,h2,h3,.disp{{font-family:"Space Grotesk",sans-serif}}
  ::selection{{background:var(--amber);color:var(--ink)}}
  a{{color:var(--breath);text-underline-offset:3px}}
  .wrap{{max-width:1120px;margin:0 auto;padding:0 28px}}
  .eyebrow{{font-family:"IBM Plex Mono",monospace;font-size:.72rem;letter-spacing:.28em;
    text-transform:uppercase;color:var(--breath);font-weight:500}}

  /* language toggle */
  .lang-toggle{{position:fixed;top:16px;right:16px;z-index:40;display:flex;gap:2px;
    background:rgba(10,30,36,.82);backdrop-filter:blur(8px);border:1px solid var(--ink-3);border-radius:3px;padding:3px}}
  .lang-btn{{font-family:"IBM Plex Mono",monospace;font-size:.72rem;letter-spacing:.14em;color:var(--mute);
    background:transparent;border:0;cursor:pointer;padding:6px 11px;border-radius:2px;transition:color .2s,background .2s}}
  .lang-btn:hover{{color:#DCE7E8}}
  .lang-btn[aria-pressed="true"]{{background:var(--amber);color:var(--ink);font-weight:600}}
  .lang-btn:focus-visible{{outline:2px solid var(--breath);outline-offset:2px}}

  /* sticky nav */
  .nav{{position:sticky;top:0;z-index:30;background:rgba(10,30,36,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--ink-3)}}
  .nav-inner{{max-width:1120px;margin:0 auto;padding:11px 28px;display:flex;align-items:center;gap:22px;overflow-x:auto;scrollbar-width:none}}
  .nav-inner::-webkit-scrollbar{{display:none}}
  .nav-brand{{font-family:"Space Grotesk";font-weight:600;font-size:.9rem;color:#EFF5F5;white-space:nowrap;flex:none}}
  .nav a{{font-family:"IBM Plex Mono";font-size:.74rem;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);
    text-decoration:none;white-space:nowrap;transition:color .2s}}
  .nav a:hover,.nav a.active{{color:var(--amber)}}
  .nav a.nav-home{{color:var(--breath);flex:none}}
  .nav a.nav-home::before{{content:"← "}}
  .nav a.nav-home:hover{{color:var(--amber)}}

  /* blueprint grid */
  .grid-bg{{position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.5;
    background-image:linear-gradient(var(--ink-3) 1px,transparent 1px),linear-gradient(90deg,var(--ink-3) 1px,transparent 1px);
    background-size:44px 44px;
    -webkit-mask-image:radial-gradient(ellipse 80% 70% at 50% 24%,#000 40%,transparent 100%);
            mask-image:radial-gradient(ellipse 80% 70% at 50% 24%,#000 40%,transparent 100%)}}
  main{{position:relative;z-index:1}}

  /* hero */
  .hero{{min-height:92svh;display:flex;flex-direction:column;justify-content:center;padding:64px 0 52px}}
  .hero-top{{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:12px;margin-bottom:auto}}
  .sig{{font-family:"IBM Plex Mono";font-size:.72rem;letter-spacing:.2em;color:var(--mute)}}
  .hero h1{{font-size:clamp(2.5rem,7vw,5.6rem);line-height:1;font-weight:600;letter-spacing:-.02em;color:#F3EDE1;margin:.35em 0 .1em}}
  .hero h1 .flow{{color:var(--breath)}} .hero h1 .leg{{color:var(--amber);white-space:nowrap}}
  .hero-sub{{max-width:56ch;font-size:1.16rem;color:#B9CBCD;font-weight:300;margin-top:.6em}}
  .beam-wrap{{margin-top:40px;width:100%}}
  .beam-wrap svg{{width:100%;max-width:760px;height:auto;display:block;margin:0 auto;overflow:visible}}
  .beam-arm{{stroke:var(--breath);stroke-width:3;stroke-linecap:round}}
  .beam-col{{stroke:var(--ink-3);stroke-width:2}}
  .beam-pan{{stroke-width:2.5;fill:none}} .pan-a{{stroke:var(--breath)}} .pan-b{{stroke:var(--amber)}}
  .beam-g{{transform-box:fill-box;transform-origin:center;animation:settle 2.6s cubic-bezier(.34,1.2,.4,1) .3s both}}
  @keyframes settle{{0%{{transform:rotate(9deg)}}60%{{transform:rotate(-4deg)}}100%{{transform:rotate(0)}}}}
  .beam-lbl{{font-family:"IBM Plex Mono";font-size:14px;letter-spacing:.05em;fill:var(--mute)}}
  .beam-pivot-lbl{{font-family:"IBM Plex Mono";font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;fill:var(--amber)}}
  .scroll-cue{{margin-top:34px;font-family:"IBM Plex Mono";font-size:.72rem;letter-spacing:.2em;color:var(--mute-2);text-transform:uppercase}}

  /* sections */
  section{{padding:70px 0}}
  .sec-head{{display:flex;gap:18px;align-items:baseline;margin-bottom:26px}}
  .sec-num{{font-family:"IBM Plex Mono";font-size:.8rem;color:var(--amber);border:1px solid var(--ink-3);border-radius:2px;padding:4px 8px;flex:none}}
  .sec-head h2{{font-size:clamp(1.7rem,3.6vw,2.7rem);font-weight:600;letter-spacing:-.015em;line-height:1.05;color:#EFF5F5}}
  .lead{{max-width:70ch;font-size:1.12rem;color:#C3D2D4;font-weight:300;margin-bottom:8px}}
  .lead em{{color:var(--breath);font-style:italic}}
  .thesis{{border-left:2px solid var(--amber);padding:6px 0 6px 26px;margin:36px 0;max-width:62ch}}
  .thesis .k{{font-family:"Space Grotesk";font-size:clamp(1.4rem,3vw,2rem);font-weight:500;line-height:1.25;color:#F3EDE1}}
  .thesis .k b{{color:var(--amber);font-weight:600}} .thesis .k s{{color:var(--coral);text-decoration-thickness:2px}}

  /* concept diagrams (section heroes) */
  .concept-wrap{{margin:30px 0 8px;padding:26px 20px;background:var(--ink-2);border:1px solid var(--ink-3);border-radius:6px}}
  svg.concept{{width:100%;height:auto;display:block;overflow:visible;margin:0 auto}}
  svg.concept[viewBox="0 0 300 360"]{{max-width:340px}}
  .c-bone{{fill:none;stroke:#3D5760;stroke-width:2.5;stroke-linecap:round}}
  .c-musc{{fill:none;stroke:var(--amber);stroke-width:3.5;stroke-linecap:round}}
  .c-flow{{fill:none;stroke:var(--breath);stroke-width:3;stroke-linecap:round}}
  .c-node{{fill:var(--breath)}}
  .c-arrow{{fill:none;stroke:var(--amber);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}}
  .c-arrow-big{{fill:none;stroke:var(--amber);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}}
  .c-body{{fill:rgba(99,194,206,.05);stroke:#3D5760;stroke-width:2}}
  .c-lock{{fill:none;stroke:var(--amber);stroke-width:3;stroke-linecap:round}}
  .c-dot{{fill:var(--amber)}}
  .c-diaph{{fill:none;stroke:var(--breath);stroke-width:3.5;stroke-linecap:round}}
  .c-lift{{stroke:var(--breath);stroke-width:1.5;opacity:.7}}
  .c-lbl{{font-family:"IBM Plex Mono";font-size:13px;fill:var(--mute)}}
  .c-lbl-breath{{fill:var(--breath)}}
  .c-cap{{font-family:"IBM Plex Mono";font-size:13px;letter-spacing:.04em;fill:var(--mute)}}
  .c-beam{{stroke:var(--breath);stroke-width:3;stroke-linecap:round}}
  .c-amber{{fill:none;stroke:var(--amber);stroke-width:2.5}}
  .c-bad{{fill:none;stroke:var(--coral);stroke-width:2.5}}
  .c-good{{fill:none;stroke:var(--breath);stroke-width:2.5}}

  /* glyphs */
  .glyph{{display:block}}
  .glyph .gl{{fill:none;stroke:currentColor;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}}
  .glyph .gh{{fill:currentColor;stroke:none}}
  .glyph .ga{{fill:none;stroke:currentColor;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}}
  .glyph .gl-dim{{opacity:.4}}
  .tg-breath{{color:var(--breath)}} .tg-amber{{color:var(--amber)}} .tg-coral{{color:var(--coral)}}

  /* teaching cards */
  .tgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1px;
    background:var(--ink-3);border:1px solid var(--ink-3);border-radius:4px;overflow:hidden}}
  .tcard{{background:var(--ink-2);padding:20px 20px 16px;display:flex;flex-direction:column;gap:12px;
    position:relative;transition:background .2s}}
  .tcard::after{{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:transparent;transition:background .2s}}
  .tcard:hover{{background:#102C35}}
  .tcard:hover.tcard::after,.tcard:hover::after{{background:var(--breath)}}
  .tc-top{{display:flex;align-items:center;gap:13px}}
  .tc-top .glyph{{width:34px;height:34px;flex:none;padding:9px;border-radius:50%;
    background:rgba(99,194,206,.09);border:1px solid var(--ink-3);box-sizing:content-box}}
  .tc-top .tg-amber{{background:rgba(233,162,59,.1)}} .tc-top .tg-coral{{background:rgba(229,107,78,.1)}}
  .badge{{font-family:"IBM Plex Mono";font-size:.62rem;letter-spacing:.16em;text-transform:uppercase;
    padding:3px 8px;border-radius:2px;border:1px solid currentColor}}
  .b-breath{{color:var(--breath)}} .b-amber{{color:var(--amber)}} .b-coral{{color:var(--coral)}}
  .t-principle{{font-family:"Space Grotesk";font-size:1.08rem;font-weight:500;line-height:1.36;color:#EFF5F5;letter-spacing:-.005em}}
  .t-more{{margin-top:auto;padding-top:14px}}
  .t-more summary{{list-style:none;cursor:pointer;font-family:"IBM Plex Mono";font-size:.66rem;letter-spacing:.14em;
    text-transform:uppercase;color:var(--breath);
    display:inline-flex;align-items:center;gap:7px;transition:all .2s;
    padding:6px 12px 6px 8px;border:1px solid rgba(99,194,206,.35);border-radius:999px;
    background:rgba(99,194,206,.07)}}
  .t-more summary::-webkit-details-marker{{display:none}}
  .t-more summary::before{{content:"+";display:inline-flex;align-items:center;justify-content:center;
    width:16px;height:16px;border-radius:50%;background:var(--amber);color:var(--ink);
    font-weight:700;font-size:.8rem;line-height:1}}
  .t-more[open] summary::before{{content:"–"}}
  .t-more summary:hover{{color:#EFF5F5;border-color:var(--breath);background:rgba(99,194,206,.16)}}
  .t-more[open] summary{{color:var(--mute);border-color:var(--ink-3);background:transparent}}
  .t-more .s-close{{display:none}} .t-more[open] .s-open{{display:none}} .t-more[open] .s-close{{display:inline}}
  .t-detail{{padding-top:12px;display:flex;flex-direction:column;gap:10px;
    animation:fade .35s ease}}
  @keyframes fade{{from{{opacity:0;transform:translateY(-4px)}}to{{opacity:1;transform:none}}}}
  .t-why,.t-mistake{{font-size:.94rem;font-weight:300;line-height:1.55;color:#AFC2C4}}
  .t-why .lbl,.t-mistake .lbl,.t-src .lbl{{font-family:"IBM Plex Mono";font-size:.6rem;letter-spacing:.14em;
    text-transform:uppercase;margin-right:4px}}
  .t-why .lbl{{color:var(--breath)}} .t-mistake{{color:#C7B0A6}} .t-mistake .lbl{{color:var(--coral)}}
  .t-src{{font-family:"IBM Plex Mono";font-size:.66rem;line-height:1.5;color:var(--mute-2)}} .t-src .lbl{{color:var(--mute)}}

  /* pose gallery */
  .pose-gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(178px,1fr));gap:14px}}
  details.pose{{background:var(--ink-2);border:1px solid var(--ink-3);border-radius:6px;overflow:hidden;
    transition:border-color .25s}}
  details.pose:hover{{border-color:rgba(99,194,206,.4)}}
  details.pose[open]{{grid-column:1/-1;border-color:var(--amber)}}
  details.pose summary{{list-style:none;cursor:pointer;padding:20px 18px 16px;display:flex;flex-direction:column;
    align-items:center;gap:12px;position:relative}}
  details.pose summary::-webkit-details-marker{{display:none}}
  .pose-art{{width:100%;max-width:120px}}
  .pose-art .glyph{{width:100%;height:auto;color:var(--breath)}}
  details.pose[open] .pose-art .glyph{{color:var(--amber)}}
  .pose-meta{{display:flex;flex-direction:column;align-items:center;gap:3px;text-align:center}}
  .pose-name{{font-family:"Space Grotesk";font-weight:600;font-size:.98rem;color:#EFF5F5;line-height:1.2}}
  .pose-count{{font-size:.64rem;letter-spacing:.12em;text-transform:uppercase;color:var(--amber)}}
  .pose-chev{{position:absolute;top:12px;right:14px;font-family:"IBM Plex Mono";color:var(--mute);font-size:1.1rem;transition:transform .25s,color .2s}}
  details.pose[open] .pose-chev{{transform:rotate(45deg);color:var(--amber)}}
  details.pose summary:hover .pose-chev{{color:#DCE7E8}}
  .pose-cards{{margin:0 14px 16px;border-radius:4px}}
  details.pose[open] summary{{border-bottom:1px solid var(--ink-3);margin-bottom:16px}}

  /* footer */
  footer{{padding:56px 0 90px;border-top:1px solid var(--ink-3);color:var(--mute)}}
  footer .mono{{font-size:.78rem;letter-spacing:.06em;line-height:1.85}} footer b{{color:#C3D2D4;font-weight:600}}

  .reveal{{opacity:0;transform:translateY(20px);transition:opacity .6s ease,transform .6s ease}}
  .reveal.in{{opacity:1;transform:none}}

  @media(max-width:720px){{
    .wrap{{padding:0 20px}} section{{padding:52px 0}} .sec-head{{flex-direction:column;gap:10px}}
    .hero{{padding-left:28px;padding-right:28px}} .hero-sub{{font-size:1.04rem}} .lead{{font-size:1.02rem}}
    .tgrid{{grid-template-columns:1fr}} .nav-inner{{padding:10px 20px;gap:16px}}
    .pose-gallery{{grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}}
    .concept-wrap{{padding:18px 12px}}
  }}
  @media(max-width:480px){{
    .lang-toggle{{top:10px;right:10px}} .hero h1{{font-size:clamp(2rem,9vw,3rem)}} .beam-lbl{{font-size:16px}}
    .pose-gallery{{grid-template-columns:1fr 1fr}}
  }}
  @media(prefers-reduced-motion:reduce){{*{{animation:none!important;scroll-behavior:auto!important}}
    .beam-g{{transform:none}} .reveal{{opacity:1;transform:none;transition:none}}}}
  .no-js .reveal{{opacity:1;transform:none}}
</style>
</head>
<body class="no-js">
<script>document.body.classList.remove('no-js');</script>
<div class="grid-bg" aria-hidden="true"></div>

<div class="lang-toggle" role="group" aria-label="Language / Язык">
  <button class="lang-btn" data-lang="en" aria-pressed="false">EN</button>
  <button class="lang-btn" data-lang="ru" aria-pressed="true">RU</button>
</div>

<nav class="nav">
  <div class="nav-inner">
    <span class="nav-brand" data-i18n="navBrand">The method · decoded</span>
    <a class="nav-home" href="index.html" data-i18n="navHome">The one idea</a>
    <a href="#phil" data-i18n="nav1">Foundations</a>
    <a href="#anat" data-i18n="nav2">Body</a>
    <a href="#method" data-i18n="nav3">Method</a>
    <a href="#breath" data-i18n="nav4">Breath</a>
    <a href="#lib" data-i18n="nav5">Asanas</a>
  </div>
</nav>

<main>

<header class="hero wrap">
  <div class="hero-top">
    <span class="eyebrow" data-i18n="heroEyebrow">Study companion · Ishvara Yoga</span>
    <span class="sig" data-i18n="heroSig">145 videos → 219 teachings · Anatoly Zenchenko</span>
  </div>
  <h1 data-i18n="heroH1">The body is the <span class="flow">instrument</span>.<br>The goal is a <span class="leg">state</span>.</h1>
  <p class="hero-sub" data-i18n="heroSub">Everything Anatoly teaches across 145 lessons rests on a few refusals: don't stretch, don't force a joint open, don't fight your body. Move by balance and contraction, earn the nervous system's trust — and the shape arrives on its own.</p>

  <div class="beam-wrap" aria-label="Schematic: a balance beam — roughly half the body's musculature forms one chain, the opposing half the other; the practice is to balance them, not to force.">
    <svg viewBox="0 0 760 240" role="img">
      <line x1="60" y1="210" x2="700" y2="210" class="beam-col" stroke-dasharray="4 6"/>
      <polygon points="380,150 360,205 400,205" fill="none" stroke="#89A2A8" stroke-width="2"/>
      <text x="380" y="232" text-anchor="middle" class="beam-pivot-lbl" data-i18n="beamPivot">balance, not force</text>
      <g class="beam-g">
        <line x1="120" y1="120" x2="640" y2="120" class="beam-arm"/>
        <line x1="120" y1="120" x2="120" y2="86" class="beam-col"/>
        <line x1="640" y1="120" x2="640" y2="86" class="beam-col"/>
        <path class="beam-pan pan-a" d="M88 86 h64 l-14 34 h-36 z"/>
        <path class="beam-pan pan-b" d="M608 86 h64 l-14 34 h-36 z"/>
        <circle cx="380" cy="120" r="6" fill="#E9A23B"/>
        <text x="120" y="66" text-anchor="middle" class="beam-lbl" data-i18n="beamA">Chain A</text>
        <text x="640" y="66" text-anchor="middle" class="beam-lbl" data-i18n="beamB">Chain B</text>
      </g>
    </svg>
  </div>
  <p class="scroll-cue" data-i18n="scrollCue">↓ read the teachings</p>
</header>

<section id="through" class="wrap reveal">
  <div class="sec-head">
    <span class="sec-num">00</span>
    <h2 data-i18n="s0h2">One thread through all of it</h2>
  </div>
  <p class="lead" data-i18n="s0lead1">Watch the videos in sequence and one idea keeps returning across every topic: <em>the body is not to be forced, but understood.</em> No instruction is about reaching further. Every one is about moving so that the nervous system permits the movement.</p>
  <div class="thesis">
    <div class="k" data-i18n="s0thesis">Don't stretch. Don't "open." <b>Balance</b> — and the body <s>stops defending itself</s> opens on its own.</div>
  </div>
  <p class="lead" data-i18n="s0lead2">The 219 teachings below decode Anatoly's channel: first principles and the logic of the body, then the method of practice, breath and the locks, and a library of specific technique for each asana. Switch languages with the toggle at top right.</p>
</section>

{sec_phil}

{sec_anat}

{sec_method}

{sec_breath}

{lib_section}

<footer class="wrap">
  <p class="mono" data-i18n="footerBody">
    <b>Source</b> · 145 videos from Anatoly Zenchenko's YouTube channel (Ishvara Yoga), transcribed locally.<br>
    <b>Method</b> · captions + Whisper large-v3 → 219 teachings, aggregated by theme and asana.<br>
    <b>Note</b> · a study reading of your teacher's direction — not medical advice. When in doubt, ask Anatoly on the mat.
  </p>
</footer>

</main>
<script>
  const io = new IntersectionObserver((es)=>{{
    es.forEach(e=>{{ if(e.isIntersecting){{ e.target.classList.add('in'); io.unobserve(e.target);}} }});
  }},{{threshold:.08, rootMargin:'0px 0px -6% 0px'}});
  document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

  const navLinks = [...document.querySelectorAll('.nav a')].filter(a=>a.getAttribute('href').startsWith('#'));
  const secs = navLinks.map(a=>document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const navIo = new IntersectionObserver((es)=>{{
    es.forEach(e=>{{ if(e.isIntersecting){{
      const id = '#'+e.target.id;
      navLinks.forEach(a=>a.classList.toggle('active', a.getAttribute('href')===id));
    }} }});
  }},{{rootMargin:'-45% 0px -50% 0px'}});
  secs.forEach(s=>navIo.observe(s));

  const RU = {RU_JSON};
  const SVGNS = "http://www.w3.org/2000/svg";
  const orig = {{}};
  function apply(lang){{
    document.querySelectorAll('[data-i18n]').forEach(el=>{{
      const k = el.getAttribute('data-i18n');
      const isSvg = el.namespaceURI === SVGNS;
      if(!(k in orig)) orig[k] = isSvg ? el.textContent : el.innerHTML;
      const val = lang === 'ru' ? RU[k] : orig[k];
      if(val == null) return;
      if(isSvg) el.textContent = val; else el.innerHTML = val;
    }});
    document.documentElement.lang = lang;
    document.querySelectorAll('.lang-btn').forEach(b=>b.setAttribute('aria-pressed', String(b.dataset.lang === lang)));
    try{{ localStorage.setItem('yoga-lang', lang); }}catch(e){{}}
  }}
  document.querySelectorAll('.lang-btn').forEach(b=>b.addEventListener('click', ()=>apply(b.dataset.lang)));
  let saved = 'ru';
  try{{ saved = localStorage.getItem('yoga-lang') || 'ru'; }}catch(e){{}}
  apply(saved);
</script>
</body>
</html>'''

out_path = os.path.join(BASE, "companion.html")
open(out_path, "w", encoding="utf-8").write(HTML)
print("wrote", out_path, len(HTML), "bytes")
print("RU keys:", len(RU), "| general", len(general), "specific", len(specific), "poses", len(groups))
