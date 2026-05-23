#!/usr/bin/env python3
"""Regenerate Clean Modern WITHOUT laptop frame."""
import os, json, base64, urllib.request, urllib.error

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
OUT = "/Users/quirineric/Desktop/Claude/boutik-saas/assets/styles/02-clean-modern.png"

PROMPT = """A pure flat screenshot — NOT a mockup, NOT a laptop, NOT a device, NOT a phone, NOT any frame whatsoever. Just the raw website pixels as if you opened the site in fullscreen and took a screenshot.

Aspect ratio: 16:10 wide, 1600x1000 pixels. Full bleed, edge to edge.

Content: hero section of a French wellness supplement brand website.

LAYOUT:
- Top: thin nav bar (logo left "VITALIS" uppercase Inter bold + menu items right "Boutique" "Bénéfices" "Avis" "Panier")
- Below nav: 2-column hero. Left = text content (60% width). Right = product photography (40% width).

LEFT CONTENT:
- Eyebrow small caps text: "COMPLÉMENT QUOTIDIEN"
- Huge Inter bold headline: "Tout ce que ton corps demande. En une cuillère."
- Subtitle Inter regular: "75 nutriments essentiels. Goût naturel. Made in France."
- Star rating row: ★★★★★ 4.9 (2 847 avis)
- CTA dark forest green solid button rounded: "Commander — 39,90 €"
- Below CTA, 3 small icons row: "Livraison 48h · Garantie 60j · Paiement sécurisé"

RIGHT PRODUCT:
- Premium matte cream cylindrical tin with VITALIS branding and green leaf logo, label says "Daily Greens · Complément Alimentaire · 300g · 30 doses".
- Subtle soft drop shadow on pure white background.
- The product fills most of the right column.

PALETTE:
- Background: pure white #FFFFFF
- Text dark: near-black #0A0A0A
- Accent green: deep emerald #047857
- Subtle gray for secondary text #64748B

STYLE REFERENCE: AG1 (drinkag1.com), Ritual, Apple product pages, Nothing.tech — Clean Modern.

CRITICAL: Output must be a FLAT WEBSITE SCREENSHOT, full bleed, NO device frame around it. Imagine the user clicked "Take screenshot" in their browser at fullscreen — that's what we want.
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
