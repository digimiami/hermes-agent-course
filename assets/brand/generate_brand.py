#!/usr/bin/env python3
"""
Generate brand assets for AI Agents Course
Output: logo, favicon, social banner, hero image
"""
import subprocess, os, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

BASE = Path("/root/hermes-course/assets/brand")
BASE.mkdir(parents=True, exist_ok=True)

W = 2000
H = 2000

def get_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    if bold:
        candidates = [c for c in candidates if "Bold" in c or "bold" in c]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

def create_logo_icon():
    """Generate the AI hexagon+circuit logo icon"""
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    
    # Outer hexagon
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 90)
        r = 700
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=None, outline=(108,92,231,180), width=12)
    
    # Inner glowing hexagon
    pts2 = []
    for i in range(6):
        a = math.radians(60 * i - 90)
        r = 620
        pts2.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts2, fill=(108,92,231,20), outline=(0,206,201,100), width=4)
    
    # Circuit lines inside hex
    circuit_points = [
        (cx-300, cy-200, cx-100, cy-200),
        (cx-100, cy-200, cx, cy-150),
        (cx, cy-150, cx, cy+50),
        (cx, cy+50, cx+200, cy+100),
        (cx+200, cy+100, cx+350, cy+50),
        (cx-200, cy+100, cx-100, cy+150),
        (cx-100, cy+150, cx+50, cy+150),
        (cx+50, cy+150, cx+200, cy+200),
        (cx-350, cy-50, cx-200, cy-50),
        (cx-200, cy-50, cx-200, cy+50),
    ]
    for x1, y1, x2, y2 in circuit_points:
        draw.line([(x1,y1),(x2,y2)], fill=(0,206,201,150), width=6)
        # Small dots at endpoints
        draw.ellipse([x1-10,y1-10,x1+10,y1+10], fill=(0,206,201,200))
        draw.ellipse([x2-10,y2-10,x2+10,y2+10], fill=(0,206,201,200))
    
    # Center node - brain/AI symbol
    # Outer glow circle
    for r in range(60, 0, -2):
        alpha = int(60 * (1 - r/60))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(108,92,231,alpha//3))
    
    # Central brain/AI icon
    draw.ellipse([cx-50, cy-50, cx+50, cy+50], fill=(108,92,231,60), outline=(0,206,201,200), width=6)
    
    # Bolt/lightning in center
    bolt = [(cx-20, cy-60), (cx+10, cy-15), (cx-5, cy-15), (cx+25, cy+40), (cx+5, cy+40)]
    draw.polygon(bolt, fill=(0,206,201,220))
    
    # Orbiting dots
    for i in range(8):
        a = math.radians(45 * i + 15)
        r = 400
        dx = cx + r * math.cos(a)
        dy = cy + r * math.sin(a)
        draw.ellipse([dx-8, dy-8, dx+8, dy+8], fill=(108,92,231,180))
    
    # Save icon
    icon = img.copy()
    
    # Full logo with text
    draw = ImageDraw.Draw(img)
    fnt = get_font(160, bold=True)
    # "AI" text
    draw.text((cx, cy+480), "AI AGENTS", fill=(255,255,255,230), font=fnt, anchor="mm")
    
    fnt2 = get_font(90, bold=False)
    draw.text((cx, cy+620), "Master Hermes Agent", fill=(180,180,200,200), font=fnt2, anchor="mm")
    
    # Save
    icon.save(str(BASE / "logo-icon.png"))
    img.save(str(BASE / "logo-full.png"))
    print("✅ Logo created")
    
    # Favicon (64x64)
    icon64 = icon.copy()
    icon64.thumbnail((64, 64), Image.LANCZOS)
    icon64.save(str(BASE / "favicon.png"))
    # Also create ICO
    icon32 = icon.copy()
    icon32.thumbnail((32, 32), Image.LANCZOS)
    icon32.save(str(BASE / "favicon.ico"))
    print("✅ Favicon created")
    
    return icon, img

def create_social_banner():
    """Create social media banner (1200x630 - OG image)"""
    Wb, Hb = 1200, 630
    img = Image.new("RGBA", (Wb, Hb), (10, 10, 26, 255))
    draw = ImageDraw.Draw(img)
    
    # Gradient overlay
    for y in range(Hb):
        alpha = int(60 * (1 - y/Hb))
        draw.line([(0,y),(Wb,y)], fill=(108,92,231,alpha//4))
    
    # Glow orb
    for r in range(200, 0, -2):
        alpha = int(40 * (1 - r/200))
        draw.ellipse([Wb//2-r, Hb//2-r, Wb//2+r, Hb//2+r], fill=(108,92,231,alpha))
    
    # Hex border
    pts = []
    cx2, cy2 = Wb//2, Hb//2
    for i in range(6):
        a = math.radians(60 * i - 90)
        r = 220
        pts.append((cx2 + r * math.cos(a), cy2 + r * math.sin(a)))
    draw.polygon(pts, fill=(108,92,231,15), outline=(0,206,201,60), width=3)
    
    # Text
    fnt_l = get_font(60, bold=True)
    draw.text((Wb//2, 80), "AI AGENTS", fill=(255,255,255,240), font=fnt_l, anchor="mm")
    fnt_m = get_font(36, bold=False)
    draw.text((Wb//2, 150), "Master Hermes Agent", fill=(180,180,200,200), font=fnt_m, anchor="mm")
    fnt_s = get_font(26)
    draw.text((Wb//2, 520), "Build Your Own AI Assistant — No Coding Required", fill=(150,150,180,180), font=fnt_s, anchor="mm")
    fnt_xs = get_font(20)
    draw.text((Wb//2, 570), "10 Modules · $97 · Lifetime Access", fill=(108,92,231,200), font=fnt_xs, anchor="mm")
    
    img.save(str(BASE / "social-banner.png"))
    print("✅ Social banner created")

def create_hero_image():
    """Create a hero image for the landing page (dark terminal-style)"""
    Wi, Hi = 1920, 600
    img = Image.new("RGBA", (Wi, Hi), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    # Terminal window
    tx, ty, tw, th = 200, 80, Wi-400, Hi-160
    draw.rounded_rectangle([tx, ty, tx+tw, ty+th], radius=20, fill=(12,12,26,230), outline=(40,40,80,150), width=2)
    
    # Title bar
    draw.rounded_rectangle([tx, ty, tx+tw, ty+45], radius=20, fill=(20,20,40,200))
    draw.rectangle([tx, ty+30, tx+tw, ty+45], fill=(20,20,40,200))
    for dx, c in [(15, (255,95,87)), (42, (255,189,46)), (69, (39,201,63))]:
        draw.ellipse([tx+dx, ty+16, tx+dx+12, ty+28], fill=c)
    
    fnt = get_font(22)
    draw.text((tx+90, ty+18), "hermes@agent: ~", fill=(140,140,160,200), font=fnt)
    
    # Terminal content lines
    lines = [
        ("$", "curl -fsSL https://get.hermes | bash", True),
        (" ", "✓ Checking dependencies...", False),
        (" ", "✓ Creating ~/.hermes/ directory", False),
        (" ", "✓ Installation complete!", False),
        ("$", "hermes", True),
        (" ", "╭──────────────────────────────────────╮", False),
        (" ", "│  Hermes Agent 2.2.0 • deepseek-chat  │", False),
        (" ", "╰──────────────────────────────────────╯", False),
        (">", "install nginx and configure reverse proxy", False),
        (" ", "  ✓ Nginx installed", False),
        (" ", "  ✓ Reverse proxy configured on port 80", False),
        ("$", "deploy app", False),
        (" ", "  🚀 Deployment complete!", False),
    ]
    y = ty + 65
    lm = tx + 25
    for prefix, text, is_cmd in lines:
        if prefix == "$":
            draw.text((lm, y), "$", fill=(0,206,201,255), font=get_font(22, bold=True))
            draw.text((lm+35, y), text, fill=(255,255,255,230), font=get_font(22))
        elif prefix == ">":
            draw.text((lm+15, y), f"> {text}", fill=(200,200,220,200), font=get_font(20))
        else:
            draw.text((lm+15, y), text, fill=(150,150,180,180), font=get_font(20))
        y += 40
    
    img.save(str(BASE / "hero-image.png"))
    print("✅ Hero image created")

def create_circle_logo():
    """Create a circle icon version for app icons"""
    img = Image.new("RGBA", (1024, 1024), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    # Circle background
    draw.ellipse([20, 20, 1004, 1004], fill=(18,18,34,255), outline=(108,92,231,80), width=8)
    
    # Inner glow
    for r in range(420, 0, -2):
        alpha = int(30 * (1 - r/420))
        draw.ellipse([512-r, 512-r, 512+r, 512+r], fill=(108,92,231,alpha))
    
    # Mini hexagon
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 90)
        r = 280
        pts.append((512 + r * math.cos(a), 512 + r * math.sin(a)))
    draw.polygon(pts, fill=None, outline=(0,206,201,120), width=6)
    
    # Center bolt
    bolt = [(488, 420), (530, 470), (508, 470), (540, 530), (500, 530)]
    draw.polygon(bolt, fill=(0,206,201,200))
    
    # Text
    fnt = get_font(80, bold=True)
    draw.text((512, 780), "AI", fill=(255,255,255,230), font=fnt, anchor="mm")
    fnt2 = get_font(40)
    draw.text((512, 870), "AGENTS", fill=(180,180,200,180), font=fnt2, anchor="mm")
    
    img.save(str(BASE / "logo-circle.png"))
    print("✅ Circle logo created")

# Run all
print("🎨 Generating brand assets...")
create_logo_icon()
create_social_banner()
create_hero_image()
create_circle_logo()

print(f"\n✅ All assets saved to {BASE}/")
print("  - logo-full.png    (2000x2000)")
print("  - logo-icon.png    (2000x2000)")
print("  - logo-circle.png  (1024x1024)")
print("  - favicon.png      (64x64)")
print("  - favicon.ico      (32x32)")
print("  - social-banner.png (1200x630)")
print("  - hero-image.png   (1920x600)")

# Show file sizes
for f in sorted(BASE.iterdir()):
    print(f"  {f.name}: {f.stat().st_size/1024:.1f} KB")
