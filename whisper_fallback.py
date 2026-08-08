import json, os, glob, subprocess, sys

OUT = "/Users/gblazer/workspace/voice/captions"
AUD = os.path.join(OUT, "audio")
os.makedirs(AUD, exist_ok=True)
YTDLP = ["/Users/gblazer/workspace/voice/.venv/bin/python", "-m", "yt_dlp"]
MODEL = "mlx-community/whisper-large-v3-turbo"

QUEUE = json.load(open(os.path.join(OUT, "whisper_queue.json")))
import mlx_whisper

done = failed = skipped = 0
for i, v in enumerate(QUEUE, 1):
    vid, title = v["id"], v["title"]
    txt_path = os.path.join(OUT, f"{vid}.txt")
    if os.path.exists(txt_path):
        skipped += 1
        print(f"[{i}/{len(QUEUE)}] cached {vid}", flush=True)
        continue

    mp3 = os.path.join(AUD, f"{vid}.mp3")
    if not os.path.exists(mp3):
        cmd = YTDLP + ["-f", "bestaudio/best", "-x", "--audio-format", "mp3",
                       "--audio-quality", "5", "--no-warnings",
                       "-o", os.path.join(AUD, f"{vid}.%(ext)s"),
                       f"https://www.youtube.com/watch?v={vid}"]
        try:
            subprocess.run(cmd, capture_output=True, timeout=300)
        except Exception as e:
            print(f"[{i}/{len(QUEUE)}] DL-ERR {vid}: {e}", flush=True)
            failed += 1
            continue
    if not os.path.exists(mp3):
        print(f"[{i}/{len(QUEUE)}] NO AUDIO {vid} | {title}", flush=True)
        failed += 1
        continue

    try:
        r = mlx_whisper.transcribe(mp3, path_or_hf_repo=MODEL, language="ru")
        text = " ".join(r["text"].split())
    except Exception as e:
        print(f"[{i}/{len(QUEUE)}] ASR-ERR {vid}: {e}", flush=True)
        failed += 1
        continue

    if len(text) < 200:
        print(f"[{i}/{len(QUEUE)}] TOO-SHORT {vid} ({len(text)}c) | {title}", flush=True)
        failed += 1
        continue

    with open(txt_path, "w", encoding="utf-8") as fh:
        fh.write(f"# {title}\n# https://youtu.be/{vid}\n# [whisper]\n\n{text}\n")
    os.remove(mp3)   # reclaim space
    done += 1
    print(f"[{i}/{len(QUEUE)}] OK {vid} ({len(text)} chars) | {title}", flush=True)

print(f"\nWHISPER DONE  transcribed={done} cached={skipped} failed={failed}", flush=True)
