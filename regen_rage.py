#!/usr/bin/env python3
"""Regen RAGE mockup with cleaner logo integration."""
import os, json, base64, urllib.request, urllib.error

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
OUT = "/Users/quirineric/Desktop/Claude/boutik-saas/assets/styles/03-bold-statement.png"

PROMPT = """Pure flat website screenshot — NOT a device mockup, NOT a frame. 16:10 aspect ratio, 1600x1000 pixels, full bleed edge to edge.

Content: hero section of a French challenger F&B brand website.

LAYOUT:
- Thin top nav bar: brand wordmark left ("RAGE" in heavy gothic blackletter font, white color, integrated naturally into the nav — NOT inside a white box), menu items right ("BOUTIQUE" "À PROPOS" "CONTACT" in uppercase Inter bold white).
- Below nav: 2-column hero. Left = giant text content. Right = product photography.

LEFT TEXT CONTENT (60% width, with generous padding):
- Massive uppercase headline, Anton or Bebas Neue ultra bold, pure white on black, 3 lines:
  "BOIS."
  "PIQUE."
  "RECOMMENCE."
- Subtitle below, uppercase Inter bold white, smaller:
  "EAU PÉTILLANTE CAFÉINÉE."
  "0 SUCRE. 0 COMPROMIS."
- CTA rectangular button below — bright neon yellow #FACC15 background, black uppercase text "ATTAQUE — 24,90 € / 6", no rounded corners or very subtle radius.

RIGHT PRODUCT (40% width):
- Tall slim matte black drink can.
- On the can label: neon yellow lightning bolt + brand name "RAGE" written in the EXACT SAME blackletter/gothic font as the navigation logo. CRITICAL CONSISTENCY: the "RAGE" wordmark in the nav AND on the can MUST be the IDENTICAL blackletter gothic typography (same letterforms, same proportions, same style). NOT one in gothic and another in sans-serif. SAME font throughout.
- Dramatic splash water effect around the can, dark studio shot, high contrast.

PALETTE:
- Background: pure black #000000
- Text: pure white #FFFFFF
- Accent: neon yellow #FACC15

CRITICAL: The "RAGE" brand name in the top-left nav must be CLEAN — just the white blackletter text on the black background, NO white box behind it, NO awkward floating block. Integrated like Aesop or Liquid Death does it — minimal nav with just clean typography.

Style references: Liquid Death, Gymshark, Asphalte, Mid-Day Squares.

Output: clean website hero screenshot, full bleed, NO device frame.
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
        with open(OUT, "wb") as f:
            f.write(img)
        print(f"✓ Regenerated {os.path.basename(OUT)} ({len(img)//1024} KB)")
        exit(0)
print(f"No image: {json.dumps(body, indent=2)[:400]}")
