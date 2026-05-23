#!/usr/bin/env python3
"""Regen 3 portraits ULTRA-réalistes (look 'photo iPhone authentique', pas stock)."""
import os, json, base64, sys, concurrent.futures
import urllib.request, urllib.error

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
OUT = "/Users/quirineric/Desktop/Claude/boutik-saas/assets/avatars"
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


# ─── ULTRA-REALISTIC: la clé c'est "iPhone photo, not portrait studio" ───
# Critère réussi : indistinguable d'une vraie photo Instagram

PEOPLE = [
    {
        "name": "leo",
        "prompt": """Real authentic iPhone photo (not a studio portrait, not a stock photo). Casual selfie aesthetic, slightly imperfect, real grain texture.

Subject: French male, 28 years old, mediterranean European descent (Italian/Spanish/Southern French look). Medium-length brown wavy hair slightly messy from the day. 3-day stubble beard. Wearing a casual heather charcoal hoodie or simple gray crewneck.

Composition: Mid-shot from chest up. Slight angle (NOT centered straight-on, more like he tilted his phone). Looking at camera with a small natural half-smile (not full grin, more like "yeah hey").

Setting: Inside his apartment in Lyon, slightly out of focus background showing a window with daylight, hint of wooden furniture and plants. The light hits one side of his face naturally.

Quality details: Real iPhone-quality photo, slight motion blur acceptable, natural skin texture (NOT smoothed), small imperfections visible (small mole, slight asymmetry). Looks like he took 5 sec to snap it.

Format: square 1024x1024. Photo-realistic. ABSOLUTELY NOT 3D, NOT illustration, NOT polished studio portrait, NOT stock photo aesthetic.""",
    },
    {
        "name": "camille",
        "prompt": """Real authentic iPhone photo (not a studio portrait, not a stock photo). Looks like a candid moment, possibly mid-conversation.

Subject: French woman, 32 years old, mixed French-North African heritage (Maghreb features, French-Algerian or French-Moroccan), shoulder-length dark brown wavy hair pulled to one side. Warm tan complexion, light freckles visible across nose/cheeks. Minimal makeup (just a hint of mascara, natural lip color). Wearing a rust-colored linen blouse or simple oat-colored sweater.

Composition: Mid-shot from upper chest up, slightly off-center. Genuine open smile showing teeth, like she just heard something amusing. Eyes slightly crinkled.

Setting: Bright sun-lit modern apartment in Bordeaux, sunlight from large window on the right casting warm light. Background slightly blurred showing a wooden bookshelf with plants and books. Maybe a small framed art print visible.

Quality details: Real iPhone-quality photo, sharp eyes but slight ambient blur, natural skin showing pores and tiny imperfections. NO airbrushing. Looks like a real photo a friend took mid-conversation.

Format: square 1024x1024. Photo-realistic, ABSOLUTELY NOT 3D, NOT illustration, NOT glamour shot, NOT stock photo aesthetic.""",
    },
    {
        "name": "yanis",
        "prompt": """Real authentic iPhone photo (not a studio portrait, not a stock photo). Outdoor street style, casual.

Subject: French man, 25 years old, clearly North African heritage (French-Tunisian or French-Algerian features, darker olive complexion, dark brown eyes). Short curly black hair with a clean fade haircut. Neat short beard. Single small gold stud earring (subtle). Wearing a plain black crew-neck t-shirt OR simple olive-green bomber jacket.

Composition: Standing outside, three-quarter portrait. Looking slightly off-camera with confident half-smile, like he's looking at someone calling his name. Hands maybe in pockets visible at frame bottom.

Setting: Urban street in Toulouse early evening. Brick wall and blurred outdoor café terrace in background. Warm golden hour sunlight from behind/side creating gentle rim light on his hair and shoulder. Slight lens flare possible.

Quality details: iPhone street photography style, natural depth of field, slight motion in background suggesting reality, slightly overexposed highlights on his shoulder from the sun. Skin texture visible, NOT smoothed.

Format: square 1024x1024. Photo-realistic, ABSOLUTELY NOT 3D, NOT illustration, NOT studio shot, NOT stock photo aesthetic.""",
    },
]

tasks = [(p["prompt"], f"{OUT}/{p['name']}.png") for p in PEOPLE]
print(f"Regen {len(tasks)} avatars ULTRA-réalistes…")
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(gen, p, o) for p, o in tasks]
    results = [f.result() for f in futures]
print(f"\n{sum(results)}/{len(results)} avatars régénérés.")
