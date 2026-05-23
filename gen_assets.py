#!/usr/bin/env python3
"""Génère le logo + l'aperçu boutique via Gemini."""
import os, json, base64, sys, concurrent.futures
import urllib.request

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3-pro-image-preview"

def gen(prompt, output_file):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode("utf-8"))
        print(f"[{output_file}] HTTP {e.code}: {json.dumps(body, indent=2)[:1000]}", file=sys.stderr)
        return False

    for part in body.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part or "inline_data" in part:
            d = part.get("inlineData") or part.get("inline_data")
            img = base64.b64decode(d["data"])
            with open(output_file, "wb") as f:
                f.write(img)
            print(f"✓ {output_file} ({len(img)//1024} KB)")
            return True
    print(f"[{output_file}] No image returned: {json.dumps(body, indent=2)[:500]}", file=sys.stderr)
    return False


LOGO_PROMPT = """
Minimalist abstract logomark for a tech SaaS product.
Single geometric symbol, no text, no letters.
Color: lime green (#A3E635 or #84CC16) on PURE BLACK background.
Design concept: a stylized abstract mark suggesting "instant creation" or "construction" — could be a folded geometric shape, a bracket-like shape, or a minimalist building block.
Style references: Linear.app logo, Vercel triangle, Cursor, Raycast — sharp, clean, vector-look, premium tech aesthetic.
Centered composition, generous padding around the mark.
Square 1024x1024.
NO TEXT IN THE IMAGE. Just the pure symbol.
"""

PREVIEW_PROMPT = """
Mockup screenshot of a premium French e-commerce product page on a laptop browser.
Top half visible: a clean modern product page hero section.
Color palette: warm cream and beige tones with deep forest green accents.
Layout: large product photo on the right (a beauty/skincare serum bottle, dark green glass with cream label, premium minimalist Korean beauty aesthetic), text on the left with a large serif headline in French "L'éclat naturel, en 28 jours." followed by a short subtitle and a dark rounded button "Découvrir — 49 €".
At the top: a thin navigation bar with a minimalist brand name and menu items.
Style references: Aesop, Glossier, Typology, premium DTC beauty French brand.
The page must look authentic, real, professional — not a stock template.
Aspect ratio: 16:10 wide. 1600x1000 pixels.
NO MOCKUP DEVICE FRAME — just the website content as if it's a clean screenshot.
"""

tasks = [
    (LOGO_PROMPT, "/Users/quirineric/Desktop/Claude/boutik-saas/assets/logo.png"),
    (PREVIEW_PROMPT, "/Users/quirineric/Desktop/Claude/boutik-saas/assets/preview.png"),
]

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(gen, p, o) for p, o in tasks]
    results = [f.result() for f in futures]

print(f"\nDone. {sum(results)}/{len(results)} images générées.")
