#!/usr/bin/env python3
"""Génère les 6 mockups de styles visuels via Gemini Nano Banana Pro."""
import os, json, base64, sys, concurrent.futures
import urllib.request, urllib.error

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
ASSETS_DIR = "/Users/quirineric/Desktop/Claude/boutik-saas/assets/styles"
os.makedirs(ASSETS_DIR, exist_ok=True)

def gen(prompt, output_file):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]}
    }
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
            with open(output_file, "wb") as f:
                f.write(img)
            print(f"✓ {os.path.basename(output_file)} ({len(img)//1024} KB)")
            return True
    print(f"[{os.path.basename(output_file)}] No image: {json.dumps(body, indent=2)[:400]}", file=sys.stderr)
    return False


BASE = """Mockup screenshot of a French e-commerce product page hero section.
Aspect ratio: 16:10 wide, 1600x1000 pixels.
The image should look like a real authentic premium DTC website hero, top portion only, NO laptop device frame, NO browser chrome — just the clean website content full-bleed.
Layout: large product photography on the right side, text content on the left (brand name top, large headline, short subtitle, dark rounded CTA button with French price in euros).
All text MUST be in French, prices in euros with comma decimal (e.g. 49,90 €).
Realistic, professional, looks like a real running brand.
"""

STYLES = [
    {
        "name": "01-editorial-premium",
        "prompt": BASE + """
STYLE: Editorial Premium — minimalist beauty editorial magazine aesthetic.
PRODUCT: Botanical skincare serum in dark amber glass dropper bottle, cream label.
BRAND NAME: "BOTANIQUE" (small uppercase letter-spaced sans).
HEADLINE: Large elegant SERIF (DM Serif Display or Cormorant) — "L'éclat retrouvé, en 28 jours."
SUBTITLE: Inter sans-serif — "Sérum botanique régénérant. Pour une peau lumineuse et apaisée."
CTA: Dark rounded button — "Découvrir — 49,90 €"
COLOR PALETTE: Cream beige #F4EDE2 background, deep forest green #1F3A2E accents, warm linen tones.
PHOTOGRAPHY: Editorial product shot with soft natural light, beige linen drape backdrop.
TYPOGRAPHY VIBE: Aesop, Sézane, Polène, Typology, Le Labo.
Generous whitespace. Refined, calm, premium.
"""
    },
    {
        "name": "02-clean-modern",
        "prompt": BASE + """
STYLE: Clean Modern — tech / wellness clinical minimal.
PRODUCT: Daily greens supplement powder in matte cream cylindrical tin with green label.
BRAND NAME: "VITALIS" (uppercase Inter bold).
HEADLINE: Inter Bold large — "Tout ce que ton corps demande. En une cuillère."
SUBTITLE: Inter regular — "75 nutriments essentiels. Goût naturel. Made in France."
CTA: Solid forest green rounded rectangle button — "Commander — 39,90 €"
COLOR PALETTE: Pure white #FFFFFF background, accent emerald green #047857, soft gray text #475569.
PHOTOGRAPHY: Clean studio shot on white background with subtle shadow, single product centered right.
TYPOGRAPHY VIBE: AG1, Ritual, Nothing, Apple, Cabaïa.
Grid-based, structured, modern. Minimal but warm.
"""
    },
    {
        "name": "03-bold-statement",
        "prompt": BASE + """
STYLE: Bold Statement — F&B challenger, irreverent, heavy attitude.
PRODUCT: Sparkling functional drink in tall slim can, matte black with neon yellow label.
BRAND NAME: "RAGE" (massive bold black caps, gothic-influenced).
HEADLINE: HUGE bold caps Anton or Archivo Black — "BOIS. PIQUE. RECOMMENCE."
SUBTITLE: Inter bold uppercase letter-spaced — "Eau pétillante caféinée. 0 sucre. 0 compromis."
CTA: Bright neon yellow rectangular button with black text — "ATTAQUE — 24,90 € / 6"
COLOR PALETTE: Pure black #000000 background, neon yellow #FACC15 accents, white text.
PHOTOGRAPHY: Dramatic high-contrast can shot with splash water effect, dark moody studio.
TYPOGRAPHY VIBE: Liquid Death, Gymshark, Asphalte, Mid-Day Squares.
Punchy, loud, can't ignore. Anti-establishment energy.
"""
    },
    {
        "name": "04-playful-friendly",
        "prompt": BASE + """
STYLE: Playful Friendly — pet brand warm, rounded, cheerful.
PRODUCT: Premium dog brush with curved wooden handle and soft pink rubber grip.
BRAND NAME: "wouafy" (lowercase rounded friendly sans — Nunito or Fredoka).
HEADLINE: Rounded sans Fredoka large — "Le brossage qu'ils adorent enfin."
SUBTITLE: Nunito regular — "Brosse anti-noeuds douce. Pour chiens à poils longs ou courts."
CTA: Coral pink rounded pill button — "Adopter — 29,90 €"
COLOR PALETTE: Warm peach #FED7AA background, coral pink #F87171 accents, soft cream, sage green hints.
PHOTOGRAPHY: Bright cheerful product shot with maybe a paw or fluffy dog ear peeking in corner, soft natural light.
TYPOGRAPHY VIBE: Bark, Chewy, Frida Baby, Konny, Olipop.
Warm, friendly, can't-help-but-smile vibe.
"""
    },
    {
        "name": "05-cinematic-ugc",
        "prompt": BASE + """
STYLE: Cinematic UGC — raw smartphone aesthetic, full-bleed video hero feel, problem-solver beauty.
PRODUCT: Hair growth serum in compact frosted glass bottle with minimal label.
BRAND NAME: "POUSSE" (small clean caps top corner).
HEADLINE: Large bold serif Fraunces over a real-feeling lifestyle photo background — "J'ai retrouvé mes cheveux en 8 semaines."
SUBTITLE: Inter — "Sérum capillaire. 1 200+ clientes vérifiées. Résultats visibles ou remboursé."
CTA: White button on dark photo — "Voir les résultats — 34,90 €"
COLOR PALETTE: Warm skin tones, golden hour lighting, soft brown and cream from real lifestyle photo background.
PHOTOGRAPHY: BIG full-bleed lifestyle photo of a woman in natural light, slight smartphone grain feel, sees her hair healthy and free. Text overlays on the photo with semi-transparent overlay band.
TYPOGRAPHY VIBE: Vacation Inc, Liquid IV, Native Deodorant, real UGC ads winners.
Authentic, raw, real woman feel. Mobile-first hero design.
"""
    },
    {
        "name": "06-neo-brutalist",
        "prompt": BASE + """
STYLE: Neo-Brutalist — fashion challenger, mono blocks, harsh layout, asymmetric.
PRODUCT: Oversized heavyweight cotton hoodie in stone gray, premium streetwear.
BRAND NAME: "ATELIER 9" (typewriter mono Space Mono caps).
HEADLINE: HUGE display font, asymmetric placement, broken grid — "LE HOODIE QU'ON VOLE."
SUBTITLE: Mono small caps — "Coton lourd 400g. Coupe oversize. Fabriqué au Portugal."
CTA: Pure black rectangle button with white mono text, no rounded corners — "ACHETER · 89,00 €"
COLOR PALETTE: Stark cream #FAFAF7 background, black blocks, single hot accent like electric blue #2563EB used sparingly.
PHOTOGRAPHY: Editorial flat-lay or model shot with brutal cropping, mono color block backdrop, intentional negative space.
TYPOGRAPHY VIBE: Tediber on indie pages, ABC Dinamo, contemporary Berlin/Paris fashion brands.
Loud, harsh, intentional ugly-on-purpose elements that look designed.
"""
    },
]

tasks = [(s["prompt"], f"{ASSETS_DIR}/{s['name']}.png") for s in STYLES]

print(f"Génération de {len(tasks)} styles en parallèle...")
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    futures = [pool.submit(gen, p, o) for p, o in tasks]
    results = [f.result() for f in futures]
print(f"\nDone. {sum(results)}/{len(results)} mockups générés.")
