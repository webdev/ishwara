import re, os, json

CHAT = "/Users/gblazer/workspace/voice/chats/_chat.txt"
TRANS = "/Users/gblazer/workspace/voice/transcripts"

def load_txt(base):
    p = os.path.join(TRANS, base + ".txt")
    return open(p).read().strip() if os.path.exists(p) else ""

line_re = re.compile(r"^‎?\[(\d+)/(\d+)/(\d+), (\d+):(\d+):(\d+)\s*([AP]M)\] ([^:]+): ‎?(.*)$")
att_re = re.compile(r"<attached:\s*([^>]+)>")

entries = []
cur = None
with open(CHAT, encoding="utf-8") as f:
    for raw in f:
        line = raw.rstrip("\n")
        m = line_re.match(line)
        if m:
            mo, d, yy, h, mm, ss, ap, sender, msg = m.groups()
            att = att_re.search(msg)
            base = att.group(1).strip() if att else None
            kind = None
            text = msg
            audio = photo = None
            if base and base.endswith(".opus"):
                kind = "audio"; audio = base
                text = load_txt(base)
            elif base and base.lower().endswith((".jpg", ".jpeg", ".png")):
                kind = "photo"; photo = base
                text = re.sub(r"‎?<attached:[^>]+>", "", msg).strip() or "[photo]"
            elif "audio omitted" in msg:
                kind = "audio_missing"; text = ""
            elif "image omitted" in msg:
                kind = "photo_missing"; text = ""
            entry = {"mo": int(mo), "d": int(d), "yy": int(yy),
                     "time_str": f"{h}:{mm}:{ss} {ap}",
                     "sender": sender.strip(), "text": text,
                     "audio": audio, "photo": photo, "kind": kind}
            entries.append(entry); cur = entry
        elif cur is not None and line.strip():
            if cur["kind"] not in ("audio", "photo", "audio_missing", "photo_missing"):
                cur["text"] += "\n" + line

n_audio = sum(1 for e in entries if e["audio"])
n_photo = sum(1 for e in entries if e["photo"])
print(f"entries={len(entries)} audio={n_audio} photo={n_photo} "
      f"audio_missing={sum(1 for e in entries if e['kind']=='audio_missing')}")

json.dump(entries, open(os.path.join(TRANS, "_dialogue.json"), "w"), ensure_ascii=False, indent=2)

with open(os.path.join(TRANS, "_dialogue.txt"), "w", encoding="utf-8") as f:
    for e in entries:
        who = "GEORGE" if "George" in e["sender"] else "TEACHER"
        if e["audio"]: tag = " 🎤"
        elif e["photo"]: tag = " 📷"
        elif e["kind"] == "audio_missing": tag = " [audio not in export]"
        else: tag = ""
        f.write(f"[{e['mo']}/{e['d']}/{e['yy']} {e['time_str']}] {who}{tag}: {e['text']}\n\n")
print("wrote dialogue files")
