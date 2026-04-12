"""
Comic v7 — LLM NEWS motion graphics explainer.
Progressive disclosure: one background, systems appear one by one.
Style reference: motion.so snackable explainers.
Output: 1920x1080 16:9 MP4 at 30fps.
"""
import os, json, base64, math, requests
from PIL import Image, ImageDraw, ImageFont

OUT = "/root/comic-v7"
FRAMES_DIR = os.path.join(OUT, "explainer_frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

NB2_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GEMINI_API_KEY")

W, H = 1920, 1080
FPS = 30
TOTAL_SECONDS = 35

# Colors (RGBA tuples used with alpha compositing)
NAVY = (15, 23, 42)
DARK_NAVY = (10, 15, 30)
WHITE = (255, 255, 255)
GOLD = (255, 200, 50)
ORANGE = (255, 140, 40)
RED = (220, 40, 40)
PURPLE = (130, 50, 180)
GREEN = (40, 200, 80)
TICKER_BG = (10, 15, 35)

# Fonts
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_COND_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()


def ease_out(t):
    return 1 - (1 - min(1, max(0, t))) ** 3


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


# ────────────────────────────────────────
# NB2 base map generation
# ────────────────────────────────────────
def gen_nb2_base():
    """Generate clean map background with NB2."""
    print("Generating clean base map with NB2...")
    if not NB2_KEY:
        print("  No NB2 key"); return None

    prompt = """A television news broadcast screen background with ONLY geography, no data:
- Top banner: solid dark navy (#0A0F23) bar full width, 60px tall
- Main area: stylized satellite-view map of the Persian Gulf and Strait of Hormuz region. Iran coastline along the north, UAE and Oman along the south. The Strait is a clear narrow passage between them. Ocean in deep teal-blue (#143F50), land in dark blue-grey (#1A2840). Country labels "IRAN", "UAE", "OMAN" in small white sans-serif text.
- Bottom bar: solid dark navy (#0A0F23) bar full width, 70px tall
- NO weather systems, NO icons, NO annotations, NO data overlays. ONLY the map geography.
- The map should fill most of the frame, with the Strait of Hormuz roughly in the right-center.
- Clean, dark, professional broadcast aesthetic. No gradients on the bars."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={NB2_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": "16:9"},
        }
    }
    try:
        r = requests.post(url, json=payload, timeout=300)
        print(f"  HTTP {r.status_code}")
        if r.status_code != 200:
            print(f"  ERR: {r.text[:500]}"); return None
        data = r.json()
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img_data = base64.b64decode(part["inlineData"]["data"])
                    path = os.path.join(OUT, "base_map_nb2.png")
                    with open(path, "wb") as f:
                        f.write(img_data)
                    print(f"  Saved: {path} ({len(img_data)//1024}KB)")
                    return path
        return None
    except Exception as e:
        print(f"  EXC: {e}"); return None


# ────────────────────────────────────────
# Drawing primitives
# ────────────────────────────────────────
def draw_rounded_box(draw, xy, fill, radius=8):
    """Draw a rounded rectangle with RGBA fill on an RGBA overlay."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def draw_glow_ellipse(draw, center, radius, color, alpha):
    """Soft radial glow effect."""
    cx, cy = center
    for r in range(radius, 0, -2):
        a = int(alpha * 0.3 * (r / radius))
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)],
                     fill=(*color, a))


# ────────────────────────────────────────
# System overlay renderers (map graphics only)
# ────────────────────────────────────────
def overlay_system_1(draw, alpha):
    """Golden sun glow over the Strait."""
    a = int(255 * alpha)
    # Sun glow at Strait location
    draw_glow_ellipse(draw, (1300, 400), 100, GOLD, a)
    # Sun body
    draw.ellipse([(1265, 365), (1335, 435)], fill=(*GOLD, a))


def overlay_system_2(draw, alpha):
    """Orange convergence arrows toward the Strait."""
    a = int(255 * alpha)
    color = (*ORANGE, a)
    # Arrows pointing toward Strait from multiple directions
    arrows = [
        [(700, 700), (900, 550), (1100, 460)],
        [(500, 400), (800, 420), (1100, 430)],
        [(1700, 650), (1500, 530), (1350, 460)],
        [(1800, 300), (1600, 380), (1400, 430)],
    ]
    for pts in arrows:
        draw.line(pts, fill=color, width=3)
        # Arrowhead at last point
        px, py = pts[-1]
        sx, sy = pts[-2]
        dx, dy = px - sx, py - sy
        length = max(1, math.sqrt(dx*dx + dy*dy))
        ux, uy = dx/length, dy/length
        s = 14
        draw.polygon([
            (int(px), int(py)),
            (int(px - s*ux + s*0.4*uy), int(py - s*uy - s*0.4*ux)),
            (int(px - s*ux - s*0.4*uy), int(py - s*uy + s*0.4*ux)),
        ], fill=color)

    # Ship icons
    for sx, sy in [(800, 620), (1050, 500), (1550, 560), (1650, 370), (650, 480)]:
        draw.rounded_rectangle([(sx-10, sy-4), (sx+10, sy+4)],
                               radius=2, fill=(255, 255, 255, int(a * 0.7)))


def overlay_system_3(draw, alpha):
    """Red storm cell over the Strait chokepoint."""
    a = int(255 * alpha)
    # Red storm glow
    draw_glow_ellipse(draw, (1330, 430), 120, RED, a)

    # Lightning bolts
    bolt_a = int(a * 0.8)
    bolt_color = (255, 255, 180, bolt_a)
    draw.line([(1310, 360), (1300, 390), (1320, 400), (1305, 440)], fill=bolt_color, width=2)
    draw.line([(1350, 370), (1360, 395), (1340, 410), (1355, 445)], fill=bolt_color, width=2)


def overlay_system_4(draw, alpha):
    """Massive purple covering the entire map region."""
    a = int(255 * alpha)
    # Giant purple wash — covers most of the map
    for y in range(80, H - 80):
        row_a = int(a * 0.22)
        draw.line([(100, y), (W - 100, y)], fill=(100, 30, 140, row_a))

    # Darker core ellipse
    draw_glow_ellipse(draw, (W // 2, H // 2), 500, (60, 10, 90), a)


# ────────────────────────────────────────
# Info panel renderers (text labels — drawn ON TOP of everything)
# ────────────────────────────────────────
def panel_branding(draw, alpha):
    """LLM NEWS logo + banner. Always visible."""
    a = int(255 * alpha)

    # Top banner bar
    draw.rectangle([(0, 0), (W, 65)], fill=(*TICKER_BG, a))

    # LLM NEWS badge
    draw_rounded_box(draw, [(18, 10), (185, 56)], (*DARK_NAVY, a), radius=8)
    draw.rounded_rectangle([(18, 10), (185, 56)], radius=8,
                           outline=(60, 90, 120, int(a * 0.6)), width=1)
    draw.text((30, 12), "LLM", fill=(*WHITE, a), font=font(FONT_BOLD, 34))
    draw.text((115, 28), "NEWS", fill=(80, 180, 240, a), font=font(FONT_BOLD, 18))

    # Banner text
    draw.text((210, 18), "STRAIT FORECAST", fill=(*WHITE, a), font=font(FONT_BOLD, 30))
    draw.text((530, 24), "— GEOPOLITICAL ADVISORY", fill=(160, 180, 200, a),
              font=font(FONT_REG, 22))

    # Bottom ticker bar (empty for now)
    draw.rectangle([(0, H - 75), (W, H)], fill=(*TICKER_BG, a))


def panel_system_1(draw, alpha):
    """System 1 info panel: Ceasefire."""
    a = int(255 * alpha)
    # Position: right side, near the sun
    x, y = 1050, 250
    draw_rounded_box(draw, [(x, y), (x + 420, y + 140)], (10, 18, 38, int(a * 0.92)))

    draw.text((x + 18, y + 12), "SYSTEM 1: CEASEFIRE",
              fill=(*GOLD, a), font=font(FONT_BOLD, 28))
    draw.text((x + 18, y + 50), "Temporary clearing. Strait reopens.",
              fill=(220, 220, 230, a), font=font(FONT_REG, 18))
    draw.text((x + 18, y + 76), "Oil prices ease. 2-week window.",
              fill=(220, 220, 230, a), font=font(FONT_REG, 18))

    # Green status
    draw.ellipse([(x + 18, y + 108), (x + 34, y + 124)], fill=(*GREEN, a))
    draw.text((x + 42, y + 106), "ALL CLEAR", fill=(*GREEN, a), font=font(FONT_BOLD, 20))


def panel_system_2(draw, alpha):
    """System 2 info panel: Re-routing."""
    a = int(255 * alpha)
    x, y = 100, 520
    draw_rounded_box(draw, [(x, y), (x + 460, y + 140)], (10, 18, 38, int(a * 0.92)))

    draw.text((x + 18, y + 12), "SYSTEM 2: RE-ROUTING",
              fill=(*ORANGE, a), font=font(FONT_BOLD, 28))
    draw.text((x + 18, y + 50), "Vessels returning through bottleneck.",
              fill=(220, 220, 230, a), font=font(FONT_REG, 18))
    draw.text((x + 18, y + 76), "Cost savings drive traffic back. $800K/voyage.",
              fill=(220, 220, 230, a), font=font(FONT_REG, 18))

    # Orange triangle + WATCH
    tx, ty = x + 18, y + 108
    draw.polygon([(tx + 8, ty), (tx, ty + 16), (tx + 16, ty + 16)], fill=(*ORANGE, a))
    draw.text((tx + 24, ty - 2), "WATCH", fill=(*ORANGE, a), font=font(FONT_BOLD, 20))


def panel_system_3(draw, alpha):
    """System 3 info panel: Trap formation."""
    a = int(255 * alpha)
    x, y = 100, 310
    draw_rounded_box(draw, [(x, y), (x + 500, y + 170)], (10, 18, 38, int(a * 0.92)))

    draw.text((x + 18, y + 12), "SYSTEM 3: TRAP FORMATION",
              fill=(*RED, a), font=font(FONT_BOLD, 28))
    draw.text((x + 18, y + 50), "Ceasefire expires. Every vessel inside",
              fill=(220, 220, 230, a), font=font(FONT_REG, 18))
    draw.text((x + 18, y + 74), "the Strait is exposed. Those who re-routed",
              fill=(220, 220, 230, a), font=font(FONT_REG, 18))
    draw.text((x + 18, y + 98), "back are caught. 72-hour exit window.",
              fill=(220, 220, 230, a), font=font(FONT_REG, 18))

    # Red status
    draw.regular_polygon((x + 28, y + 140, 10), 8, fill=(*RED, a))
    draw.text((x + 44, y + 130), "SEVERE", fill=(*RED, a), font=font(FONT_BOLD, 20))

    # Countdown timer top-right
    draw_rounded_box(draw, [(1640, 80), (1890, 140)], (30, 10, 15, int(a * 0.9)))
    draw.text((1660, 88), "CEASEFIRE WINDOW", fill=(255, 120, 120, a), font=font(FONT_BOLD, 16))
    draw.text((1710, 112), "14 DAYS", fill=(255, 80, 80, a), font=font(FONT_BOLD, 22))


def panel_system_4(draw, alpha):
    """System 4 info panel: Permanent weaponization."""
    a = int(255 * alpha)
    x, y = 100, 100
    draw_rounded_box(draw, [(x, y), (x + 600, y + 200)], (15, 10, 30, int(a * 0.95)))

    draw.text((x + 18, y + 12), "SYSTEM 4: PERMANENT",
              fill=(*PURPLE, a), font=font(FONT_BOLD, 32))
    draw.text((x + 18, y + 50), "WEAPONIZATION",
              fill=(*PURPLE, a), font=font(FONT_BOLD, 32))

    draw.text((x + 18, y + 98), "The Strait is now a weapon even when open.",
              fill=(220, 220, 230, a), font=font(FONT_REG, 19))
    draw.text((x + 18, y + 124), "Maritime insurance permanently reprices.",
              fill=(220, 220, 230, a), font=font(FONT_REG, 19))
    draw.text((x + 18, y + 150), "Geography is now geopolitics.",
              fill=(240, 240, 250, a), font=font(FONT_BOLD, 19))

    # Status bar
    draw_rounded_box(draw, [(x + 18, y + 178), (x + 480, y + 198)],
                     (40, 15, 55, a), radius=4)
    draw.text((x + 28, y + 178), "UNPRECEDENTED — NO HISTORICAL MODEL",
              fill=(220, 170, 255, a), font=font(FONT_BOLD, 16))


def draw_ticker(draw, text, alpha):
    """Bottom ticker text."""
    a = int(255 * alpha)
    draw.text((30, H - 52), text, fill=(210, 215, 225, a), font=font(FONT_REG, 20))


# ────────────────────────────────────────
# Frame renderer
# ────────────────────────────────────────
def render_frame(base_img, frame_num):
    """Render one frame. Layer order: base → map overlays → text panels."""
    t = frame_num / FPS  # time in seconds

    # Start with base
    frame = base_img.copy().convert("RGBA")

    # Layer 1: Map overlays (weather graphics on the map)
    map_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(map_layer)

    if t >= 3:
        overlay_system_1(md, ease_out((t - 3) / 1.0))
    if t >= 9:
        overlay_system_2(md, ease_out((t - 9) / 1.0))
    if t >= 16:
        overlay_system_3(md, ease_out((t - 16) / 1.5))
    if t >= 23:
        overlay_system_4(md, ease_out((t - 23) / 2.0))

    frame = Image.alpha_composite(frame, map_layer)

    # Layer 2: Text panels (always on top of map graphics)
    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(text_layer)

    # Branding fades in at start
    panel_branding(td, ease_out(t / 1.0))

    # System panels fade in with their overlays
    if t >= 3:
        panel_system_1(td, ease_out((t - 3) / 1.0))
    if t >= 9:
        panel_system_2(td, ease_out((t - 9) / 1.0))
    if t >= 16:
        panel_system_3(td, ease_out((t - 16) / 1.5))
    if t >= 23:
        panel_system_4(td, ease_out((t - 23) / 2.0))

    # Ticker
    if t < 3:
        pass
    elif t < 9:
        draw_ticker(td, "BREAKING: Iran reopens Strait of Hormuz under 2-week ceasefire agreement. Oil futures drop 4%.", ease_out((t - 3) / 0.5))
    elif t < 16:
        draw_ticker(td, "UPDATE: Major shipping lines redirecting through Strait. Estimated savings: $800K per voyage vs Cape route.", ease_out((t - 9) / 0.5))
    elif t < 23:
        draw_ticker(td, "ANALYSIS: Companies maintaining Cape routes now positioned advantageously. Re-routed vessels face 72-hour exit window.", ease_out((t - 16) / 0.5))
    else:
        draw_ticker(td, "ADVISORY: Markets pricing System 1. Shipping responding to System 2. Analysts debating System 3. Nobody has a model for System 4.", ease_out((t - 23) / 0.5))

    frame = Image.alpha_composite(frame, text_layer)
    return frame.convert("RGB")


# ────────────────────────────────────────
# Main
# ────────────────────────────────────────
def main():
    # Step 1: Base map
    print("=" * 60)
    print("STEP 1: Base map")
    print("=" * 60)

    base_path = gen_nb2_base()
    if base_path:
        base_img = Image.open(base_path).resize((W, H), Image.LANCZOS)
        print(f"  Using NB2 base: {base_path}")
    else:
        # Fallback: use the existing NB2 slide 1 as base (it has System 1 baked in,
        # but it's better than the crude programmatic map)
        fallback = os.path.join(OUT, "strait_slide1_nb2.png")
        if os.path.exists(fallback):
            base_img = Image.open(fallback).resize((W, H), Image.LANCZOS)
            print(f"  Fallback: using slide 1 NB2 as base")
        else:
            # Last resort: dark navy background
            base_img = Image.new("RGB", (W, H), NAVY)
            print(f"  Using plain dark background")

    # Step 2: Render frames
    total = TOTAL_SECONDS * FPS
    print(f"\n{'='*60}")
    print(f"STEP 2: Rendering {total} frames ({TOTAL_SECONDS}s at {FPS}fps)")
    print("=" * 60)

    for i in range(total):
        frame = render_frame(base_img, i)
        frame.save(os.path.join(FRAMES_DIR, f"frame_{i:05d}.png"))
        if i % (FPS * 3) == 0:
            print(f"  {i}/{total} (t={i/FPS:.0f}s)")

    print(f"  Done")

    # Step 3: Compile
    print(f"\n{'='*60}")
    print("STEP 3: Compile MP4")
    print("=" * 60)

    out_path = os.path.join(OUT, "strait_explainer_v2.mp4")
    cmd = (
        f'ffmpeg -y -framerate {FPS} -i {FRAMES_DIR}/frame_%05d.png '
        f'-c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium '
        f'"{out_path}"'
    )
    os.system(cmd)

    if os.path.exists(out_path):
        mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"  Output: {out_path} ({mb:.1f}MB)")
    else:
        print("  FAILED")


if __name__ == "__main__":
    main()
