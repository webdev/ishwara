import glob, json, os, sys, time
import mlx_whisper

MODEL = "mlx-community/whisper-large-v3-mlx"
CHATS = "/Users/gblazer/workspace/voice/chats"
OUT = "/Users/gblazer/workspace/voice/transcripts"
os.makedirs(OUT, exist_ok=True)

files = sorted(glob.glob(os.path.join(CHATS, "*.opus")))
print(f"{len(files)} opus files", flush=True)

results = {}
for i, f in enumerate(files, 1):
    base = os.path.basename(f)
    txt_path = os.path.join(OUT, base + ".txt")
    if os.path.exists(txt_path):
        with open(txt_path) as fh:
            results[base] = fh.read()
        print(f"[{i}/{len(files)}] cached {base}", flush=True)
        continue
    t0 = time.time()
    try:
        r = mlx_whisper.transcribe(f, path_or_hf_repo=MODEL, language="ru")
        text = r["text"].strip()
    except Exception as e:
        text = f"[ERROR: {e}]"
    with open(txt_path, "w") as fh:
        fh.write(text)
    results[base] = text
    print(f"[{i}/{len(files)}] {base} ({time.time()-t0:.0f}s, {len(text)} chars)", flush=True)

with open(os.path.join(OUT, "_all.json"), "w") as fh:
    json.dump(results, fh, ensure_ascii=False, indent=2)
print("DONE", flush=True)
