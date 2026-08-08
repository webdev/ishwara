import re, json

rows = []
with open("/tmp/vidlist.tsv", encoding="utf-8") as f:
    for line in f:
        parts = line.rstrip("\n").split("\\t")  # yt-dlp wrote literal backslash-t
        if len(parts) < 2:
            continue
        vid, title = parts[0], parts[1]
        dur = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        rows.append((vid, title, dur))

# Anatoly is the author; his instructional videos carry his name.
ANATOLY = re.compile(r"Зенченко|Зенченк", re.I)

# Non-instructional: promos, tours, teacher-course invites, business livestreams,
# interviews, generic branding clips.
EXCLUDE = re.compile(
    r"Прямой эфир|Приглашен|Приглаше|курс подготовк|подготовк|преподавател|"
    r"Обучение инструктор|семинар с|Йога-тур|тур с|Выездн|Интервью|Інтерв|"
    r"Online-занятия|Online-заняття|автор методики|о курсе|о преподавател|"
    r"Как стать успешным|показательн",
    re.I,
)

keep, drop = [], []
for vid, title, dur in rows:
    is_anatoly = bool(ANATOLY.search(title))
    is_excluded = bool(EXCLUDE.search(title))
    # Very short clips (<40s) are almost always promos/teasers.
    too_short = dur and dur < 40
    if is_anatoly and not is_excluded and not too_short:
        keep.append((vid, title, dur))
    else:
        drop.append((vid, title, dur))

keep.sort(key=lambda r: -r[2])  # longest (most instructional) first
print(f"TOTAL={len(rows)}  KEEP={len(keep)}  DROP={len(drop)}")
print(f"KEEP total minutes: {sum(r[2] for r in keep)//60}")
print("\n===== KEEP (Anatoly instructional) =====")
for vid, title, dur in keep:
    print(f"{dur//60:>3}m  {vid}  {title}")

json.dump([{"id": v, "title": t, "dur": d} for v, t, d in keep],
          open("/Users/gblazer/workspace/voice/captions/keep.json", "w"),
          ensure_ascii=False, indent=2)
