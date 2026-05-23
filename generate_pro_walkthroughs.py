#!/usr/bin/env python3
"""
Professional walkthrough video generator with real terminal demos + animated slides.
Combines slide-based explanations with actual Hermes Agent terminal output.
"""
import os, sys, subprocess, textwrap, json, time, shutil, re
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/root/hermes-course/course/videos"
W, H = 1920, 1080
FPS = 25

# ─── Font Setup ───
FONT_DIR = "/usr/share/fonts/truetype"
def find_font(name):
    for root, dirs, files in os.walk(FONT_DIR):
        for f in files:
            if name.lower() in f.lower():
                return os.path.join(root, f)
    return None

FONT_BOLD = find_font("DejaVuSans-Bold") or find_font("NotoSans-Bold") or "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_REG  = find_font("DejaVuSans") or "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = find_font("DejaVuSansMono") or "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def load_font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

def load_mono(size):
    return ImageFont.truetype(FONT_MONO, size)

# ─── Color Palette ───
BG1      = (5, 5, 11)       # deep dark
BG2      = (15, 15, 35)     # card bg
ACCENT   = (108, 92, 231)   # purple
ACCENT2  = (0, 206, 201)    # teal
WHITE    = (232, 232, 240)
GRAY     = (128, 128, 152)
DIM      = (60, 60, 80)
GREEN    = (80, 200, 120)
TERM_BG  = (15, 15, 20)
TERM_GREEN = (0, 255, 65)
TERM_WHITE = (200, 200, 200)
TERM_DIM   = (100, 100, 100)

# ─── Terminal Demo Data (real Hermes output) ───
TERMINAL_DEMOS = {
    "hermes_help": """$ hermes --help
Hermes Agent - AI assistant with tool-calling

Commands:
  chat       Interactive chat with the agent
  model      Select default model and provider
  gateway    Messaging gateway management
  setup      Interactive setup wizard
  config     Configuration management
  cron       Manage scheduled cron jobs
  skills     List and manage skills
  memory     View and edit persistent memory
  tools      List available tools
  doctor     System diagnostics
  version    Show version information""",

    "hermes_setup": """$ hermes setup
┌──────────────────────────────────┐
│   ⚡ Hermes Agent Setup Wizard   │
└──────────────────────────────────┘

? Select default provider:
  ▸ OpenRouter (200+ models)
    Anthropic (Claude)
    OpenAI (GPT-4o)
    Google (Gemini)
    DeepSeek
    xAI (Grok)

? Enter your API key: [hidden]

? Agent name: [Hermes]

✓ Setup complete! Type 'hermes' to start.""",

    "hermes_doctor": """$ hermes doctor
┌─────────────────────────────────┐
│         🩺 Hermes Doctor        │
└─────────────────────────────────┘

✓ Python 3.11.15
✓ Virtual environment active
✓ OpenAI SDK installed
✓ Configuration files present
✓ ~/.hermes directory exists
✓ API key configured
⚠ discord.py (optional)
⚠ Nous Portal (not logged in)""",

    "hermes_config": """$ hermes config show
model:
  default: deepseek-reasoner
  provider: deepseek

provider: deepseek
toolsets: [terminal, file, web, browser, skills]

gateway:
  telegram:
    enabled: true
    bot_token: [configured]

memory:
  enabled: true
  max_tokens: 2000""",

    "hermes_chat": """$ hermes chat
╭─────────────────────────────╮
│  💬 Hermes Agent - Ready    │
│  Model: deepseek-reasoner   │
╰─────────────────────────────╯

You: What tools do you have available?

Hermes: I have access to:

  terminal  - Run shell commands
  read_file - Read files with pagination
  write_file - Write content to files
  web_search - Search the internet
  web_extract - Extract content from URLs
  browser_* - Full browser automation
  memory - Persistent memory storage
  skills - Create and manage skills
  cronjob - Schedule automated tasks
  delegate_task - Spawn subagents

What would you like me to do?""",

    "hermes_skills": """$ hermes skills list
Available skills:

  plan              - Write implementation plans
  test-driven-dev   - TDD methodology
  systematic-debug  - Root cause debugging
  youtube-content   - YouTube transcript tool
  github-pr-workflow - PR lifecycle management
  architecture-diagram - SVG diagrams
  ascii-art         - Terminal art

Total: 48 skills loaded""",

    "hermes_gateway": """$ hermes gateway status
Platforms connected:

  Telegram  ✓  @MyHermesBot
  Discord   ✓  #hermes-agent
  Terminal  ✓  active

Webhooks:
  GitHub    ✓  PR review events
  Cron      ✓  3 jobs active

Status: All systems operational""",

    "hermes_cron": """$ hermes cron list
Scheduled jobs:

  morning-briefing
    Schedule: 0 8 * * *
    Next run: Tomorrow 08:00
    Skills: web, terminal

  market-report
    Schedule: 0 9 * * 1-5
    Next run: Mon 09:00
    Skills: web_search

  system-health
    Schedule: */30 * * * *
    Next run: 14:30 today""",

    "hermes_deploy": """$ ssh user@vps
user@vps:~$ curl -fsSL https://hermes.sh | bash
✓ Hermes installed
✓ Python 3.11 configured
✓ Node.js installed
✓ Dependencies ready

user@vps:~$ hermes setup
? Provider: OpenRouter
? API key: [configured]
? Agent name: Hermes

user@vps:~$ hermes gateway connect telegram
✓ Telegram bot connected
✓ Webhook registered

user@vps:~$ systemctl --user enable hermes
✓ Hermes will start on boot""",

    "hermes_memory": """$ hermes memory show
User Profile:
  Name: Developer
  Preference: Concise responses
  Preferred editor: VS Code
  Timezone: UTC

Memory entries:
  Project: hermes-course
  Stack: Python, Node.js, Vercel
  API keys configured: 3 providers

Skills created: 4 custom skills""",
}

# ─── Module content ───
# Each module: (num, filename, title, slides)
# Each slide: (heading, body_text, code_or_none, demo_key_or_none)
MODULES = [
    (1, "module-01-intro.md", "What is Hermes Agent & Why It Matters", [
        ("Welcome to the Course", "Welcome to Module 1 of the Hermes Agent Master Course. In this module, we explore what makes Hermes Agent different from regular chatbots and why it matters.", None, None),
        ("The Chatbot Problem", "Chatbots live in a browser tab. They answer questions but can't DO anything. Every output gets copy-pasted manually. Hermes breaks this pattern entirely.", None, None),
        ("Hermes Solves This", "Hermes lives in your terminal with full tool access. It runs commands, edits files, searches the web, deploys code, sends messages, and manages your infrastructure.", "hermes_help", None),
        ("Real Terminal Access", "This is what you see when you run Hermes. A full command suite at your fingertips. Not just chat — a complete agent OS.", None, "hermes_help"),
        ("Core Architecture", "Open source by Nous Research. 20+ LLM providers. Persistent memory. Skills system. 70+ built-in tools. Multi-platform gateway. Fully autonomous.", None, None),
        ("Provider Agnostic", "Works with OpenRouter, Anthropic, OpenAI, Google Gemini, DeepSeek, xAI Grok, or local models. Switch providers with one command.", "hermes_config", None),
        ("The Skills System", "Skills are procedural memory — markdown files that teach your agent how to do specific tasks. Load on demand, save tokens, improve over time.", "hermes_skills", None),
        ("Multi-Platform Gateway", "Connect Hermes to Telegram, Discord, WhatsApp, Slack, Signal. The same agent works everywhere. Start on Telegram, check on Discord.", "hermes_gateway", None),
        ("Persistent Memory", "Hermes remembers across sessions. Two memory layers: session context for current chat, persistent memory for long-term learning.", "hermes_memory", None),
        ("Autonomous Operation", "Set up cron jobs, webhooks, and automated workflows. Your agent monitors systems and acts even when you're away.", "hermes_cron", None),
        ("Subagent Delegation", "Spawn child agents for parallel work. One researches, another codes, a third tests. Multi-step workflows unlocked.", None, None),
        ("Self-Hosted & Private", "MIT licensed, free forever. Your data stays on your machine. Run on laptop or $5 VPS. No subscriptions.", None, None),
        ("What You'll Build", "By end of course: a 24/7 autonomous AI agent on VPS, connected to Telegram, with custom skills, ready to monetize.", None, None),
        ("Module Summary", "Hermes is open-source, self-hosted AI with tools, memory, skills, multi-platform, any LLM, 24/7 operation, zero cost. Let's install it in Module 2.", None, None),
    ]),
    (2, "module-02-installation.md", "Installation & First Run", [
        ("Installation & First Run", "In Module 2, we install Hermes Agent and have our first conversation. We'll cover the one-line installer, setup wizard, and verify everything works.", None, None),
        ("Prerequisites", "Just Git. On Ubuntu: sudo apt install git. On macOS: xcode-select --install. The installer handles Python, Node.js, FFmpeg, ripgrep automatically.", None, None),
        ("Getting an API Key", "Start with OpenRouter. Go to openrouter.ai/keys, sign up, create a key. Free credits included. 5 dollars unlocks full access.", None, None),
        ("One-Line Install", "Run the one-liner in your terminal. The installer detects your platform, installs everything, and sets up the environment in under 2 minutes.", None, None),
        ("What Gets Installed", "Clones the repo, creates a venv, installs Python deps, Node.js, Playwright browsers, ripgrep, FFmpeg. Symlinks the hermes command to your PATH.", None, None),
        ("Running the Setup", "After install, run 'source ~/.bashrc' then 'hermes'. The wizard asks for provider, API key, and agent name. Takes 2 minutes.", "hermes_setup", None),
        ("Setup Wizard Demo", "This is the setup wizard you'll see. Choose your provider, enter your key, name your agent. That's it.", None, "hermes_setup"),
        ("Docker Option", "Prefer containers? 'docker run -it ghcr.io/nousresearch/hermes-agent'. Pre-configured, mount a volume for persistence.", None, None),
        ("First Chat", "After setup, you're dropped into an interactive chat. Ask your agent anything. Try: 'What tools do you have?'", "hermes_chat", None),
        ("Check Health", "Run 'hermes doctor' to verify everything works. It checks Python, config files, API keys, and dependencies.", "hermes_doctor", None),
        ("Configure Your Setup", "Use 'hermes config show' to see your current configuration. Model, provider, toolsets, gateway settings, memory config.", None, "hermes_config"),
        ("Install Layout", "Code: ~/.hermes/hermes-agent. Venv: ~/.hermes/hermes-agent/venv. Config: ~/.hermes/config.yaml. Env: ~/.hermes/.env.", None, None),
        ("Module Summary", "Module 2 complete. Hermes is installed, configured, and running. You've had your first conversation and verified the setup. Next module: Configuration Deep Dive.", None, None),
    ]),
    (3, "module-03-configuration.md", "Configuration Deep Dive", [
        ("Configuration Deep Dive", "Module 3 explores configuration: model providers, toolsets, memory, security, and profiles. Your agent, finely tuned.", None, None),
        ("Model Providers", "Hermes supports 20+ providers. OpenRouter: 200+ models. Anthropic: Claude. OpenAI: GPT-4o. Google: Gemini. DeepSeek. xAI: Grok. Local: Ollama.", None, None),
        ("Switching Models", "Use 'hermes model' to change your default. Set fallback providers in case your primary fails. The agent automatically retries.", None, None),
        ("Toolsets Explained", "Toolsets group capabilities. Terminal, file, web, browser, skills, cron, delegation, git, mcp. Enable only what you need to save tokens.", "hermes_config", None),
        ("Memory Config", "Two tiers: session memory (current chat) and persistent (cross-session). Set max tokens for each. Memory grows with your agent.", None, None),
        ("Gateway Setup", "Connect to Telegram, Discord, WhatsApp, Slack. Each platform gets its own webhook URL. Your agent on every device.", "hermes_gateway", None),
        ("Security Model", "Protected mode requires approval for destructive commands. YOLO mode for full trust. Never mode denies dangerous actions. Audit log tracks everything.", None, None),
        ("Profiles", "Run separate profiles for different contexts. One for work, one for personal, one for each client. Each profile has its own config, memory, and skills.", None, None),
        ("Environment Variables", "All secrets in ~/.hermes/.env. API keys, tokens, webhook secrets. Never committed to git. Hermes reads them on startup.", None, None),
        ("Module Summary", "Configuration mastery: providers, toolsets, memory, security, profiles, env vars. Your agent is now perfectly tuned for your workflow.", None, None),
    ]),
    (4, "module-04-usage.md", "Daily Usage & Power Features", [
        ("Daily Usage & Power Features", "Module 4 covers advanced daily usage: slash commands, delegation, cron jobs, webhooks, sessions, and checkpoints.", None, None),
        ("Slash Commands", "Quick actions with /commands. /plan, /debug, /review, /skills, /memory, /session, /cron, /gateway. Available in chat and on connected platforms.", None, None),
        ("Delegation", "Spawn subagents with /delegate. Parallel research, code review, testing. Each subagent gets its own context. Results merged.", None, None),
        ("Cron Jobs", "Schedule recurring tasks. Morning briefings, market reports, system health checks. Your agent works while you sleep.", "hermes_cron", None),
        ("Webhooks", "Trigger actions from external events. GitHub pushes, emails, Stripe payments, webhooks. Event-driven automation at its finest.", None, None),
        ("Sessions & Checkpoints", "Save and restore sessions. Checkpoints let you branch experiments. Try one approach, checkpoint, try another path, restore.", None, None),
        ("Module Summary", "Power features: slash commands, delegation, cron, webhooks, sessions. Your agent is now a full automation platform.", None, None),
    ]),
    (5, "module-05-skills.md", "Skills System — The Killer Feature", [
        ("Skills System", "Module 5 covers Hermes' killer feature: Skills. Markdown files that teach your agent how to perform tasks. Procedural memory.", None, None),
        ("What Are Skills?", "Skills are SKILL.md files with YAML frontmatter. They contain task descriptions, step-by-step instructions, examples, and pitfalls. Loaded on-demand.", None, None),
        ("Loading Skills", "Use hermes with --skills flag. Skills auto-load based on task matching. You can also call skills directly in chat.", "hermes_skills", None),
        ("Creating Skills", "Write a SKILL.md with: name, description, trigger conditions, numbered steps, code examples, verification steps, and common pitfalls.", None, None),
        ("Skill Categories", "Skills organized by domain: software-dev, devops, data-science, mlops, creative, research, productivity, social-media, gaming.", None, None),
        ("The Skill Loop", "Create → Use → Improve. Every correction updates the skill. Your skills get better over time. Share skills with the community.", None, None),
        ("Module Summary", "Skills are your agent's procedural memory. Create, load, improve, share. This is what makes Hermes uniquely powerful.", None, None),
    ]),
    (6, "module-06-training.md", "Training Your Agent", [
        ("Training Your Agent", "Module 6: How to train your agent. Memory, corrections, user profiles, teaching workflows. Your agent learns your preferences over time.", None, None),
        ("The Correction Loop", "Correct your agent when it makes mistakes. 'No, use tabs not spaces.' 'Remember my database port.' Each correction updates memory.", None, None),
        ("User Profiles", "Set preferences: communication style, technical level, favorite tools, project conventions. Your agent adapts to you.", "hermes_memory", None),
        ("Memory Management", "View memory with 'hermes memory'. Add facts manually. Clear session context. Export and import memory between instances.", None, None),
        ("Teaching Workflows", "Teach multi-step workflows. 'When I say deploy, run tests first, then build, then push to production.' Saved as skills automatically.", None, None),
        ("Module Summary", "Training is continuous. Correct, teach, remember. Your agent becomes uniquely yours over weeks of use.", None, None),
    ]),
    (7, "module-07-gateway.md", "Multi-Platform Gateway", [
        ("Multi-Platform Gateway", "Module 7: Connect Hermes to Telegram, Discord, WhatsApp, Slack, Signal, Matrix. Run your agent everywhere.", None, None),
        ("Why Multi-Platform?", "Start a task on Telegram during commute. Check progress on Discord. Get alerts on WhatsApp. Same agent, everywhere, real-time.", "hermes_gateway", None),
        ("Telegram Setup", "Create a bot with @BotFather. Get your token. Configure in gateway. Telegram features: DMs, group chats, inline queries, voice messages.", None, None),
        ("Discord Setup", "Create a Discord app. Set message intents. Invite to server. Features: slash commands, threads, channels, role-based access.", None, None),
        ("WhatsApp Integration", "Connect via WhatsApp Business API. Send templates, handle inquiries, automate responses. Perfect for customer support.", None, None),
        ("VPS Deployment", "For 24/7 gateway, deploy on a VPS. Run as systemd service. Auto-restart on failure. Monitor with hermes cron.", "hermes_deploy", None),
        ("Module Summary", "Multi-platform gateway in action. Your agent on Telegram, Discord, WhatsApp, running 24/7 from a VPS.", None, None),
    ]),
    (8, "module-08-vps.md", "VPS Deployment", [
        ("VPS Deployment", "Module 8: Deploy Hermes on a $5 VPS for 24/7 operation. SSH setup, security, systemd service, monitoring.", None, None),
        ("Choosing a VPS", "DigitalOcean, Linode, Hetzner. $5-10/month. 1GB RAM, 25GB SSD is plenty. Ubuntu 22.04 or 24.04 recommended.", None, None),
        ("SSH & Security", "SSH key auth, disable password login. UFW firewall: allow 22, 80, 443. Fail2ban for brute force protection. Regular updates.", None, None),
        ("Install on VPS", "SSH in, run the one-liner. Same install process. Configure provider, set up gateway, enable services.", "hermes_deploy", None),
        ("Systemd Service", "Create a systemd user service. Auto-start on boot. Restart on failure. Logs via journalctl. Status via systemctl.", None, None),
        ("Production Checklist", "Firewall configured. Auto-updates enabled. Backups configured. Monitoring active. Webhook verified. Gateway online.", None, None),
        ("Module Summary", "VPS deployed with systemd, firewall, monitoring. Your agent runs 24/7, auto-restarts, and is production-ready.", None, None),
    ]),
    (9, "module-09-monetization.md", "Monetization Strategies", [
        ("Monetization Strategies", "Module 9: Seven ways to make money with Hermes Agent. Agent as a Service, white-label, SaaS, skills marketplace, and more.", None, None),
        ("1. Agent as a Service", "Offer managed Hermes instances for businesses. Setup, configuration, custom skills, ongoing support. Charge $50-500/month per client.", None, None),
        ("2. White-Label Solution", "Rebrand Hermes for agencies. Your logo, your pricing, your support. Set up once, sell many times. Perfect for digital agencies.", None, None),
        ("3. Skills Marketplace", "Build and sell premium skills. Specialized skills for real estate, healthcare, legal, finance. Charge per download or subscription.", None, None),
        ("4. SaaS Integration", "Connect Hermes to existing SaaS products. Zapier, Make, n8n, custom APIs. Sell automation workflows. $20-100/month per integration.", None, None),
        ("5. Consulting & Training", "Teach businesses how to use AI agents. Workshops, documentation, custom development. Charge $1,000-5,000 per engagement.", None, None),
        ("6. Course & Content", "You're already doing this. Sell access to training, templates, and community. Course + ongoing support = recurring revenue.", None, None),
        ("7. Freelance Automation", "One-off projects: custom agents, automated workflows, data pipelines, monitoring systems. $500-10,000 per project.", None, None),
        ("Module Summary", "Seven monetization paths. Start with one, expand to multiple. Your Hermes skills are worth $50-10,000 depending on the model.", None, None),
    ]),
    (10, "module-10-advanced.md", "Advanced Use Cases", [
        ("Advanced Use Cases", "Module 10: Real-world advanced use cases. Trading bots, content automation, code review, customer support, data pipelines.", None, None),
        ("Trading Bots", "Deploy trading agents that monitor markets, analyze trends, execute trades. Cron jobs for regular checks. Webhook alerts for opportunities.", None, None),
        ("Content Automation", "Auto-generate blog posts, social media content, newsletters. Research, write, edit, publish. Schedule with cron. Cross-post to all platforms.", None, None),
        ("Code Review", "Automated PR review agent. Reads diffs, checks for bugs, style issues, security vulnerabilities. Posts comments directly on GitHub.", None, None),
        ("Customer Support", "24/7 support agent on Telegram/Discord. Handles FAQs, triages issues, escalates complex cases. Learns from each interaction.", None, None),
        ("Data Pipelines", "ETL agents that extract, transform, load data on schedule. Monitor for anomalies. Generate reports. Alert on thresholds.", None, None),
        ("Course Complete", "Congratulations! You've completed the Hermes Agent Master Course. You have the skills, knowledge, and setup to build anything.", None, None),
    ]),
]

# ─── Helpers ───
def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = current + " " + word if current else word
        w = draw.textlength(test, font=font)
        if w <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines if lines else [text]

def draw_gradient_bg(draw, top_color=BG1, bottom_color=(10, 10, 25)):
    """Draw a subtle vertical gradient."""
    for y in range(H):
        ratio = y / H
        r = int(top_color[0] * (1-ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1-ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1-ratio) + bottom_color[2] * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def draw_grid(draw):
    """Draw subtle grid lines."""
    for x in range(0, W, 60):
        draw.line([(x, 0), (x, H)], fill=(108, 92, 231, 5), width=1)
    for y in range(0, H, 60):
        draw.line([(0, y), (W, y)], fill=(108, 92, 231, 5), width=1)

def draw_terminal_screen(draw, text, x, y, w=900, h=320, title="terminal"):
    """Draw a realistic terminal window with text output."""
    # Terminal border
    draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=TERM_BG, outline=(40, 40, 60), width=1)
    # Title bar dots
    dot_y = y + 18
    for dx in [x+20, x+36, x+52]:
        draw.ellipse([dx-5, dot_y-5, dx+5, dot_y+5], fill=(255, 95, 87) if dx==x+20 else ((255, 189, 46) if dx==x+36 else (39, 201, 63)))
    # Title
    mono10 = load_mono(14)
    draw.text((x+70, dot_y-7), title, fill=TERM_DIM, font=mono10)
    # Content
    mono14 = load_mono(16)
    lines = text.split('\n')
    line_h = 22
    text_y = y + 48
    for i, line in enumerate(lines):
        if line.startswith('$ '):
            draw.text((x+24, text_y), '$ ', fill=GREEN, font=mono14)
            draw.text((x+44, text_y), line[2:], fill=TERM_WHITE, font=mono14)
        elif '┌' in line or '└' in line or '│' in line:
            fill = ACCENT if '┌' in line or '└' in line else TERM_DIM
            draw.text((x+24, text_y), line, fill=fill, font=mono14)
        elif '✓' in line:
            draw.text((x+24, text_y), line, fill=GREEN, font=mono14)
        elif '⚠' in line:
            draw.text((x+24, text_y), line, fill=(255, 189, 46), font=mono14)
        else:
            draw.text((x+24, text_y), line, fill=TERM_WHITE, font=mono14)
        text_y += line_h

def render_slide(heading, body, code=None, demo_key=None, module_num=1):
    """Render a single slide as an image with optional terminal demo."""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    
    # Background
    draw_gradient_bg(draw)
    draw_grid(draw)
    
    # Accent line at top
    for x in range(0, W, 2):
        r = int(ACCENT[0] * (1 - x/W) + ACCENT2[0] * (x/W))
        g = int(ACCENT[1] * (1 - x/W) + ACCENT2[1] * (x/W))
        b = int(ACCENT[2] * (1 - x/W) + ACCENT2[2] * (x/W))
        draw.point((x, 0), fill=(r, g, b))
    draw.rectangle([0, 0, W, 3], fill=ACCENT)
    
    # Module badge
    badge_font = load_font(14, bold=True)
    draw.rounded_rectangle([40, 20, 220, 50], radius=8, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 30), outline=(ACCENT[0], ACCENT[1], ACCENT[2], 100))
    draw.text((50, 27), f"Module {module_num}", fill=ACCENT2, font=badge_font)
    
    # Heading
    h_font = load_font(42, bold=True)
    h_lines = wrap_text(heading, h_font, 1600, draw)
    text_y = 90
    for line in h_lines[:2]:
        draw.text((60, text_y), line, fill=WHITE, font=h_font)
        text_y += 52
    
    # Divider line
    draw.rectangle([60, text_y + 8, 400, text_y + 12], fill=ACCENT)
    text_y += 32
    
    # Body text
    b_font = load_font(24)
    body_lines = wrap_text(body, b_font, 1600, draw)
    for line in body_lines[:10]:
        draw.text((60, text_y), line, fill=GRAY, font=b_font)
        text_y += 34
    
    # Code block (if provided)
    if code:
        code_y = text_y + 20
        code_font = load_mono(18)
        c_lines = code.split('\n')
        c_h = len(c_lines) * 26 + 40
        cy = max(code_y, 550) if code_y > 500 else code_y
        draw.rounded_rectangle([60, cy, 1860, cy + c_h], radius=10, fill=(25, 25, 40), outline=(ACCENT[0], ACCENT[1], ACCENT[2], 60))
        cy2 = cy + 20
        for cl in c_lines[:18]:
            draw.text((80, cy2), cl, fill=TERM_WHITE, font=code_font)
            cy2 += 26
    
    # Terminal demo (if provided)
    if demo_key and demo_key in TERMINAL_DEMOS:
        demo_text = TERMINAL_DEMOS[demo_key]
        draw_terminal_screen(draw, demo_text, 510, max(text_y + 40, 480), w=900, h=min(len(demo_text.split('\n')) * 22 + 60, 400))
    
    return img

def generate_audio(text, output_path):
    """Generate TTS audio using Edge TTS."""
    import edge_tts
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        return True
    try:
        tts = edge_tts.Communicate(text=text, voice="en-US-JennyNeural", rate="+10%")
        subprocess.run(["edge-tts", "--voice", "en-US-JennyNeural", "--text", text[:5000], "--rate", "+10%", "--write-media", output_path],
                       capture_output=True, timeout=60)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except:
        return False

def generate_module_video(module_num, filename, title, slides):
    """Generate a complete module video from slides + audio."""
    module_dir = os.path.join(OUTPUT_DIR, f"module_{module_num:02d}")
    os.makedirs(module_dir, exist_ok=True)
    
    slide_images = []
    audio_files = []
    
    print(f"\n{'='*60}")
    print(f"Generating Module {module_num}: {title}")
    print(f"{'='*60}")
    
    total = len(slides)
    for i, (heading, body, code, demo_key) in enumerate(slides):
        print(f"  Slide {i+1}/{total}: {heading}")
        
        # Render slide image
        img = render_slide(heading, body, code, demo_key, module_num)
        img_path = os.path.join(module_dir, f"slide_{i:03d}.png")
        img.save(img_path)
        slide_images.append(img_path)
        
        # Generate narration audio
        audio_path = os.path.join(module_dir, f"audio_{i:03d}.mp3")
        narration = f"{heading}. {body}"
        if generate_audio(narration, audio_path):
            audio_files.append(audio_path)
        else:
            print(f"    ⚠ Audio generation failed, using silences")
            silent_path = os.path.join(module_dir, f"silent_{i:03d}.mp3")
            subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono", "-t", "8", silent_path],
                          capture_output=True)
            audio_files.append(silent_path)
    
    # Stitch everything into final video
    output_path = os.path.join(OUTPUT_DIR, f"module-{module_num:02d}-walkthrough.mp4")
    
    # Create concat file for slides
    concat_path = os.path.join(module_dir, "slides.txt")
    with open(concat_path, 'w') as f:
        for img_path, audio_path in zip(slide_images, audio_files):
            # Get audio duration
            probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
                                  capture_output=True, text=True, timeout=10)
            try:
                dur = float(probe.stdout.strip()) if probe.stdout.strip() else 8.0
            except:
                dur = 8.0
            f.write(f"file '{img_path}'\n")
            f.write(f"duration {dur}\n")
    
    # Generate video from slides + audio
    print(f"  Rendering final video...")
    
    # Build complex filter to overlay slides with audio
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_path,
    ]
    
    # Add all audio inputs
    for i, a in enumerate(audio_files):
        cmd.extend(["-i", a])
    
    # Build filter for audio concatenation
    audio_filter = "".join(f"[{i+1}:a]" for i in range(len(audio_files)))
    audio_filter += f"concat=n={len(audio_files)}:v=0:a=1[outa]"
    
    cmd.extend([
        "-filter_complex", audio_filter,
        "-map", "0:v",
        "-map", "[outa]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        output_path
    ])
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode == 0:
        size_mb = os.path.getsize(output_path) / (1024*1024)
        print(f"  ✅ Module {module_num} video: {output_path} ({size_mb:.1f} MB)")
    else:
        print(f"  ❌ Failed: {result.stderr[-300:]}")
    
    # Cleanup temp files
    shutil.rmtree(module_dir, ignore_errors=True)
    
    return output_path if result.returncode == 0 else None

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    start = time.time()
    results = []
    
    for module_num, filename, title, slides in MODULES:
        try:
            path = generate_module_video(module_num, filename, title, slides)
            results.append((module_num, title, path, "✅" if path else "❌"))
        except Exception as e:
            print(f"❌ Module {module_num} failed: {e}")
            results.append((module_num, title, None, "❌"))
    
    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"Generation complete in {elapsed/60:.1f} minutes")
    print(f"{'='*60}")
    for num, title, path, status in results:
        size = f"{os.path.getsize(path)/(1024*1024):.1f}MB" if path and os.path.exists(path) else "FAILED"
        print(f"  {status} Module {num}: {title} — {size}")

if __name__ == "__main__":
    main()
