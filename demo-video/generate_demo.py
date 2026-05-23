#!/usr/bin/env python3
"""
Generate a 90-second Hermes Agent demo video
Creates animated terminal-style scenes → compiles with FFmpeg
"""
import subprocess, os, json, math, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path("/root/hermes-course/demo-video")
BASE.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = BASE / "frames"
FRAMES_DIR.mkdir(exist_ok=True)

W, H = 1920, 1080
FPS = 30
FONT_SIZE = 28
TERM_PAD = 60
TERM_TOP = 140
LINE_H = 38

def get_font(size):
    for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

FONT = get_font(FONT_SIZE)
FONT_BOLD = get_font(FONT_SIZE + 4)

def draw_frame(lines, progress=1.0, highlight=None, caption=""):
    """Render a single terminal-style frame"""
    img = Image.new("RGBA", (W, H), (10, 10, 20, 255))
    draw = ImageDraw.Draw(img)
    
    # Subtle grid background
    for x in range(0, W, 60):
        draw.line([(x,0),(x,H)], fill=(20,20,35,50), width=1)
    for y in range(0, H, 60):
        draw.line([(0,y),(W,y)], fill=(20,20,35,50), width=1)
    
    # Terminal window
    term_x, term_y = 60, 160
    term_w, term_h = W - 120, H - 220
    draw.rounded_rectangle([term_x, term_y, term_x+term_w, term_y+term_h],
                          radius=14, fill=(15,15,28,230), outline=(40,40,80,200), width=2)
    
    # Title bar
    draw.rounded_rectangle([term_x, term_y, term_x+term_w, term_y+40],
                          radius=14, fill=(25,25,50,255), outline=None)
    draw.rectangle([term_x, term_y+30, term_x+term_w, term_y+40], fill=(25,25,50,255))
    # Dots
    for dx, c in [(12, (255,95,87)), (40, (255,189,46)), (68, (39,201,63))]:
        draw.ellipse([term_x+dx, term_y+14, term_x+dx+12, term_y+26], fill=c)
    draw.text((term_x+90, term_y+12), "hermes@agent: ~", fill=(140,140,160,200), font=FONT)
    
    # Lines of text (terminal content)
    y_pos = term_y + 60
    visible_count = int(len(lines) * progress)
    
    for i, line in enumerate(lines[:visible_count]):
        if not line:
            y_pos += LINE_H
            continue
        is_prompt = line.startswith("$")
        is_cmd = line.startswith(">")
        is_output = not is_prompt and not is_cmd
        
        if is_prompt:
            text_to_show = line[1:].lstrip()
            # Draw prompt $
            draw.text((term_x+20, y_pos), "$", fill=(0, 206, 201, 255), font=FONT_BOLD)
            # Draw command text
            draw.text((term_x+50, y_pos), text_to_show, fill=(255,255,255,240), font=FONT_BOLD)
        elif is_cmd:
            draw.text((term_x+50, y_pos), line[1:].lstrip(), fill=(255,255,255,220), font=FONT)
        else:
            color = highlight if highlight and highlight in line else (180,180,200,200)
            draw.text((term_x+25, y_pos), line, fill=color, font=FONT)
        
        y_pos += LINE_H
    
    # Caption at bottom
    if caption:
        cap_y = H - 60
        # Draw caption background
        draw.rounded_rectangle([W//2-350, cap_y-10, W//2+350, cap_y+50],
                              radius=20, fill=(0,0,0,160), outline=(108,92,231,80), width=1)
        draw.text((W//2, cap_y+18), caption, fill=(200,200,255,255), font=FONT, anchor="mm")
    
    return img

# Scene definitions: (duration_sec, lines, caption, typing_speed_multiplier)
SCENES = [
    # Scene 1: Intro splash
    (6, [
        "╔══════════════════════════════════════════════════════╗",
        "║     HERMES AGENT — BUILD AN AUTOMATION IN 90s      ║",
        "╚══════════════════════════════════════════════════════╝",
        "",
        "Hermes Agent is an open-source AI framework",
        "that runs in your terminal, connects to any LLM,",
        "and has real tools — web search, file editing,",
        "terminal access, and multi-platform messaging.",
        "",
        "Watch as we build a complete automation:",
        "→ Install Hermes",
        "→ Configure Telegram",
        "→ Create custom skills",
        "→ Deploy a server",
        "→ Automate a workflow",
    ], "Hermes Agent — Open Source AI That Does Things", 0.8),
    
    # Scene 2: Install Hermes
    (10, [
        "",
        "Step 1: Install Hermes Agent",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "$ curl -fsSL https://raw.githubusercontent.com/NousResearch/",
        "  hermes-agent/main/scripts/install.sh | bash",
        "",
        "✓ Checking dependencies... Python 3.11 found",
        "✓ Creating ~/.hermes/ directory structure",
        "✓ Installing core dependencies",
        "✓ Setting up virtual environment",
        "✓ Installing CLI entry point",
        "",
        "✅ Installation complete!",
        "$ hermes --version",
        "hermes 2.2.0 — Nous Research",
    ], "One command install — ready in 60 seconds", 0.6),
    
    # Scene 3: First chat + model setup
    (10, [
        "",
        "Step 2: Configure & Chat",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "$ hermes setup",
        "",
        "  ◇ Select model provider: OpenRouter",
        "  ◇ Enter API key: **************",
        "  ◇ Enable tools: web, terminal, file",
        "  ✓ Configuration saved",
        "",
        "$ hermes",
        "╭──────────────────────────────────────────────╮",
        "│  Hermes Agent 2.2.0  •  Model: deepseek-chat │",
        "╰──────────────────────────────────────────────╯",
        "",
        "You: install nginx and configure it as a reverse proxy",
    ], "Choose your LLM provider — works with 20+ models", 0.5),
    
    # Scene 4: Agent running
    (12, [
        "",
        "Hermes processes your request...",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "> 🔍 Checking server OS... Ubuntu 22.04",
        "> 📦 Installing nginx via apt...",
        "   Reading package lists... Done",
        "   Building dependency tree... Done",
        "   nginx is already the newest version (1.24)",
        "",
        "> ⚙  Configuring nginx as reverse proxy...",
        "   Creating /etc/nginx/sites-available/app",
        "   Setting up proxy_pass to localhost:3000",
        "   Enabling site configuration",
        "   Testing nginx configuration... OK",
        "",
        "> 🔄 Restarting nginx... Done",
        "",
        "✅ Nginx installed and configured!",
        "   Your app is now accessible via port 80.",
    ], "Hermes runs real commands — installs, configures, deploys", 0.5),
    
    # Scene 5: Telegram
    (12, [
        "",
        "Step 3: Connect Telegram Bot",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "$ hermes gateway setup",
        "",
        "  ◇ Platform: Telegram",
        "  ◇ Bot token from BotFather: **********",
        "  ◇ Install as systemd service... Done",
        "",
        "✓ Gateway running! Your agent is online 24/7",
        "",
        "── Telegram Chat ───────────────────────────────",
        "You: check server health",
        "Bot: 🔍 Running diagnostics...",
        "     CPU: 12% | RAM: 1.2/3.8GB | Disk: 45%",
        "     ✓ All services running normally",
        "",
        "You: deploy the latest build",
        "Bot: 🚀 Deploying... pulled, built, restarted ✅",
    ], "Message your agent from anywhere via Telegram", 0.5),
    
    # Scene 6: Skills
    (12, [
        "",
        "Step 4: Create Custom Skills",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "Skills are reusable procedures your agent remembers.",
        "One command → complex multi-step automation.",
        "",
        "$ hermes skills list",
        "",
        "  📦 Installed Skills (48):",
        "  ├─ deploy-flask    → Full Flask deployment pipeline",
        "  ├─ audit-server    → Security & performance audit",
        "  ├─ scrape-data     → Web scraping with export",
        "  ├─ monitor-health  → Server health check + alert",
        "  └─ backup-db      → Database backup & rotation",
        "",
        "$ hermes",
        "You: run monitor-health every 30 min and alert me on Telegram",
        "Hermes: ✓ Cron job created — monitoring your server!",
    ], "Skills = reusable automation. Your agent gets smarter every day.", 0.5),
    
    # Scene 7: VPS Deployment
    (10, [
        "",
        "Step 5: Deploy 24/7 on a VPS",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "$ ssh root@your-server",
        "$ curl -fsSL https://get.hermes | bash",
        "$ hermes setup",
        "$ hermes gateway install",
        "$ systemctl status hermes-gateway",
        "",
        "● hermes-gateway.service — Hermes Agent Gateway",
        "   Loaded: loaded (/etc/systemd/system/)",
        "   Active: active (running) since 2026-05-23",
        "   Main PID: 1234 (python3)",
        "   Memory: 180MB | CPU: 0.5%",
        "",
        "Total cost: $5/mo for the VPS.",
        "Your agent runs 24/7, accessible from anywhere.",
    ], "Full deployment on a $5/mo VPS — runs 24/7", 0.6),
    
    # Scene 8: Outro
    (10, [
        "",
        "What You Just Built in 90 Seconds:",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "✅ Hermes Agent installed and configured",
        "✅ Connected to your preferred LLM (20+ options)",
        "✅ Telegram bot — message your agent from your phone",
        "✅ Custom skills — reusable automation procedures",
        "✅ VPS deployment — 24/7 operation for $5/mo",
        "✅ Cron jobs, webhooks, and monitoring",
        "",
        "Now imagine what you can automate:",
        "→ Deploy servers in one command",
        "→ Monitor infrastructure from Telegram",
        "→ Scrape data and generate reports",
        "→ Automate your entire workflow",
        "",
        "The full course covers all of this and more.",
    ], "90 seconds — from zero to a fully operational AI agent", 0.7),
]

def generate_frames():
    total_frames = sum(int(dur * FPS) for dur, _, _, _ in SCENES)
    frame_idx = 0
    
    # Generate a subtle animated background glow that changes per scene
    for scene_idx, (duration, lines, caption, speed) in enumerate(SCENES):
        scene_frames = int(duration * FPS)
        # Calculate typing: when do we finish drawing all lines?
        # Lines visible = progress * total_lines, where progress ramps up
        
        total_lines = len(lines)
        # At what frame do we finish typing?
        # Faster typing = finish earlier, slower = later
        type_end_frame = int(scene_frames * speed)  # finish typing at this % of scene
        
        for f in range(scene_frames):
            frame_global = frame_idx + f
            time_pct = f / scene_frames
            
            if time_pct < 0.1:
                # Brief pause before typing starts
                progress = 0
            elif time_pct < speed:
                # Typing phase
                typing_progress = (time_pct - 0.1) / (speed - 0.1)
                typing_progress = min(1.0, max(0, typing_progress))
                progress = typing_progress
            else:
                # All lines visible, maybe flash a highlight
                progress = 1.0
            
            # Slight color cycling for highlight at end
            highlight = None
            if progress >= 1.0:
                pulse = (math.sin(frame_global * 0.1) + 1) * 0.5
                if pulse > 0.85:
                    # Highlight last line
                    pass
            
            img = draw_frame(lines, progress, highlight=highlight, caption=caption)
            img.save(str(FRAMES_DIR / f"frame_{frame_global:06d}.png"))
        
        frame_idx += scene_frames
    
    return total_frames

print("🎬 Generating 90-second demo video frames...")
total_frames = generate_frames()
print(f"   {total_frames} frames generated ({total_frames/FPS:.0f}s)")

print("\n▶ Generating voiceover narration...")
subprocess.run([
    "edge-tts",
    "--voice", "en-US-GuyNeural",
    "--text", 
    "Hermes Agent is an open source AI framework that runs in your terminal. "
    "It connects to any LLM provider and has real tools - web search, file editing, "
    "and terminal access. In this demo you will see how Hermes installs in one command, "
    "connects to Telegram, creates reusable skills, and deploys to a VPS. "
    "First, install Hermes with a single curl command. The installer handles everything. "
    "Next, configure your model provider - Hermes works with OpenRouter, Anthropic, "
    "OpenAI, DeepSeek, and over 20 others. "
    "Now the agent is running. Ask it to install Nginx, configure a reverse proxy, "
    "or deploy your application. Hermes executes real commands on your system. "
    "Connect Telegram for mobile access. Message your agent from anywhere - "
    "check server health, deploy updates, run diagnostics. "
    "Create reusable skills. Save complex workflows as one command skills. "
    "Your library of automation grows over time. "
    "Finally, deploy on a five dollar per month VPS. Your agent runs 24 7, "
    "accessible from Telegram, with cron jobs and webhooks. "
    "Master Hermes Agent - the complete course covers installation, configuration, "
    "skills, training, gateway setup, VPS deployment, and monetization. "
    "Enroll now and build your own AI assistant today.",
    "--rate", "+5%",
    "--write-media", str(BASE / "narration.mp3"),
], check=True)

# Get narration duration
dur = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "csv=p=0", str(BASE / "narration.mp3")
], capture_output=True, text=True)
narration_dur = float(dur.stdout.strip())
print(f"   Voiceover duration: {narration_dur:.1f}s")

print("\n▶ Compositing video with FFmpeg...")
# Create video from frames, add narration, loop or pad audio if needed
vid = str(BASE / "hermes_demo_narrated.mp4")

# First pass: create video from frames with audio
# Pad audio to match video or vice versa
vid_dur = total_frames / FPS
print(f"   Video duration: {vid_dur:.1f}s | Audio: {narration_dur:.1f}s")

# Build the final video - match video length to audio
subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", str(FRAMES_DIR / "frame_%06d.png"),
    "-i", str(BASE / "narration.mp3"),
    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
    "-c:a", "aac", "-b:a", "128k",
    "-pix_fmt", "yuv420p",
    "-shortest",
    str(vid)
], check=True)

# Check output
sz = os.path.getsize(vid)
out_dur = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "csv=p=0", vid
], capture_output=True, text=True)
print(f"\n✅ Demo video ready!")
print(f"   Path: {vid}")
print(f"   Size: {sz/1024/1024:.1f} MB")
print(f"   Duration: {float(out_dur.stdout.strip()):.1f}s")
print(f"   Resolution: {W}x{H} @ {FPS}fps")

# Also export a version without audio for the website
vid_no_audio = str(BASE / "hermes_demo.mp4")
subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", str(FRAMES_DIR / "frame_%06d.png"),
    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-frames:v", str(total_frames),
    vid_no_audio
], check=True)
print(f"   (Also saved silent version: {sz/1024/1024:.1f} MB)")
