#!/usr/bin/env python3
"""Génère favicon sg. via Gemini."""
import os, json, base64, urllib.request, urllib.error

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
OUT = "/Users/quirineric/Desktop/Claude/boutik-saas/assets/favicon-sg.png"

PROMPT = """Square brand mark, 512x512.
Background: pure black #08090B.
Centered text "sg." in ULTRA bold heavy sans-serif (think Satoshi Black 900).
The "sg" letters are in pure white #FFFFFF.
The dot "." after sg is in vivid amber/orange #F59E0B.
Lowercase letters, tight letter-spacing (-3%).
The text fills about 60% of the canvas height, perfectly centered.
Premium tech minimal aesthetic (think Linear, Vercel, Notion favicons).
NO other elements, NO frame, NO decoration. Just the text "sg." on black background.
Output as a clean square PNG.
"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
payload = {"contents": [{"parts": [{"text": PROMPT}]}], "generationConfig": {"responseModalities": ["IMAGE"]}}
data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=300) as resp:
        body = json.loads(resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    body = json.loads(e.read().decode("utf-8"))
    print(f"HTTP {e.code}: {json.dumps(body, indent=2)[:600]}")
    exit(1)

for part in body.get("candidates", [{}])[0].get("content", {}).get("parts", []):
    if "inlineData" in part or "inline_data" in part:
        d = part.get("inlineData") or part.get("inline_data")
        img = base64.b64decode(d["data"])
        with open(OUT, "wb") as f: f.write(img)
        print(f"✓ {os.path.basename(OUT)} ({len(img)//1024} KB)")
        exit(0)
print(f"No image")
