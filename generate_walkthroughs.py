#!/usr/bin/env python3
"""
Generate 2-3 minute module walkthrough videos with voiceover + animated slides.
Each module gets a narrated walkthrough covering the key concepts.
"""
import os
import subprocess
import tempfile
import textwrap
import time

OUTPUT_DIR = "/root/hermes-course/course/videos"
W, H = 1920, 1080
FPS = 25

MODULE_DATA = [
    (1, "module-01-intro.md", "What is Hermes Agent & Why It Matters", [
        ("What is an AI Agent?", "Unlike chatbots that just answer questions, Hermes Agent is an AI that can use tools, run commands, edit files, browse the web, and execute multi-step workflows automatically."),
        ("Chatbots vs Hermes", "ChatGPT tells you what to do. Hermes does it for you. It runs commands, edits files, tests code, and remembers what it learned."),
        ("Core Architecture", "Open-source by Nous Research. Runs in your terminal. Connects to 20+ LLM providers. Has persistent memory, a skills system, and tool calling."),
        ("Why Self-Hosted?", "Your data stays on your machine. MIT license - free forever. No subscriptions. Runs on your laptop or a $5 VPS."),
        ("What You'll Build", "By the end of this course, you'll have a fully autonomous AI agent running 24/7, connected to Telegram, with custom skills and monetization ready."),
    ]),
    (2, "module-02-installation.md", "Installation & First Run", [
        ("One Command Install", "Install Hermes with a single command: pip install hermes-agent. Works on Mac, Linux, and Windows via WSL2."),
        ("Setup Wizard", "The first run wizard walks you through selecting a model provider, configuring API keys, and setting up your agent name."),
        ("First Conversation", "Your first interaction with Hermes. Ask it to run a command, search the web, or help with a task. Watch it work in real time."),
        ("Docker Setup", "Prefer containers? Hermes has a Docker image. Pull it, run it, and you're ready to go in minutes."),
        ("Configuration Options", "Choose from 20+ LLM providers, configure toolsets, set up memory, and customize your agent's behavior."),
    ]),
    (3, "module-03-configuration.md", "Configuration Deep Dive", [
        ("Model Providers", "Connect to OpenAI, Anthropic Claude, DeepSeek, Google Gemini, OpenRouter, or even local models via Ollama. Switch anytime."),
        ("API Keys & Security", "Store API keys securely using .env files. Never commit them to Git. Hermes loads them automatically."),
        ("Toolsets Explained", "Enable specific tools: file operations, web browsing, code execution, browser automation. Only give your agent what it needs."),
        ("Profiles System", "Create multiple profiles for different use cases. One for development, one for trading, one for personal assistant."),
        ("Memory Configuration", "Configure how your agent remembers. Short-term session memory and long-term persistent memory that survives restarts."),
    ]),
    (4, "module-04-usage.md", "Daily Usage & Power Features", [
        ("Slash Commands", "Quick commands like /help, /memory, /skills, /config. Access every feature without leaving the terminal."),
        ("Subagent Delegation", "Spawn child agents to handle subtasks in parallel. One agent researches, another writes code, a third tests it."),
        ("Cron Jobs", "Schedule your agent to run tasks automatically. Daily reports, health checks, market monitoring - set it and forget it."),
        ("Webhooks", "Trigger your agent via HTTP requests. Integrate with GitHub, Stripe, Zapier, or any service that sends webhooks."),
        ("Sessions & Checkpoints", "Save your agent's state and resume later. Perfect for long-running research or complex multi-step tasks."),
    ]),
    (5, "module-05-skills.md", "Skills System - The Killer Feature", [
        ("What Are Skills?", "Skills are reusable procedures your agent can run on command. Think of them as your agent's muscle memory."),
        ("Creating Your First Skill", "Write a skill file, test it, install it. Your agent can now perform that task on demand."),
        ("Skill Libraries", "The Hermes ecosystem has 48+ built-in skills. Deploy servers, audit code, scrape websites, monitor systems."),
        ("Self-Improving Skills", "Skills learn from corrections. The more you use them, the better they get. Your agent gets smarter every day."),
        ("Publishing Skills", "Share your skills with the community. Build a reputation as a skill author."),
    ]),
    (6, "module-06-training.md", "Training Your Agent", [
        ("Persistent Memory", "Your agent remembers everything it learns across sessions. No more repeating yourself."),
        ("Teaching Your Agent", "Correct mistakes, add examples, set preferences. Your agent learns how you like things done."),
        ("Correction Workflows", "When your agent makes a mistake, correct it once. It remembers and does better next time."),
        ("User Profiles", "Configure your agent to know who you are, what you do, and how you prefer to work."),
        ("Learning Loop", "Every interaction is a training opportunity. Over time, your agent becomes uniquely tuned to your workflows."),
    ]),
    (7, "module-07-gateway.md", "Multi-Platform Gateway", [
        ("Telegram Integration", "Connect your agent to Telegram via BotFather. Message your agent from anywhere."),
        ("Discord Setup", "Add your agent to Discord servers. It can monitor channels, respond to questions, and run commands."),
        ("WhatsApp Connection", "Connect your agent to WhatsApp for personal assistant workflows."),
        ("Cross-Platform", "The same agent works everywhere. Start a task on Telegram, check progress on Discord."),
        ("Use Cases", "Server alerts on Telegram, customer support on Discord, personal assistant on WhatsApp."),
    ]),
    (8, "module-08-vps.md", "VPS Deployment", [
        ("VPS Setup", "Get a $5/month VPS from DigitalOcean, Hetzner, or Vultr. Deploy Ubuntu, secure it with SSH keys."),
        ("Security Hardening", "Enable firewall, disable root login, set up fail2ban. Complete security checklist included."),
        ("systemd Service", "Run Hermes as a background service. It starts on boot, restarts on crash, logs everything."),
        ("Monitoring", "Set up health checks, resource monitoring, and Telegram alerts. Know if your agent goes down."),
        ("24/7 Operation", "Your agent never sleeps. Cron jobs, webhooks, and continuous monitoring run around the clock."),
    ]),
    (9, "module-09-monetization.md", "Monetization Strategies", [
        ("Agent as a Service", "Build custom agents for clients. Automate their workflows. Charge monthly."),
        ("White-Label Solutions", "Rebrand Hermes as your own product. Sell access to clients with custom skills."),
        ("Skills Marketplace", "Create and sell premium skills. Build a library and generate passive income."),
        ("SaaS Model", "Build a multi-tenant platform. Hundreds of users, one infrastructure."),
        ("Pricing Strategies", "How to price your services. From $500/month for basic setups to $10K/month for enterprise."),
    ]),
    (10, "module-10-advanced.md", "Advanced Use Cases", [
        ("Trading Bots", "Build automated trading bots that monitor markets and execute trades based on your strategy."),
        ("Content Automation", "Generate blog posts, social media content, and marketing copy automatically."),
        ("Code Review Assistant", "Set up your agent to review pull requests, find bugs, and suggest improvements."),
        ("Customer Support", "Automate support responses. Your agent handles common questions, escalates complex ones."),
        ("Data Pipelines", "Build ETL pipelines, data cleaning workflows, and automated reporting systems."),
    ]),
]

SLIDE_TEMPLATES = {
    "title": {
        "bg": (5, 5, 11),
        "accent": "#6c5ce7",
        "title_color": (167, 139, 250),
    },
    "content": {
        "bg": (5, 5, 11),
        "accent": "#00cec9",
        "title_color": (0, 206, 201),
    },
    "outro": {
        "bg": (5, 5, 11),
        "accent": "#6c5ce7",
        "title_color": (167, 139, 250),
    },
}


def generate_narration(text, module_num):
    """Generate voiceover audio using Edge TTS."""
    out_path = os.path.join(OUTPUT_DIR, f"module-{module_num:02d}_narration.mp3")
    if os.path.exists(out_path):
        return out_path
    
    # Use edge-tts via terminal
    cmd = [
        "edge-tts",
        "--voice", "en-US-JennyNeural",
        "--text", text,
        "--write-media", out_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  TTS error: {result.stderr}")
        return None
    
    duration = get_audio_duration(out_path)
    print(f"  Narration: {duration:.1f}s")
    return out_path


def get_audio_duration(path):
    """Get audio duration in seconds."""
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ], capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 0


def make_slide(slide_type, title, body_lines, progress, frame_num, total_frames):
    """Generate a single frame as PNG."""
    from PIL import Image, ImageDraw, ImageFont
    
    img = Image.new('RGB', (W, H), (5, 5, 11))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        font_footer = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except:
        font_title = font_body = font_footer = ImageFont.load_default()
    
    # Grid background
    for x in range(0, W, 60):
        for y in range(0, H, 60):
            draw.point((x, y), fill=(12, 12, 28))
    
    # Top accent line
    accent_colors = {
        "title": (108, 92, 231),
        "content": (0, 206, 201),
        "outro": (108, 92, 231),
    }
    accent = accent_colors.get(slide_type, (108, 92, 231))
    for x in range(0, W, 2):
        intensity = 0.5 + 0.5 * abs((x / W) * 2 - 1)
        draw.rectangle([x, 0, x + 1, 3], fill=(int(accent[0] * intensity), int(accent[1] * intensity), int(accent[2] * intensity)))
    
    if slide_type == "title":
        # Fade in title
        alpha = min(255, int(255 * progress))
        # Big module number behind
        num_color = (int(alpha * 0.08), int(alpha * 0.06), int(alpha * 0.12))
        draw.text((W // 2 - 400, 80), f"Module {frame_num // 100 + 1}", fill=num_color, font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 160))
        
        # Module badge
        bbox = draw.textbbox((0, 0), f"MODULE {frame_num // 100 + 1}", font=font_footer)
        tw = bbox[2] - bbox[0]
        draw.rounded_rectangle([W // 2 - tw // 2 - 20, 250, W // 2 + tw // 2 + 20, 290], radius=8, fill=(108, 92, 231, int(alpha * 0.3)))
        draw.text((W // 2 - tw // 2, 255), f"MODULE {frame_num // 100 + 1}", fill=(int(alpha), int(alpha * 0.8), int(alpha * 1.0)), font=font_footer)
        
        # Title
        lines = textwrap.wrap(title, width=25)
        for li, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_title)
            tw = bbox[2] - bbox[0]
            c = int(alpha * 0.9)
            draw.text(((W - tw) // 2, 340 + li * 75), line, fill=(c, c, min(255, c + 20)), font=font_title)
    
    elif slide_type == "content":
        # Body text - fade in line by line
        for li, line in enumerate(body_lines):
            line_alpha = max(0, min(255, int(255 * (progress * len(body_lines) - li))))
            if line_alpha <= 0:
                continue
            
            c = int(line_alpha * 0.8)
            y = 320 + li * 75
            
            # Bullet point
            draw.ellipse([300, y + 10, 315, y + 25], fill=(int(c * 0.6), c, int(c * 0.6)))
            
            bbox = draw.textbbox((0, 0), line, font=font_body)
            draw.text((340, y + 2), line, fill=(c, c, c), font=font_body)
    
    elif slide_type == "outro":
        # Fade in
        alpha = min(255, int(255 * progress))
        
        # Terminal-style box
        draw.rounded_rectangle([350, 280, 1570, 500], radius=14, fill=(10, 10, 20), outline=(int(alpha * 0.3), int(alpha * 0.2), int(alpha * 0.4)))
        draw.rounded_rectangle([350, 280, 1570, 320], radius=14, fill=(15, 15, 30))
        draw.rectangle([350, 305, 1570, 320], fill=(15, 15, 30))
        
        for li, line in enumerate(body_lines):
            bbox = draw.textbbox((0, 0), line, font=font_body)
            c = int(alpha * 0.9)
            color = (int(c * 0.7), c, int(c * 0.6)) if li == 0 else (c, c, c)
            draw.text((400, 340 + li * 50), line, fill=color, font=font_body)
        
        # Cursor blink
        if frame_num % 12 < 6:
            draw.text((400 + len(body_lines[-1]) * 17, 340 + (len(body_lines) - 1) * 50), "_", fill=(0, 206, 201), font=font_body)
    
    return img


def generate_module_video(num, title, slides_data, narration_text):
    """Generate a complete module walkthrough video."""
    out_path = os.path.join(OUTPUT_DIR, f"module-{num:02d}-walkthrough.mp4")
    if os.path.exists(out_path):
        size = os.path.getsize(out_path) / 1024 / 1024
        print(f"  Already exists: {size:.1f} MB")
        return out_path
    
    # 1. Generate narration
    print(f"  Generating narration...")
    audio_path = generate_narration(narration_text, num)
    if not audio_path:
        return None
    
    audio_duration = get_audio_duration(audio_path)
    
    # 2. Calculate frames needed
    total_frames = int(audio_duration * FPS) + FPS * 2  # audio + 2 seconds buffer
    
    # 3. Create slide plan based on audio timing
    # Each slide gets equal time
    num_slides = len(slides_data) + 2  # title + content slides + outro
    frames_per_slide = total_frames // num_slides
    
    # 4. Render frames
    print(f"  Rendering {total_frames} frames ({audio_duration:.1f}s audio)...")
    
    temp_dir = tempfile.mkdtemp()
    frames_dir = os.path.join(temp_dir, "frames")
    os.makedirs(frames_dir)
    
    frame_idx = 0
    
    # Title slide
    for i in range(frames_per_slide):
        progress = i / frames_per_slide
        img = make_slide("title", title, [], progress, i, frames_per_slide)
        img.save(os.path.join(frames_dir, f"frame_{frame_idx:06d}.png"))
        frame_idx += 1
        if i % 100 == 0:
            print(".", end="", flush=True)
    
    # Content slides
    for slide_title, slide_body in slides_data:
        body_lines = textwrap.wrap(slide_body, width=60)
        for i in range(frames_per_slide):
            progress = i / frames_per_slide
            img = make_slide("content", slide_title, body_lines, progress, i, frames_per_slide)
            img.save(os.path.join(frames_dir, f"frame_{frame_idx:06d}.png"))
            frame_idx += 1
            if i % 100 == 0:
                print(".", end="", flush=True)
    
    # Outro slide
    outro_lines = [
        "Continue to the next module",
        "for more advanced concepts.",
        "",
        "hermes-course@agentmail.to",
    ]
    for i in range(frames_per_slide):
        progress = i / frames_per_slide
        img = make_slide("outro", "Module Complete", outro_lines, progress, i, frames_per_slide)
        img.save(os.path.join(frames_dir, f"frame_{frame_idx:06d}.png"))
        frame_idx += 1
        if i % 100 == 0:
            print(".", end="", flush=True)
    
    print(f" done ({frame_idx} frames)")
    
    # 5. Combine frames + audio into video
    print("  Compositing video...")
    video_temp = os.path.join(temp_dir, "video.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%06d.png"),
        "-i", audio_path,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        video_temp
    ]
    subprocess.run(cmd, capture_output=True)
    
    # 6. Copy to final destination
    subprocess.run(["cp", video_temp, out_path])
    
    size = os.path.getsize(out_path) / 1024 / 1024
    print(f"  Video: {os.path.basename(out_path)} ({size:.1f} MB)")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    
    return out_path


def build_narration_script(num, title, slides_data):
    """Build a natural narration script from slide data."""
    lines = [f"Welcome to Module {num}: {title}."]
    lines.append("")
    
    for slide_title, slide_body in slides_data:
        lines.append(slide_body)
    
    lines.append("")
    lines.append("This concludes this module. Continue to the next module for more advanced concepts.")
    lines.append("Happy building with Hermes Agent!")
    
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("GENERATING MODULE WALKTHROUGH VIDEOS WITH VOICEOVER")
    print("=" * 60)
    
    for num, filename, title, slides_data in MODULE_DATA:
        print(f"\nModule {num}: {title}")
        
        # Build narration
        narration = build_narration_script(num, title, slides_data)
        
        # Generate video
        generate_module_video(num, title, slides_data, narration)
        
        print(f"  Done!")
    
    print("\n" + "=" * 60)
    print("ALL MODULE WALKTHROUGH VIDEOS COMPLETE!")
    print("=" * 60)
    
    # List all walkthrough videos
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if "walkthrough" in f:
            path = os.path.join(OUTPUT_DIR, f)
            size = os.path.getsize(path) / 1024 / 1024
            print(f"  {f} - {size:.1f} MB")


if __name__ == "__main__":
    main()
