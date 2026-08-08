import json, os, subprocess, sys, time, glob

KEEP = json.load(open("/Users/gblazer/workspace/voice/captions/keep.json"))
OUT = "/Users/gblazer/workspace/voice/captions"
YTDLP = ["/Users/gblazer/workspace/voice/.venv/bin/python", "-m", "yt_dlp"]

# YouTube now gates auto-captions behind PO tokens; the web client + bgutil
# token server (docker, :4416) mints both the gvs and subs tokens. json3 gives
# discrete caption events, so no rolling-overlap dedup is needed (unlike VTT).
COMMON = [
    "--skip-download", "--write-auto-subs",
    "--sub-langs", "ru-ru,ru",          # real ASR track (ru-ru preferred, ru fallback)
    "--sub-format", "json3",
    "--extractor-args", "youtube:player_client=web",
    "--ignore-no-formats-error",        # web client has no A/V formats; we only want subs
    "--no-warnings",
]

def json3_to_text(path):
    """Concatenate caption events into flowing text. Returns (text, n_events)."""
    d = json.load(open(path, encoding="utf-8"))
    events = d.get("events", [])
    parts = []
    for e in events:
        for seg in e.get("segs", []):
            t = seg.get("utf8", "")
            if t and t != "\n":
                parts.append(t)
    text = "".join(parts)
    text = " ".join(text.split())     # normalize whitespace
    return text, len(events)

done = failed = skipped = whisper_queue_n = 0
whisper_queue = []

for i, v in enumerate(KEEP, 1):
    vid, title = v["id"], v["title"]
    txt_path = os.path.join(OUT, f"{vid}.txt")
    if os.path.exists(txt_path):
        skipped += 1
        print(f"[{i}/{len(KEEP)}] cached {vid}", flush=True)
        continue

    tmpl = os.path.join(OUT, f"{vid}.%(ext)s")
    for f in glob.glob(os.path.join(OUT, f"{vid}.*.json3")):
        os.remove(f)
    cmd = YTDLP + COMMON + ["-o", tmpl, f"https://www.youtube.com/watch?v={vid}"]
    try:
        subprocess.run(cmd, capture_output=True, timeout=120)
    except Exception as e:
        print(f"[{i}/{len(KEEP)}] ERROR {vid}: {e}", flush=True)
        failed += 1
        continue

    js = None
    for f in sorted(glob.glob(os.path.join(OUT, f"{vid}.*.json3"))):
        js = f
        break
    if not js:
        print(f"[{i}/{len(KEEP)}] NO CAPTION -> whisper | {title}", flush=True)
        whisper_queue.append(v); whisper_queue_n += 1
        continue

    text, n_events = json3_to_text(js)
    os.remove(js)
    # Placeholder tracks are a single title-card event (or a stub <200 chars).
    if n_events <= 2 or len(text) < 200:
        print(f"[{i}/{len(KEEP)}] PLACEHOLDER ({n_events}ev) -> whisper | {title}", flush=True)
        whisper_queue.append(v); whisper_queue_n += 1
        continue

    with open(txt_path, "w", encoding="utf-8") as fh:
        fh.write(f"# {title}\n# https://youtu.be/{vid}\n\n{text}\n")
    done += 1
    print(f"[{i}/{len(KEEP)}] OK {vid} ({len(text)} chars, {n_events}ev) | {title}", flush=True)
    time.sleep(1.0)

json.dump(whisper_queue, open(os.path.join(OUT, "whisper_queue.json"), "w"),
          ensure_ascii=False, indent=2)
print(f"\nDONE  captions={done} cached={skipped} whisper_needed={whisper_queue_n} failed={failed}", flush=True)
