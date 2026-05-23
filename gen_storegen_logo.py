#!/usr/bin/env python3
"""Génère 3 variantes de logos pour storegen.io via Gemini Nano Banana Pro."""
import os, json, base64, sys, concurrent.futures
import urllib.request, urllib.error

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
OUT = "/Users/quirineric/Desktop/Claude/boutik-saas/assets/logos"
os.makedirs(OUT, exist_ok=True)

def gen(prompt, output_file):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseModalities": ["IMAGE"]}}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode("utf-8"))
        print(f"[{os.path.basename(output_file)}] HTTP {e.code}: {json.dumps(body, indent=2)[:600]}", file=sys.stderr)
        return False
    for part in body.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part or "inline_data" in part:
            d = part.get("inlineData") or part.get("inline_data")
            img = base64.b64decode(d["data"])
            with open(output_file, "wb") as f: f.write(img)
            print(f"✓ {os.path.basename(output_file)} ({len(img)//1024} KB)")
            return True
    return False


BASE = """Single brand logomark for a tech SaaS product called "Storegen" (a tool that builds Shopify stores instantly via AI).
NO TEXT, NO LETTERS, NO WORDS — just the abstract symbol mark.
Pure black background #000000. Symbol in amber gold color #F59E0B (or a gradient amber→darker amber #D97706).
Premium tech aesthetic, sharp clean vector look, sits beautifully at small sizes (favicon-ready).
Reference brands' logo style: Linear.app, Vercel triangle, Cursor, Raycast, Stripe — minimal geometric.
Centered composition, generous padding around the mark.
Output: square 1024x1024, the mark fills about 50% of the canvas.
"""

CONCEPTS = [
    {
        "name": "01-stacked-blocks",
        "prompt": BASE + """
DESIGN CONCEPT: Stacked geometric blocks suggesting CONSTRUCTION + GENERATION.
3 to 4 overlapping rounded squares or rectangles arranged in an isometric or stacked layout, suggesting layers being assembled into a complete structure.
The composition should feel like blocks being generated and snapping into place — premium and dynamic but minimal.
Maybe one block is slightly offset/exploded to suggest the "generation" moment.
""",
    },
    {
        "name": "02-folded-G",
        "prompt": BASE + """
DESIGN CONCEPT: Abstract geometric letterform that subtly suggests a "G" or "S" but reads as a pure abstract mark.
Created from folded paper or origami-like ribbon shapes — clean lines, sharp angles.
Modern tech aesthetic, suggests "structure being built" through the folding metaphor.
""",
    },
    {
        "name": "03-spark-cube",
        "prompt": BASE + """
DESIGN CONCEPT: A 3D minimalist cube or hexagon with a small spark/lightning element either inside or emerging from one face.
The cube represents the "store/structure" and the spark represents the AI generation moment.
Very minimal — just the cube silhouette in amber outlines with one inner detail.
Premium tech vector look.
""",
    },
]

tasks = [(c["prompt"], f"{OUT}/{c['name']}.png") for c in CONCEPTS]
print(f"Génération de {len(tasks)} variantes Storegen logo...")
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(gen, p, o) for p, o in tasks]
    results = [f.result() for f in futures]
print(f"\n{sum(results)}/{len(results)} logos générés.")
