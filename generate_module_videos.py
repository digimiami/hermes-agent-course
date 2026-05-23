#!/usr/bin/env python3
"""Generate 30-second module intro videos for all 10 Hermes Course modules."""
import os
import subprocess
import textwrap
import tempfile
import shutil

MODULES = [
    (1, "What is Hermes Agent & Why It Matters", "Understand the architecture\necosystem, and why Hermes\nis different from ChatGPT", [
        "What is an AI agent?",
        "Hermes vs ChatGPT",
        "Core architecture overview",
        "Why self-hosted agents win"
    ], "Your understanding of\nAI agent fundamentals"),
    (2, "Installation & First Run", "Install on your local machine.\nOne command. First conversation\nin under 5 minutes.", [
        "One-liner install command",
        "Docker setup option",
        "Setup wizard walkthrough",
        "Your first agent conversation"
    ], "Hermes running on\nyour local machine"),
    (3, "Configuration Deep Dive", "Model providers, API keys,\ntoolsets, profiles, memory,\nand security setup.", [
        "20+ LLM providers",
        "API keys & security",
        "Toolsets & profiles",
        "Memory configuration"
    ], "Your fully configured\nHermes environment"),
    (4, "Daily Usage & Power Features", "Slash commands, delegation,\ncron jobs, webhooks,\nand advanced sessions.", [
        "Useful slash commands",
        "Subagent delegation",
        "Cron jobs & scheduling",
        "Webhook integration"
    ], "Power user workflows\nyou'll use every day"),
    (5, "Skills System - The Killer Feature", "Create, manage, and publish\nskills. Build your agent's\nknowledge base.", [
        "What are Hermes skills?",
        "Creating your first skill",
        "Skill libraries & sharing",
        "Self-improving skills"
    ], "Your own library of\n50+ reusable skills"),
    (6, "Training Your Agent", "Memory, user profiles,\ncorrections pipeline, and\nteaching workflows.", [
        "Persistent memory system",
        "Teaching your agent",
        "Correction workflows",
        "User profiles & preferences"
    ], "An agent trained on\nyour specific workflows"),
    (7, "Multi-Platform Gateway", "Telegram, Discord, WhatsApp\nbots. Run your agent\neverywhere.", [
        "Telegram bot setup",
        "Discord integration",
        "WhatsApp connection",
        "Cross-platform workflows"
    ], "Your agent accessible\nfrom any device"),
    (8, "VPS Deployment", "Set up a $5 VPS, secure\nit, run Hermes 24/7 as\na systemd service.", [
        "VPS provider setup",
        "Security hardening",
        "systemd service config",
        "Monitoring & uptime"
    ], "Your agent running\n24/7 on a $5 VPS"),
    (9, "Monetization Strategies", "7 ways to make money - \nagent as a service, SaaS,\nwhite-label, and more.", [
        "Agent-as-a-Service model",
        "White-label solutions",
        "Skills marketplace",
        "Building a SaaS product"
    ], "A clear strategy to\ngenerate revenue"),
    (10, "Advanced Use Cases", "Trading bots, content\nautomation, code review,\ncustomer support, pipelines.", [
        "Trading bot automation",
        "Content creation pipeline",
        "Code review assistant",
        "Customer support agent"
    ], "Production-ready\nagent systems"),
]

OUTPUT_DIR = "/root/hermes-course/course/videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
W, H = 1920, 1080


def make_frame(module_num, title, subtitle, bullets, build_text, frame_num):
    from PIL import Image, ImageDraw, ImageFont
    
    img = Image.new('RGB', (W, H), (5, 5, 11))
    draw = ImageDraw.Draw(img)
    
    try:
        font_lg = ImageFont.truetype(FONT_FILE, 52)
        font_md = ImageFont.truetype(FONT_FILE, 36)
        font_sm = ImageFont.truetype(FONT_FILE, 28)
        font_bullet = ImageFont.truetype(FONT_MONO, 26)
        font_num = ImageFont.truetype(FONT_FILE, 120)
    except Exception:
        font_lg = ImageFont.load_default()
        font_md = font_sm = font_bullet = font_num = font_lg

    # Determine section
    if frame_num < 75:
        section = "title"
        progress = frame_num / 75.0
    elif frame_num < 150:
        section = "bullets"
        current_bullet = min(int((frame_num - 75) / 25), 3)
        progress = ((frame_num - 75) % 25) / 25.0
    else:
        section = "build"
        progress = (frame_num - 150) / 50.0
    
    # Grid background
    for x in range(0, W, 60):
        for y in range(0, H, 60):
            draw.point((x, y), fill=(15, 15, 30))
    
    # Top accent gradient line
    for x in range(0, W, 2):
        intensity = int(12 + 8 * abs((x / W) * 2 - 1))
        draw.rectangle([x, 0, x + 1, 2], fill=(intensity * 2, intensity, intensity * 3))
    
    if section == "title":
        # Module number
        num_text = "Module %d" % module_num
        bbox = draw.textbbox((0, 0), num_text, font=font_num)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, 180), num_text, fill=(30, 25, 50), font=font_num)
        
        # Title
        alpha = min(255, int(255 * progress * 2))
        for line_i, line in enumerate(textwrap.wrap(title, width=30)):
            bbox = draw.textbbox((0, 0), line, font=font_lg)
            tw = bbox[2] - bbox[0]
            y_pos = 340 + line_i * 70
            draw.text(((W - tw) // 2, y_pos), line, fill=(int(alpha * 0.7), int(alpha * 0.6), alpha), font=font_lg)
        
        # Subtitle
        sub_alpha = max(0, min(255, int(255 * (progress - 0.3) * 3)))
        if sub_alpha > 0:
            for line_i, line in enumerate(subtitle.split('\n')):
                bbox = draw.textbbox((0, 0), line, font=font_sm)
                tw = bbox[2] - bbox[0]
                draw.text(((W - tw) // 2, 500 + line_i * 45), line, fill=(int(sub_alpha * 0.4), int(sub_alpha * 0.4), int(sub_alpha * 0.5)), font=font_sm)
    
    elif section == "bullets":
        # Section title
        draw.text((W // 2 - 200, 160), "What You'll Learn", fill=(108, 92, 231), font=font_md)
        
        # Module name at top
        short_title = title[:25]
        header = "Module %d: %s" % (module_num, short_title)
        bbox = draw.textbbox((0, 0), header, font=font_sm)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, 80), header, fill=(100, 100, 140), font=font_sm)
        
        # Bullets
        for bullet_idx, bullet in enumerate(bullets):
            y_base = 270 + bullet_idx * 120
            if bullet_idx < current_bullet:
                # Already revealed
                draw.rounded_rectangle([300, y_base, 1620, y_base + 75], radius=10, fill=(18, 18, 34), outline=(60, 50, 100))
                draw.text((350, y_base + 18), "  " + bullet, fill=(200, 200, 220), font=font_bullet)
            elif bullet_idx == current_bullet:
                # Current bullet - animate in
                a = min(255, int(255 * progress))
                draw.rounded_rectangle([300, y_base, 1620, y_base + 75], radius=10, fill=(18, 18, 34), outline=(108, 92, 231))
                draw.text((350, y_base + 18), "  " + bullet, fill=(int(a * 0.8), int(a * 0.8), a), font=font_bullet)
            
            # Bullet number
            draw.text((330, y_base + 18), "%d." % (bullet_idx + 1), fill=(0, 206, 201), font=font_bullet)
    
    elif section == "build":
        draw.text((W // 2 - 200, 200), "What You Will Build", fill=(0, 206, 201), font=font_md)
        
        a = min(255, int(255 * progress * 2))
        
        # Terminal window
        draw.rounded_rectangle([350, 350, 1570, 650], radius=14, fill=(10, 10, 20), outline=(50, 50, 80))
        draw.rounded_rectangle([350, 350, 1570, 390], radius=14, fill=(18, 18, 34))
        draw.rectangle([350, 375, 1570, 390], fill=(18, 18, 34))
        draw.text((380, 358), "  === hermesshell - Build Complete ===", fill=(100, 100, 100), font=font_sm)
        
        lines = build_text.split('\n')
        for li, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_bullet)
            tw = bbox[2] - bbox[0]
            line_alpha = max(0, min(255, int(a * ((li + 1) / 4))))
            draw.text((400, 420 + li * 50), line, fill=(int(line_alpha * 0.7), line_alpha, int(line_alpha * 0.6)), font=font_bullet)
        
        # Cursor blink
        if int(frame_num / 8) % 2 == 0 and lines:
            last_line = lines[-1]
            kw = len(last_line) * 14
            draw.text((400 + kw + 5, 420 + (len(lines) - 1) * 50), "_", fill=(0, 206, 201), font=font_bullet)
    
    return img


def render_module_video(num, title, subtitle, bullets, build_text):
    out_path = os.path.join(OUTPUT_DIR, "module-%02d.mp4" % num)
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print("  Already exists: module-%02d.mp4 (%.1f MB)" % (num, size / 1024 / 1024))
        return out_path
    
    temp_dir = tempfile.mkdtemp()
    frames_dir = os.path.join(temp_dir, "frames")
    os.makedirs(frames_dir)
    
    total_frames = 200
    
    print("  Rendering %d frames..." % total_frames, end="", flush=True)
    for i in range(total_frames):
        img = make_frame(num, title, subtitle, bullets, build_text, i)
        img.save(os.path.join(frames_dir, "frame_%05d.png" % i))
        if i % 50 == 49:
            print(".", end="", flush=True)
    
    print(" done")
    
    cmd = [
        "ffmpeg", "-y", "-framerate", "25",
        "-i", os.path.join(frames_dir, "frame_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "23",
        "-an",
        out_path
    ]
    subprocess.run(cmd, capture_output=True)
    
    size = os.path.getsize(out_path)
    print("  Video: %s (%.1f MB)" % (out_path, size / 1024 / 1024))
    
    shutil.rmtree(temp_dir)
    return out_path


def main():
    print("Generating Module Intro Videos")
    print("=" * 50)
    
    for num, title, subtitle, bullets, build_text in MODULES:
        print("Module %d: %s" % (num, title[:40]))
        render_module_video(num, title, subtitle, bullets, build_text)
    
    print()
    print("=" * 50)
    print("All module videos generated!")
    print("Location: %s/" % OUTPUT_DIR)
    
    for f in sorted(os.listdir(OUTPUT_DIR)):
        path = os.path.join(OUTPUT_DIR, f)
        size = os.path.getsize(path)
        print("  module-%02d.mp4 - %.1f MB" % (int(f.split("-")[1].split(".")[0]), size / 1024 / 1024))


if __name__ == "__main__":
    main()
