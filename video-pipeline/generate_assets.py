#!/usr/bin/env python3
"""Generate background scenes and ASS caption files for all 10 module videos."""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

PIPELINE = "/root/hermes-course/video-pipeline"
os.makedirs(f"{PIPELINE}/scenes", exist_ok=True)
os.makedirs(f"{PIPELINE}/captions", exist_ok=True)
os.makedirs(f"{PIPELINE}/audio", exist_ok=True)

W, H = 1920, 1080
FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

# Module script data
MODULES_SCRIPTS = {
    1: {"title": "What is Hermes Agent & Why It Matters", "subtitle": "What Makes It Different", "duration": 150},
    2: {"title": "Installation & First Run", "subtitle": "One Command to Install", "duration": 160},
    3: {"title": "Configuration Deep Dive", "subtitle": "Master Every Config Option", "duration": 155},
    4: {"title": "Daily Usage & Power Features", "subtitle": "Become a Power User", "duration": 160},
    5: {"title": "Skills System", "subtitle": "The Killer Feature", "duration": 160},
    6: {"title": "Training Your Agent", "subtitle": "Memory & Teaching Workflows", "duration": 150},
    7: {"title": "Multi-Platform Gateway", "subtitle": "One Agent Everywhere", "duration": 150},
    8: {"title": "VPS Deployment", "subtitle": "24/7 on a $5 VPS", "duration": 150},
    9: {"title": "Monetization Strategies", "subtitle": "7 Ways to Make Money", "duration": 160},
    10: {"title": "Advanced Use Cases", "subtitle": "Production-Ready Systems", "duration": 160},
}

# Caption segments per module
CAPTIONS = {
    1: [(0, 8, "Welcome to Module 1"), (8, 16, "What makes Hermes Agent fundamentally different"),
        (16, 27, "ChatGPT gives you answers. Hermes gets things done."), (27, 38, "It lives in your terminal. Connected to everything."),
        (38, 48, "It runs commands, writes files, fixes errors automatically"), (48, 58, "Open source. MIT license. Built by Nous Research."),
        (58, 68, "20+ LLM providers. Zero lock-in."), (68, 80, "Persistent memory. Self-improving skills."),
        (80, 92, "70+ tools. Multi-platform. Cron jobs."), (92, 105, "Runs 24/7 on a $5 VPS"),
        (105, 120, "This isn't a chatbot. It's your autonomous agent."), (120, 150, "Let's get started with Module 1")],
    2: [(0, 8, "Install Hermes Agent in under 5 minutes"), (8, 18, "One command to install: curl | bash"),
        (18, 28, "Docker also available: docker run"), (28, 38, "Setup wizard guides you step by step"),
        (38, 48, "Start with OpenRouter - one key, 200+ models"), (48, 60, "Your first conversation - ask it anything"),
        (60, 72, "Hermes reads files, runs commands, explores"), (72, 85, "Stuck? hermes doctor diagnoses everything"),
        (85, 100, "Active community on Discord and GitHub"), (100, 130, "Hermes running and ready to work"),
        (130, 160, "Module 2 complete - you're ready for configuration")],
    3: [(0, 8, "Module 3: Configuration Deep Dive"), (8, 18, "Two files: config.yaml and .env"),
        (18, 28, "Version control safe - no credential leaks"), (28, 40, "Config hierarchy: defaults to user to project to env"),
        (40, 52, "Model providers and fallback chains"), (52, 65, "Route tasks to different models"),
        (65, 78, "Profiles for different contexts"), (78, 90, "Coding, DevOps, Research profiles"),
        (90, 105, "Tool security and approval gates"), (105, 130, "Fully tuned configuration ready"), (130, 155, "Module 3 complete")],
    4: [(0, 8, "Module 4: Daily Usage & Power Features"), (8, 18, "Interactive chat vs single query mode"),
        (18, 28, "20+ slash commands"), (28, 40, "New, Model, Save, Background"),
        (40, 52, "Subagent delegation"), (52, 65, "Parallel task execution"),
        (65, 75, "Cron jobs for scheduled automation"), (75, 88, "Event-driven webhooks"),
        (88, 100, "GitHub, Stripe, custom integrations"), (100, 130, "You're now a Hermes power user"),
        (130, 160, "Ready for Module 5: Skills System")],
    5: [(0, 8, "Module 5: Skills System"), (8, 18, "The killer feature of Hermes Agent"),
        (18, 28, "Most AI assistants are amnesiacs"), (28, 40, "Skills = permanent, reusable knowledge"),
        (40, 52, "Markdown files with structured frontmatter"), (52, 65, "Create once, use forever"),
        (65, 78, "Skill Hub ecosystem"), (78, 90, "Browse, install, publish skills"),
        (90, 105, "50+ skills = agent that knows your stack"), (105, 130, "The compound learning effect"), (130, 160, "Module 5 complete")],
    6: [(0, 8, "Module 6: Training Your Agent"), (8, 18, "Skills = capabilities. Training = preferences."),
        (18, 28, "Memory system: facts and profile"), (28, 40, "Corrections pipeline"),
        (40, 52, "Every correction is a permanent improvement"), (52, 65, "Session search: find any past conversation"),
        (65, 78, "The compound effect of training"), (78, 92, "Agent that knows your entire workflow"),
        (92, 120, "Anticipates your needs"), (120, 150, "Module 6 complete")],
    7: [(0, 8, "Module 7: Multi-Platform Gateway"), (8, 18, "One agent, every platform"),
        (18, 28, "Telegram, Discord, Slack, WhatsApp, Signal"), (28, 38, "Same agent, different interfaces"),
        (38, 50, "Continue conversations across platforms"), (50, 62, "Setup: hermes gateway setup"),
        (62, 75, "Install as systemd service"), (75, 88, "Security: allowlists, pairing, tiers"),
        (88, 100, "Cron jobs deliver anywhere"), (100, 130, "One agent everywhere you need it"), (130, 150, "Module 7 complete")],
    8: [(0, 8, "Module 8: VPS Deployment"), (8, 18, "From laptop to production"),
        (18, 28, "$5/month VPS is all you need"), (28, 40, "30-minute setup guide"),
        (40, 52, "Security hardening"), (52, 65, "Systemd auto-start on boot"),
        (65, 78, "Monitoring & health checks"), (78, 92, "Never offline, always running"),
        (92, 120, "Access your agent from anywhere"), (120, 150, "Module 8 complete")],
    9: [(0, 8, "Module 9: Monetization Strategies"), (8, 18, "7 ways to make money with Hermes"),
        (18, 28, "Agent as a Service: $20-50 per month"), (28, 40, "Local business automation: $500-5000"),
        (40, 52, "Custom skill development: $100-500"), (52, 65, "Affiliate marketing: passive income"),
        (65, 78, "Sell this course"), (78, 90, "White-label Hermes: $2K-5K setup"),
        (90, 105, "SaaS product: highest reward"), (105, 130, "MIT license = full freedom"), (130, 160, "Module 9 complete")],
    10: [(0, 8, "Module 10: Advanced Use Cases"), (8, 18, "Production-ready Hermes systems"),
         (18, 28, "Trading bots: 24/7 market automation"), (28, 40, "Content automation: script to publish"),
         (40, 52, "Code review bots with webhooks"), (52, 65, "Customer support agents"),
         (65, 78, "Multi-agent orchestration"), (78, 90, "Full development pipeline automation"),
         (90, 105, "Research, build, test, deploy"), (105, 130, "Welcome to the future of AI agents"),
         (130, 160, "Course complete! Here is your certificate")],
}

# Scene colors per module
SCENE_COLORS = {
    1: ["#05050b", "#0a0a1a", "#0f0f20", "#0a0a18", "#050510", "#080818"],
    2: ["#05050b", "#0a0a1a", "#0f0f20", "#0a0a18", "#080818", "#050510"],
    3: ["#05050b", "#0a0a1a", "#0f0f20", "#0a0a18", "#080818", "#050510"],
    4: ["#05050b", "#0a0a1a", "#0f0f20", "#0a0a18", "#080818", "#050510"],
    5: ["#05050b", "#0a0a1a", "#0f0f20", "#0a0a18", "#080818", "#050510"],
    6: ["#05050b", "#0a0a1a", "#0f0f20", "#0a0a18", "#080818", "#050510"],
    7: ["#05050b", "#0a0a1a", "#0f0f20", "#0a0a18", "#080818", "#050510"],
    8: ["#05050b", "#0a0a1a", "#0f0f20", "#0a0a18", "#080818", "#050510"],
    9: ["#05050b", "#0a0a1a", "#0f0f20", "#0a0a18", "#080818", "#050510"],
    10: ["#05050b", "#0a0a1a", "#0f0f20", "#0a0a18", "#080818", "#050510"],
}

SCENE_TITLES = {
    1: ["Hermes Agent", "What Makes It Different", "Open Source & Provider Agnostic", "Key Superpowers", "Self-Hosted & Always On", "Let's Begin"],
    2: ["Installation & First Run", "One Command Install", "Setup Wizard", "Your First Conversation", "Troubleshooting", "Ready for Module 3"],
    3: ["Configuration Deep Dive", "Config Files & Hierarchy", "Model Providers & Fallbacks", "Profiles & Routing", "Tool Security", "Ready for Module 4"],
    4: ["Daily Usage & Power Features", "Interactive Mode & Slash Commands", "Subagent Delegation", "Cron Jobs & Scheduling", "Webhook Integration", "Ready for Module 5"],
    5: ["Skills System", "The Problem with Amnesiac AI", "How Skills Work", "Skill Hub Ecosystem", "The Compound Effect", "Ready for Module 6"],
    6: ["Training Your Agent", "Memory System", "Corrections Pipeline", "Session Search", "The Compound Effect", "Ready for Module 7"],
    7: ["Multi-Platform Gateway", "One Agent, Every Platform", "Setup & Configuration", "Security & Access Control", "Cross-Platform Cron Delivery", "Ready for Module 8"],
    8: ["VPS Deployment", "Why a VPS?", "30-Minute Setup", "Security Hardening", "Monitoring & Uptime", "Ready for Module 9"],
    9: ["Monetization Strategies", "Agent as a Service", "Local Business Automation", "Skills & White-Label", "SaaS & Affiliate", "Ready for Module 10"],
    10: ["Advanced Use Cases", "Trading Bots", "Content Automation", "Code Review & Support", "Multi-Agent Systems", "Course Complete!"],
}

SCENE_DURATIONS = [8, 25, 25, 25, 25, 50]  # Total should be roughly each module's duration

def hex_to_rgb(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def generate_backgrounds(num):
    """Generate 1920x1080 background PNGs for each scene of a module."""
    colors = SCENE_COLORS[num]
    titles = SCENE_TITLES[num]
    out_dir = f"{PIPELINE}/scenes/module{num:02d}"
    os.makedirs(out_dir, exist_ok=True)
    
    font_lg = ImageFont.truetype(FONT_FILE, 72) if os.path.exists(FONT_FILE) else ImageFont.load_default()
    font_md = ImageFont.truetype(FONT_FILE, 40) if os.path.exists(FONT_FILE) else ImageFont.load_default()
    font_sm = ImageFont.truetype(FONT_FILE, 28) if os.path.exists(FONT_FILE) else ImageFont.load_default()
    
    for i in range(len(colors)):
        bg_color = hex_to_rgb(colors[i])
        img = Image.new('RGB', (W, H), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Grid pattern
        for x in range(0, W, 50):
            draw.line([(x, 0), (x, H)], fill=(hex_to_rgb('#1a1a2e') if bg_color[0] < 15 else hex_to_rgb('#0a0a1e')), width=1)
        for y in range(0, H, 50):
            draw.line([(0, y), (W, y)], fill=(hex_to_rgb('#1a1a2e') if bg_color[0] < 15 else hex_to_rgb('#0a0a1e')), width=1)
        
        # Top gradient accent line
        for x in range(0, W, 2):
            intensity = int(12 + 8 * abs((x / W) * 2 - 1))
            draw.rectangle([x, 0, x + 1, 3], fill=(intensity * 2, intensity, intensity * 3))
        
        # Module badge top-right
        badge_text = f"Module {num} / 10"
        bbox = draw.textbbox((0, 0), badge_text, font=font_sm)
        draw.text((W - bbox[2] - 30, 20), badge_text, fill=(hex_to_rgb('#6c5ce7')), font=font_sm)
        
        # Main title - centered
        title = titles[i]
        wrapped = textwrap.wrap(title, width=22)
        y_start = 340 - (len(wrapped) - 1) * 40
        
        for line_i, line in enumerate(wrapped):
            bbox = draw.textbbox((0, 0), line, font=font_lg)
            tw = bbox[2] - bbox[0]
            draw.text(((W - tw) // 2, y_start + line_i * 90), line,
                      fill=(hex_to_rgb('#a78bfa')), font=font_lg)
        
        # Subtitle for first scene
        if i == 0:
            subtitle = MODULES_SCRIPTS[num]["subtitle"]
            bbox = draw.textbbox((0, 0), subtitle, font=font_md)
            tw = bbox[2] - bbox[0]
            draw.text(((W - tw) // 2, 520), subtitle,
                      fill=(hex_to_rgb('#6c5ce7')), font=font_md)
        
        # Bottom decorative line
        for x in range(W // 2 - 100, W // 2 + 100, 2):
            alpha = int(80 * abs((x - W // 2 + 100) / 100))
            draw.rectangle([x, H - 40, x + 1, H - 38], fill=(alpha, alpha // 2, alpha))
        
        out_path = f"{out_dir}/scene_{i:02d}.png"
        img.save(out_path)
        print(f"  Scene {i}: {out_path}")
    
    # Create concat file
    durations = SCENE_DURATIONS.copy()
    total_scene = sum(durations)
    # Adjust last scene's duration to match module duration
    mod_dur = MODULES_SCRIPTS[num]["duration"]
    if total_scene != mod_dur:
        durations[-1] += mod_dur - total_scene
    
    with open(f"{out_dir}/concat.txt", 'w') as f:
        for i, dur in enumerate(durations):
            f.write(f"file scene_{i:02d}.png\nduration {dur}\n")
        f.write(f"file scene_{len(durations)-1:02d}.png\n")
    
    print(f"  Concat file: {out_dir}/concat.txt")
    return durations

def generate_ass(num, captions_list):
    """Generate ASS subtitle file for a module."""
    ass_path = f"{PIPELINE}/captions/module{num:02d}.ass"
    
    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1920",
        "PlayResY: 1080",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Cap,DejaVu Sans Bold,42,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,100,100,70,1",
        "Style: Title,DejaVu Sans Bold,36,&H00A78BFA,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,8,100,100,70,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    
    def to_ass(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = t % 60
        return f"{h}:{m:02d}:{s:05.2f}"
    
    for start, end, text in captions_list:
        ass_lines.append(f"Dialogue: 0,{to_ass(start)},{to_ass(end)},Cap,,0,0,0,,{text}")
    
    with open(ass_path, 'w') as f:
        f.write("\n".join(ass_lines))
    print(f"  ASS: {ass_path} ({len(captions_list)} captions)")

def generate_all():
    print("=" * 60)
    print("🎬 Generating backgrounds and captions for all 10 modules")
    print("=" * 60)
    
    for num in range(1, 11):
        print(f"\n📦 Module {num}: {MODULES_SCRIPTS[num]['title']}")
        generate_backgrounds(num)
        generate_ass(num, CAPTIONS[num])
    
    print(f"\n{'=' * 60}")
    print(f"✅ All assets generated in {PIPELINE}/")
    print("=" * 60)

if __name__ == "__main__":
    generate_all()
