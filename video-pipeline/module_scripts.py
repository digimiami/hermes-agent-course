#!/usr/bin/env python3
"""Define voiceover scripts, captions, and scene data for all 10 module videos."""

# Each module: (title, subtitle, script_text_bullets_for_tts, captions_segments, scenes_info)
# script_text: the full voiceover text (~2-3 min at 140 wpm ≈ 280-420 words)
# captions: list of (start_sec, end_sec, text)
# scenes: list of (bg_color_hex, title_overlay, duration_sec)

MODULES = {
    1: {
        "title": "What is Hermes Agent & Why It Matters",
        "subtitle": "Understand the architecture and why Hermes is different",
        "duration": 150,  # 2:30
        "script": (
            "Welcome to the Hermes Agent course. In this module, we'll explore what makes Hermes Agent "
            "fundamentally different from every AI tool you've used before.\n\n"
            "You've probably used ChatGPT, Claude, or Gemini. You ask a question, get an answer, "
            "and then copy-paste the result into a terminal or file. That's the chatbot pattern — "
            "the AI is disconnected from your actual workflow.\n\n"
            "Hermes breaks that completely. Instead of a web chat window, it lives in your terminal. "
            "Connected to your file system, your shell, your APIs, your messaging apps. "
            "It doesn't just tell you the command to run — it runs it. It doesn't just write your script — "
            "it executes it, tests it, and fixes it if it fails.\n\n"
            "Built by Nous Research, Hermes is open source under the MIT license. "
            "It supports over twenty LLM providers — OpenRouter, OpenAI, Anthropic, Google, local models — "
            "and you can switch between them with a single command. No lock-in, no vendor risk.\n\n"
            "But the real superpowers are persistent memory that remembers everything you teach it, "
            "a skills system that self-improves over time, over seventy built-in tools, "
            "multi-platform access through Telegram, Discord, and more, "
            "cron jobs for scheduled automation, and subagent delegation for parallel work.\n\n"
            "And the best part? It runs on a five-dollar VPS. Twenty-four seven. Always on. "
            "This isn't a chatbot. It's your autonomous AI agent. Let's get started."
        ),
        "captions": [
            (0, 8, "Welcome to Module 1"),
            (8, 16, "What makes Hermes Agent fundamentally different"),
            (16, 27, "ChatGPT gives you answers. Hermes gets things done."),
            (27, 38, "It lives in your terminal. Connected to everything."),
            (38, 48, "It runs commands, writes files, fixes errors automatically"),
            (48, 58, "Open source. MIT license. Built by Nous Research."),
            (58, 68, "20+ LLM providers. Zero lock-in."),
            (68, 80, "Persistent memory. Self-improving skills."),
            (80, 92, "70+ tools. Multi-platform. Cron jobs."),
            (92, 105, "Runs 24/7 on a $5 VPS"),
            (105, 120, "This isn't a chatbot. It's your autonomous agent."),
            (120, 150, "Let's get started with Module 1"),
        ],
        "scenes": [
            ("#05050b", "Hermes Agent", 8),
            ("#0a0a1a", "What Makes It Different", 30),
            ("#0f0f20", "Open Source & Provider Agnostic", 30),
            ("#0a0a18", "Key Superpowers", 35),
            ("#050510", "Self-Hosted & Always On", 25),
            ("#080818", "Let's Begin", 22),
        ],
    },
    2: {
        "title": "Installation & First Run",
        "subtitle": "One command. First conversation in under 5 minutes",
        "duration": 160,
        "script": (
            "In this module, you'll install Hermes Agent on your machine and have your first "
            "conversation in under five minutes.\n\n"
            "The installation is a single command — curl the install script and pipe it to bash. "
            "That's it. The installer handles Python, Node.js, ripgrep, and FFmpeg automatically. "
            "If you prefer Docker, there's a container image you can run with one docker command.\n\n"
            "After installation, just source your bashrc and type hermes. "
            "The setup wizard walks you through choosing a provider and getting your first API key. "
            "OpenRouter is the best starting point — one key gives you access to over two hundred models.\n\n"
            "The very first thing you should do is ask Hermes something related to your work. "
            "Let it read files, run commands, and explore your environment. "
            "This immediate utility is what hooks people — within the first thirty seconds, "
            "you'll realize this isn't a chatbot, it's a coworker.\n\n"
            "If you run into any issues, hermes doctor diagnoses everything automatically. "
            "Node version problems, missing dependencies, broken config — it finds and fixes them. "
            "And if you get stuck, the community Discord and GitHub discussions are incredibly active. "
            "By the end of this module, you'll have Hermes running and ready to work."
        ),
        "captions": [
            (0, 8, "Install Hermes Agent in under 5 minutes"),
            (8, 18, "One command to install: curl | bash"),
            (18, 28, "Docker also available: docker run"),
            (28, 38, "Setup wizard guides you step by step"),
            (38, 48, "Start with OpenRouter - one key, 200+ models"),
            (48, 60, "Your first conversation - ask it anything"),
            (60, 72, "Hermes reads files, runs commands, explores"),
            (72, 85, "Stuck? hermes doctor diagnoses everything"),
            (85, 100, "Active community on Discord and GitHub"),
            (100, 130, "Hermes running and ready to work"),
            (130, 160, "Module 2 complete - you're ready for configuration"),
        ],
        "scenes": [
            ("#05050b", "Installation & First Run", 8),
            ("#0a0a1a", "One Command Install", 25),
            ("#0f0f20", "Setup Wizard", 20),
            ("#0a0a18", "Your First Conversation", 30),
            ("#080818", "Troubleshooting with hermes doctor", 25),
            ("#050510", "Ready for Module 3: Configuration", 52),
        ],
    },
    3: {
        "title": "Configuration Deep Dive",
        "subtitle": "Master every configuration option in Hermes Agent",
        "duration": 155,
        "script": (
            "Welcome to Module 3. Configuration is where Hermes really opens up. "
            "There are two main files under dot-hermes: config.yaml for behavioral settings, "
            "and dot-env for API keys and secrets. This split means you can version control your config "
            "without risking credential leaks.\n\n"
            "Let's talk about the config hierarchy. Hermes loads defaults first, then your user config, "
            "then any project-level config, and finally environment variables which override everything. "
            "This layered approach means you can have different setups for different projects.\n\n"
            "The most important settings are your model provider and profile. "
            "You can set a primary provider, a fallback chain, and even routing rules "
            "that send different task types to different models. Complex reasoning goes to Claude Opus, "
            "quick lookups go to a cheaper model, code generation goes to a code-specialized model.\n\n"
            "Profiles are another game-changer. You can define multiple profiles for different contexts — "
            "a coding profile with git tools enabled, a DevOps profile with terminal and web access, "
            "a research profile with browser and search tools. Switch between them with one command.\n\n"
            "Tool security is also configured here. You can enable or disable specific toolsets, "
            "set approval gates for dangerous operations, and configure the browser sandbox. "
            "By the end of this module, you'll have a fully tuned configuration."
        ),
        "captions": [
            (0, 8, "Module 3: Configuration Deep Dive"),
            (8, 18, "Two files: config.yaml and .env"),
            (18, 28, "Version control safe - no credential leaks"),
            (28, 40, "Config hierarchy: defaults → user → project → env"),
            (40, 52, "Model providers and fallback chains"),
            (52, 65, "Route tasks to different models"),
            (65, 78, "Profiles for different contexts"),
            (78, 90, "Coding, DevOps, Research profiles"),
            (90, 105, "Tool security and approval gates"),
            (105, 130, "Fully tuned configuration ready"),
            (130, 155, "Module 3 complete"),
        ],
        "scenes": [
            ("#05050b", "Configuration Deep Dive", 8),
            ("#0a0a1a", "Config Files & Hierarchy", 25),
            ("#0f0f20", "Model Providers & Fallbacks", 25),
            ("#0a0a18", "Profiles & Routing", 25),
            ("#080818", "Tool Security", 25),
            ("#050510", "Ready for Module 4", 47),
        ],
    },
    4: {
        "title": "Daily Usage & Power Features",
        "subtitle": "Slash commands, delegation, cron jobs, and more",
        "duration": 160,
        "script": (
            "Module 4 is where you graduate from beginner to power user. "
            "Hermes has two main modes: interactive chat with a full terminal UI, "
            "and single query mode for one-off commands. You'll use interactive mode most of the time.\n\n"
            "The slash commands are your shortcuts. New starts a fresh session. "
            "Model switches providers mid-conversation. Save persists important context. "
            "Background launches tasks that run while you keep working. "
            "There are over twenty slash commands that cover everything you need.\n\n"
            "Subagent delegation is perhaps the most powerful feature. "
            "You can spawn up to three subagents to work in parallel on independent tasks. "
            "Each gets its own terminal, tools, and context. You can even spawn orchestrator agents "
            "that delegate further. This turns Hermes from a single assistant into a whole team.\n\n"
            "Cron jobs let you schedule recurring tasks. A daily market briefing at eight AM, "
            "a weekly codebase health check, a monthly report generator. "
            "Set it once and Hermes handles it forever, delivering results to your Telegram or Discord.\n\n"
            "Webhooks add event-driven automation. A GitHub push triggers a deployment check. "
            "A Stripe payment triggers a thank-you email. Hermes can be the brain behind any webhook. "
            "By the end of this module, you're a daily Hermes power user."
        ),
        "captions": [
            (0, 8, "Module 4: Daily Usage & Power Features"),
            (8, 18, "Interactive chat vs single query mode"),
            (18, 28, "20+ slash commands"),
            (28, 40, "/new, /model, /save, /background"),
            (40, 52, "Subagent delegation"),
            (52, 65, "Parallel task execution"),
            (65, 75, "Cron jobs for scheduled automation"),
            (75, 88, "Event-driven webhooks"),
            (88, 100, "GitHub, Stripe, custom integrations"),
            (100, 130, "You're now a Hermes power user"),
            (130, 160, "Ready for Module 5: Skills System"),
        ],
        "scenes": [
            ("#05050b", "Daily Usage & Power Features", 8),
            ("#0a0a1a", "Interactive Mode & Slash Commands", 25),
            ("#0f0f20", "Subagent Delegation", 25),
            ("#0a0a18", "Cron Jobs & Scheduling", 25),
            ("#080818", "Webhook Integration", 25),
            ("#050510", "Ready for Module 5", 52),
        ],
    },
    5: {
        "title": "Skills System - The Killer Feature",
        "subtitle": "Create, manage, and publish reusable skills",
        "duration": 160,
        "script": (
            "Module 5 covers the single most important feature of Hermes Agent: the Skills System. "
            "Most AI assistants are amnesiacs. You teach them something one day, and the next day "
            "they've forgotten it entirely. Hermes breaks this cycle with skills.\n\n"
            "A skill is a markdown file with structured frontmatter and a body. "
            "It tells Hermes how to handle a specific type of task. The frontmatter defines the skill's "
            "name, description, triggers, and dependencies. The body contains the instructions, examples, "
            "and code templates that the agent follows when the skill is loaded.\n\n"
            "When you load a skill, Hermes gets permanent knowledge about that domain. "
            "Create a skill for your deployment workflow once, and Hermes remembers it forever. "
            "No more repeating yourself. Every correction you make becomes a permanent improvement.\n\n"
            "The skill library grows organically. Start with the built-in skills, then create your own. "
            "There's a Skill Hub ecosystem where you can browse, install, and publish skills. "
            "Community skills cover everything from trading bots to code review to content creation.\n\n"
            "The compound effect is remarkable. After fifty-plus skills, Hermes knows your entire stack, "
            "your preferences, your conventions, your workflow. It becomes a true extension of you. "
            "This is the killer feature that makes Hermes irreplaceable."
        ),
        "captions": [
            (0, 8, "Module 5: Skills System"),
            (8, 18, "The killer feature of Hermes Agent"),
            (18, 28, "Most AI assistants are amnesiacs"),
            (28, 40, "Skills = permanent, reusable knowledge"),
            (40, 52, "Markdown files with structured frontmatter"),
            (52, 65, "Create once, use forever"),
            (65, 78, "Skill Hub ecosystem"),
            (78, 90, "Browse, install, publish skills"),
            (90, 105, "50+ skills = agent that knows your stack"),
            (105, 130, "The compound learning effect"),
            (130, 160, "Module 5 complete"),
        ],
        "scenes": [
            ("#05050b", "Skills System", 8),
            ("#0a0a1a", "The Problem with Amnesiac AI", 25),
            ("#0f0f20", "How Skills Work", 25),
            ("#0a0a18", "Skill Hub Ecosystem", 25),
            ("#080818", "The Compound Effect", 25),
            ("#050510", "Ready for Module 6: Training", 52),
        ],
    },
    6: {
        "title": "Training Your Agent",
        "subtitle": "Memory, corrections, and teaching workflows",
        "duration": 150,
        "script": (
            "Module 6 is about training your agent to know you. Skills give Hermes capabilities, "
            "but training gives it your preferences, your conventions, your style.\n\n"
            "The memory system has two targets: memory for your personal notes and environment facts, "
            "and user profile for who you are and how you communicate. "
            "When you correct Hermes, it saves that correction as a durable fact. "
            "Next time, it doesn't make the same mistake.\n\n"
            "The corrections pipeline is key. Every time you tell Hermes don't do that or remember this, "
            "that feedback is stored in memory and applied in future sessions. "
            "Over time, the agent learns your preferred approach to everything.\n\n"
            "Session search lets Hermes recall past conversations. "
            "Ask what were we doing on the trading bot last week, and it retrieves the relevant session, "
            "including the decisions made and the final outcome. No context lost.\n\n"
            "After fifty-plus sessions of training, Hermes doesn't just answer questions — "
            "it anticipates your needs. It knows your database schema, your deployment process, "
            "your code style, your tools, your team. "
            "That's the compound effect, and it's what makes Hermes truly yours."
        ),
        "captions": [
            (0, 8, "Module 6: Training Your Agent"),
            (8, 18, "Skills = capabilities. Training = preferences."),
            (18, 28, "Memory system: facts and profile"),
            (28, 40, "Corrections pipeline"),
            (40, 52, "Every correction is a permanent improvement"),
            (52, 65, "Session search: find any past conversation"),
            (65, 78, "The compound effect of training"),
            (78, 92, "Agent that knows your entire workflow"),
            (92, 120, "Anticipates your needs"),
            (120, 150, "Module 6 complete"),
        ],
        "scenes": [
            ("#05050b", "Training Your Agent", 8),
            ("#0a0a1a", "Memory System", 25),
            ("#0f0f20", "Corrections Pipeline", 25),
            ("#0a0a18", "Session Search", 25),
            ("#080818", "The Compound Effect", 25),
            ("#050510", "Ready for Module 7: Gateway", 42),
        ],
    },
    7: {
        "title": "Multi-Platform Gateway",
        "subtitle": "Run your agent on Telegram, Discord, and more",
        "duration": 150,
        "script": (
            "Module 7 covers the Gateway — a background daemon that connects Hermes to your messaging apps. "
            "Telegram, Discord, Slack, WhatsApp, Signal, and over fifteen more platforms, "
            "all from one agent instance.\n\n"
            "The key idea is simple: same AI agent, different chat interfaces. "
            "Your tools, memory, skills, and cron jobs work identically across every platform. "
            "Message Hermes from Telegram on your phone while commuting, "
            "then continue the same conversation from Discord on your desktop.\n\n"
            "Setup is straightforward. Run hermes gateway setup for the interactive wizard, "
            "or configure it manually in your dot-env file. "
            "Then install it as a systemd service so it runs automatically on boot. "
            "Hermes gateway install does this in one command.\n\n"
            "Security is built in. You can set allowlists for who can message your agent, "
            "require pairing for DMs, create admin and user tiers, "
            "and require approval for dangerous operations like file deletion or code execution.\n\n"
            "Cron jobs can deliver to any platform. Your daily briefing goes to Telegram, "
            "your code review reports go to Discord, your trading alerts go to Signal. "
            "One agent, everywhere you need it."
        ),
        "captions": [
            (0, 8, "Module 7: Multi-Platform Gateway"),
            (8, 18, "One agent, every platform"),
            (18, 28, "Telegram, Discord, Slack, WhatsApp, Signal"),
            (28, 38, "Same agent, different interfaces"),
            (38, 50, "Continue conversations across platforms"),
            (50, 62, "Setup: hermes gateway setup"),
            (62, 75, "Install as systemd service"),
            (75, 88, "Security: allowlists, pairing, tiers"),
            (88, 100, "Cron jobs deliver anywhere"),
            (100, 130, "One agent everywhere you need it"),
            (130, 150, "Module 7 complete"),
        ],
        "scenes": [
            ("#05050b", "Multi-Platform Gateway", 8),
            ("#0a0a1a", "One Agent, Every Platform", 25),
            ("#0f0f20", "Setup & Configuration", 25),
            ("#0a0a18", "Security & Access Control", 25),
            ("#080818", "Cross-Platform Cron Delivery", 25),
            ("#050510", "Ready for Module 8: VPS", 42),
        ],
    },
    8: {
        "title": "VPS Deployment",
        "subtitle": "Run Hermes 24/7 on a $5 VPS",
        "duration": 150,
        "script": (
            "Module 8 is where you take your Hermes agent to production. "
            "Running on your laptop is fine for development, but for a 24-7 setup — "
            "a bot your team uses, cron jobs that fire at three AM, "
            "an agent that monitors your infrastructure — you need a VPS.\n\n"
            "A basic one-CPU, one-gigabyte RAM server costs just four to six dollars per month. "
            "Less than a streaming subscription. And it's plenty for Hermes.\n\n"
            "The setup takes about thirty minutes. SSH into your VPS, create a user, "
            "secure SSH with key-based authentication, install Hermes, "
            "configure the gateway, set up systemd to auto-start on boot, and done.\n\n"
            "The module covers security hardening — fail2ban, firewall rules, regular updates. "
            "And monitoring: how to check your agent's health, set up alerts, "
            "and handle crashes with automatic restart via systemd.\n\n"
            "Once deployed, your agent is always on. Cron jobs fire on schedule. "
            "Your gateway never goes offline. Your skills and memory persist. "
            "And you can access your agent from anywhere, on any device, at any time. "
            "Production Hermes. Twenty-four seven."
        ),
        "captions": [
            (0, 8, "Module 8: VPS Deployment"),
            (8, 18, "From laptop to production"),
            (18, 28, "$5/month VPS is all you need"),
            (28, 40, "30-minute setup guide"),
            (40, 52, "Security hardening"),
            (52, 65, "Systemd auto-start on boot"),
            (65, 78, "Monitoring & health checks"),
            (78, 92, "Never offline, always running"),
            (92, 120, "Access your agent from anywhere"),
            (120, 150, "Module 8 complete"),
        ],
        "scenes": [
            ("#05050b", "VPS Deployment", 8),
            ("#0a0a1a", "Why a VPS?", 25),
            ("#0f0f20", "30-Minute Setup", 25),
            ("#0a0a18", "Security Hardening", 25),
            ("#080818", "Monitoring & Uptime", 25),
            ("#050510", "Ready for Module 9: Monetization", 42),
        ],
    },
    9: {
        "title": "Monetization Strategies",
        "subtitle": "7 ways to make money with Hermes Agent",
        "duration": 160,
        "script": (
            "Module 9 is about turning your Hermes skills into income. "
            "Because Hermes is open source under MIT and runs on cheap infrastructure, "
            "you can build revenue streams that would be impossible with closed platforms.\n\n"
            "Strategy one: Agent as a Service. Set up Hermes for clients on their own VPS. "
            "Charge twenty to fifty dollars per month per user. Low overhead, recurring revenue.\n\n"
            "Strategy two: Local business automation. Restaurants, clinics, law firms — "
            "they all need appointment scheduling, customer support, inventory management. "
            "Hermes handles all of it. Five hundred to five thousand per setup.\n\n"
            "Strategy three: Custom skill development. Companies need specialized agent skills. "
            "Charge one hundred to five hundred per skill. Each skills takes one to two weeks to build.\n\n"
            "Strategy four: Affiliate marketing. Promote Hermes, VPS providers, and AI tools. "
            "Passive income, fifty to five hundred per month.\n\n"
            "Strategy five: Sell this course. You already have the content. "
            "Package it, market it, scale it.\n\n"
            "Strategy six: White-label Hermes. Rebrand it for agencies. "
            "Two to five thousand setup plus monthly recurring.\n\n"
            "Strategy seven: Build a SaaS product on top of Hermes. "
            "The most ambitious but highest reward. The MIT license gives you full freedom."
        ),
        "captions": [
            (0, 8, "Module 9: Monetization Strategies"),
            (8, 18, "7 ways to make money with Hermes"),
            (18, 28, "Agent as a Service: $20-50/mo per user"),
            (28, 40, "Local business automation: $500-5000"),
            (40, 52, "Custom skill development: $100-500"),
            (52, 65, "Affiliate marketing: passive income"),
            (65, 78, "Sell this course"),
            (78, 90, "White-label Hermes: $2K-5K setup"),
            (90, 105, "SaaS product: highest reward"),
            (105, 130, "MIT license = full freedom"),
            (130, 160, "Module 9 complete"),
        ],
        "scenes": [
            ("#05050b", "Monetization Strategies", 8),
            ("#0a0a1a", "Agent as a Service", 25),
            ("#0f0f20", "Local Business Automation", 25),
            ("#0a0a18", "Skills & White-Label", 25),
            ("#080818", "SaaS & Affiliate", 25),
            ("#050510", "Ready for Module 10: Advanced", 52),
        ],
    },
    10: {
        "title": "Advanced Use Cases",
        "subtitle": "Trading bots, content automation, code review, and pipelines",
        "duration": 160,
        "script": (
            "Module 10 is where everything comes together. We'll cover advanced production use cases "
            "that show the full power of Hermes Agent.\n\n"
            "First, trading bots. Hermes can monitor crypto and stock markets, "
            "analyze trends with technical indicators, and execute trades through exchange APIs. "
            "Set up cron jobs for hourly market scans, configure alerts via the gateway, "
            "and let your agent trade around the clock.\n\n"
            "Content automation is another powerhouse use case. "
            "Hermes can generate scripts, create voiceovers with TTS, "
            "run SadTalker for talking-head animations, composite videos with FFmpeg, "
            "and upload the final result to YouTube. An entire content pipeline from a single command.\n\n"
            "Code review bots integrate with GitHub webhooks. "
            "Every pull request gets automatically reviewed — security scan, code quality check, "
            "style consistency. Comments are posted directly on the PR.\n\n"
            "Customer support agents run on the gateway. "
            "Your Telegram or Discord bot answers common questions, creates tickets, "
            "escalates complex issues. Twenty-four seven support without hiring.\n\n"
            "And multi-agent systems with subagent delegation let you orchestrate complex workflows. "
            "One agent researches, another builds, a third tests, a fourth deploys. "
            "Your entire development pipeline, automated. Welcome to the future."
        ),
        "captions": [
            (0, 8, "Module 10: Advanced Use Cases"),
            (8, 18, "Production-ready Hermes systems"),
            (18, 28, "Trading bots: 24/7 market automation"),
            (28, 40, "Content automation: script to publish"),
            (40, 52, "Code review bots with webhooks"),
            (52, 65, "Customer support agents"),
            (65, 78, "Multi-agent orchestration"),
            (78, 90, "Full development pipeline automation"),
            (90, 105, "Research, build, test, deploy"),
            (105, 130, "Welcome to the future of AI agents"),
            (130, 160, "Course complete! Here is your certificate"),
        ],
        "scenes": [
            ("#05050b", "Advanced Use Cases", 8),
            ("#0a0a1a", "Trading Bots", 25),
            ("#0f0f20", "Content Automation", 25),
            ("#0a0a18", "Code Review & Support", 25),
            ("#080818", "Multi-Agent Systems", 25),
            ("#050510", "Course Complete!", 52),
        ],
    },
}
