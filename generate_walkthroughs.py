#!/usr/bin/env python3
"""
Generate 2-3 minute module walkthrough videos with detailed voiceover + animated slides.
Each module gets 15+ detailed slides with comprehensive narration.
"""
import os
import subprocess
import tempfile
import textwrap
import time
import json

OUTPUT_DIR = "/root/hermes-course/course/videos"
W, H = 1920, 1080
FPS = 25

def t(s, bold=False):
    """Tag text for rendering"""
    return f"<t>{s}</t>"

# Each module: (num, filename, title, [(subtitle, body_text, code_example_or_none), ...])
# body_text is the narration text that will be read aloud for this slide
MODULE_DATA = [
    (1, "module-01-intro.md", "What is Hermes Agent & Why It Matters", [
        ("Welcome", "Welcome to Module 1 of the Hermes Agent Master Course. In this module, we will explore what Hermes Agent actually is, how it differs from regular chatbots, and why it matters for your workflow.", None),
        ("The Problem with Chatbots", "Chatbots like ChatGPT and Claude are great for answering questions, but they stop there. They live in a browser tab, disconnected from your actual workflow. You copy-paste their output into your terminal, your editor, or your chat app. Hermes Agent breaks this pattern completely.", None),
        ("What Makes Hermes Different", "Hermes Agent lives inside your terminal, connected to your file system, shell, browser, APIs, and messaging apps. It doesn't just tell you what command to run, it runs it for you. It doesn't just write code, it executes it, tests it, and fixes it when it fails.", None),
        ("Core Architecture", "Hermes is an open-source project built by Nous Research, the same team behind the Hermes language models. It runs on your own infrastructure, connects to over 20 LLM providers, and features persistent memory, a skills system, and a powerful tool-calling framework.", None),
        ("Provider Agnosticism", "One of Hermes' most powerful features is that it works with any LLM provider. OpenRouter gives you access to 200+ models from one key. You can use Anthropic Claude, OpenAI GPT, DeepSeek, Google Gemini, Grok from xAI, or even run local models via Ollama. Switch with a single command.", None),
        ("The Skills System", "Skills are Hermes' killer feature. They are markdown files that teach your agent how to perform specific tasks. Think of them as procedural memory, your agent's muscle memory. Skills load on demand, saving tokens, and they improve over time based on your corrections.", None),
        ("Persistent Memory", "Unlike chatbots that forget everything between sessions, Hermes has two memory layers: session memory for the current conversation and persistent memory that survives restarts. When you teach your agent something, it remembers next time.", None),
        ("Tool Calling Explained", "Hermes can use over 70 built-in tools. It can run terminal commands, read and write files, search the web, browse websites, interact with git repositories, send emails, control smart home devices, and even spawn subagents to work in parallel.", None),
        ("Multi-Platform Gateway", "Your agent isn't locked to the terminal. The gateway system lets you connect Hermes to Telegram, Discord, WhatsApp, Slack, Signal, Matrix, and more. The same agent works everywhere. Start a task on Telegram, check on it from Discord.", None),
        ("Autonomous Operation", "Hermes can run autonomously on a schedule. Set up cron jobs, webhooks, and automated workflows. Your agent monitors systems, sends reports, processes data, and takes action even when you are not at your computer.", None),
        ("Self-Hosted & Private", "Your data stays on your machine. Hermes is MIT licensed, free forever, with no subscriptions. Run it on your laptop or deploy it on a $5 VPS. No data leaves your infrastructure unless you choose to connect external services.", None),
        ("Subagent Delegation", "Spawn child agents to work on tasks in parallel. One agent researches a topic, another writes code, a third tests it. Each subagent gets its own conversation context and toolset. This unlocks complex multi-step workflows.", None),
        ("The Learning Loop", "Every interaction with Hermes is a training opportunity. When you correct a mistake, the agent remembers and does better next time. Over weeks and months, your agent becomes uniquely tuned to your workflows, preferences, and coding style.", None),
        ("What You'll Build", "By the end of this course, you will have a fully autonomous AI agent running 24-7 on a cloud VPS. It will be connected to Telegram, have custom skills for your specific use cases, and be ready to monetize through various strategies we cover later.", None),
        ("Module Summary", "To summarize: Hermes Agent is an open-source, self-hosted AI that uses tools, remembers everything, improves over time, works on any platform, connects to any LLM provider, runs 24-7, and costs nothing but your server. Let's move on to Module 2 where we install it.", None),
    ]),
    (2, "module-02-installation.md", "Installation & First Run", [
        ("Welcome", "Welcome to Module 2 of the Hermes Agent Master Course. In this module, we will install Hermes Agent on your machine and have your first conversation with it. We will cover the one-line installer, Docker setup, and the setup wizard.", None),
        ("Prerequisites", "Before installing, make sure you have Git installed. On Ubuntu, run sudo apt install git. On macOS, use xcode-select --install or brew install git. The installer handles everything else: Python, Node.js, ripgrep, and ffmpeg are all provisioned automatically.", None),
        ("Getting an API Key", "You need an API key from an LLM provider. For beginners, OpenRouter is the best starting point. Go to openrouter.ai forward slash keys, sign up, and create a key. The free tier gives you enough credits to explore for weeks. Top up with 5 dollars to access everything.", None),
        ("One-Line Install", "Open your terminal and run curl -fsSL followed by the Hermes install script URL, piped to bash. That is it. The installer detects your platform, installs uv, creates a virtual environment, installs dependencies, sets up Node.js and Playwright browsers, and installs system tools.", None),
        ("What the Installer Does", "The install script clones the Hermes repository, creates a Python virtual environment, installs all Python dependencies, installs Node.js for browser automation, installs Playwright browsers for web automation, installs ripgrep for fast file search, and symlinks the hermes command.", None),
        ("Install Layout", "After installation, the Hermes code lives in dot hermes slash hermes-agent. The virtual environment is at dot hermes slash hermes-agent slash venv. The hermes command is symlinked to dot local bin slash hermes. Your shell config is updated to include this in your PATH.", None),
        ("Running the Setup Wizard", "After installing, run source dot bashrc then just type hermes. The first-run wizard will guide you through choosing a model provider, entering your API key, setting your agent name, and configuring basic preferences. The whole process takes under 2 minutes.", None),
        ("Choosing a Provider", "The setup wizard shows a list of supported providers. Select OpenRouter for maximum flexibility with 200 plus models. Or choose a specific provider like Anthropic, OpenAI, or Google Gemini. You can switch providers anytime with the hermes model command.", None),
        ("Docker Installation", "Prefer containers? Hermes has an official Docker image. Run docker run minus it ghcr.io forward slash nousresearch forward slash hermes-agent. The Docker image includes everything pre-configured. Mount a volume for persistent data like dot hermes.", None),
        ("First Conversation", "Once the wizard is complete, you will see the Hermes prompt. Try asking: run ls minus la in my home directory. Or: what is the weather in London? Or: create a new file called test.txt with hello world. Watch Hermes use its tools to fulfill your request in real time.", None),
        ("Understanding the Interface", "The Hermes interface is a terminal prompt with tool execution visible. You see every command Hermes runs, every file it reads or writes, every web search it performs. You can approve or deny tool calls. Use slash commands like slash help, slash memory, slash skills.", None),
        ("Slash Commands Overview", "Slash commands are quick ways to control your agent. Slash help shows all available commands. Slash memory lets you inspect what your agent remembers. Slash skills lists loaded skills. Slash config opens configuration. Slash model switches providers mid-conversation.", None),
        ("Configuration Files", "Hermes configuration lives in dot hermes slash config dot yaml. This file controls model settings, provider configurations, toolsets, security settings, and platform connections. You can edit it directly or use the hermes config command.", None),
        ("Troubleshooting", "If something goes wrong, run hermes doctor. This diagnostic command checks your installation, verifies API keys, tests provider connections, and suggests fixes. It is the first thing to try when something is not working.", None),
        ("Module Summary", "You now have Hermes installed and running. You have had your first conversation and understand the interface. In Module 3, we will dive deep into configuration, model providers, toolsets, and security settings to customize your agent.", None),
    ]),
    (3, "module-03-configuration.md", "Configuration Deep Dive", [
        ("Welcome", "Welcome to Module 3 of the Hermes Agent Master Course. In this module, we will explore configuration in depth, covering model providers, API key management, toolsets, security, profiles, and memory settings.", None),
        ("The Config File", "The main configuration file is dot hermes slash config dot yaml. It uses YAML format and controls every aspect of your agent's behavior. You can edit it with any text editor or use the hermes config command to modify specific settings.", None),
        ("Model Configuration", "The model section defines your default provider and model. Set default to your preferred model name, provider to the service name, and base URL if using a custom endpoint. You can override these per conversation with the slash model command.", None),
        ("Provider Configuration", "Under providers, you configure API keys and settings for each service. Hermes supports OpenRouter, OpenAI, Anthropic, DeepSeek, Google Gemini, xAI Grok, Hugging Face, and local endpoints via Ollama or LM Studio. Each has its own configuration block.", None),
        ("API Key Security", "Store API keys in a dot env file in your home directory. Hermes reads this file automatically. The keys are never written to the config file or logged. This prevents accidental credential exposure in git commits or terminal output.", None),
        ("Toolsets Configuration", "Toolsets control which capabilities your agent has. Enable specific toolsets for your use case: terminal for shell access, file for file operations, web for internet search, browser for web automation, vision for image analysis. Disable tools you do not need for security.", None),
        ("Profiles System", "Profiles let you create multiple configurations for different contexts. A development profile with coding tools, a trading profile with market data access, a personal assistant profile connected to your messaging apps. Switch between them with hermes profile select.", None),
        ("Memory Configuration", "Memory is configured under the memory section. Set memory underscore enabled to true. Configure user profile to store information about yourself. Set character limits and flush intervals. Hermes uses compression to manage context window efficiently.", None),
        ("Agent Settings", "The agent section controls behavior: max turns limits conversation length, gateway timeout controls how long the agent waits for responses, reasoning effort adjusts thinking depth, and temperature affects creativity. Tune these for your use case.", None),
        ("Security Settings", "Security is paramount. The security section includes command allowlists, approval modes, website blocklists, and secret redaction. Use approvals to require confirmation for dangerous operations like deleting files or modifying configuration.", None),
        ("Gateway Configuration", "The gateway section configures platform connections. Set up Telegram with your bot token, Discord with your bot credentials, WhatsApp with your business account. Each platform has its own configuration block with webhooks, rate limits, and permissions.", None),
        ("Cron Jobs", "Schedule recurring tasks with cron jobs. Each job has a schedule expression, a prompt for the agent, and delivery settings. Jobs run autonomously in the background. Use cases include daily reports, health checks, market monitoring, and content generation.", None),
        ("Webhook Setup", "Webhooks let external services trigger your agent. Configure webhook endpoints and signatures. Integrate with GitHub for pull request reviews, Stripe for payment notifications, Zapier for no-code automations, or any service that sends HTTP requests.", None),
        ("Delegation Settings", "The delegation section controls subagent behavior. Set max concurrent children for parallel task execution, max spawn depth for nested delegation, orchestrator mode for complex workflows, and timeout settings for long-running tasks.", None),
        ("Module Summary", "Configuration mastery is key to getting the most from Hermes. You now understand how to configure providers, manage API keys securely, set up profiles, tune agent behavior, and configure the gateway, cron, and webhook systems.", None),
    ]),
    (4, "module-04-usage.md", "Daily Usage & Power Features", [
        ("Welcome", "Welcome to Module 4 of the Hermes Agent Master Course. In this module, we will cover daily usage patterns, power features like subagent delegation, cron jobs, webhooks, sessions, and checkpoints. These are the tools that make Hermes truly powerful.", None),
        ("Everyday Conversation", "Use Hermes for daily tasks: summarize documents, draft emails, research topics, write code snippets, debug issues, manage files, and automate repetitive commands. Treat it like a supercharged terminal assistant that remembers everything.", None),
        ("File Operations", "Hermes can read, write, edit, and search files. Use it to refactor code, find bugs across your project, batch rename files, merge documents, and manage your entire file system. The patch tool does targeted find-and-replace edits with fuzzy matching.", None),
        ("Web Research", "Ask Hermes to research topics. It searches the web, extracts content from pages, and synthesizes findings. Use it for competitor analysis, market research, fact checking, and staying current with industry news.", None),
        ("Code Assistance", "Hermes excels at coding tasks. It can write functions, debug errors, review pull requests, generate tests, refactor legacy code, and document your projects. It understands your codebase context and suggests improvements.", None),
        ("Subagent Delegation", "The delegate task tool spawns child agents. Each subagent gets its own conversation and tools. Use them for parallel work: one agent researches deployment options while another writes the Dockerfile and a third tests the configuration.", None),
        ("Cron Jobs in Depth", "Cron jobs run on a schedule. Create them with the cronjob tool. Specify a schedule expression, the task prompt, and delivery destination. Jobs can be one-shot or recurring. Use for daily backups, hourly market checks, or weekly reports.", None),
        ("Sessions & Checkpoints", "Sessions save your conversation state. Resume later where you left off. Checkpoints create snapshots that you can restore if something goes wrong. Use these for long-running research projects or complex multi-step tasks.", None),
        ("Memory Management", "Use the memory tool to save important facts. Memory persists across sessions and is injected into every conversation. Save user preferences, environment details, project conventions, and API quirks. Keep it compact and focused on durable facts.", None),
        ("Skills System in Practice", "Load skills with skill view. The skills list command shows all available skills organized by category. Skills are loaded on demand, saving tokens. When you find a workflow you repeat, save it as a skill for future use.", None),
        ("Terminal Power User", "The terminal tool runs shell commands. Use background mode for long-running processes with notification on complete. Use PTY mode for interactive tools. Watch patterns for server startup signals. Process management for lifecycle control.", None),
        ("Browser Automation", "Hermes can navigate websites, fill forms, click buttons, take screenshots, and extract data. Use it for web scraping, form submissions, CAPTCHA handling, visual QA testing, and monitoring dynamic content.", None),
        ("File Search & Management", "Use search files for lightning-fast content and filename search. Write file creates new files with automatic parent directories. Patch does fuzzy find-and-replace with syntax validation. Read file shows paginated content with line numbers.", None),
        ("Integration Patterns", "Combine features for powerful workflows. Example: a cron job that researches competitors daily, saves findings to a file, then sends a summary to Telegram. Or a webhook that triggers code review on every GitHub pull request.", None),
        ("Module Summary", "You now know the daily power features of Hermes. Subagent delegation, cron jobs, memory management, and integration patterns unlock your agent's full potential. Practice combining these features for your specific use cases.", None),
    ]),
    (5, "module-05-skills.md", "Skills System - The Killer Feature", [
        ("Welcome", "Welcome to Module 5 of the Hermes Agent Master Course. In this module, we dive deep into the Skills System, the single most powerful feature of Hermes Agent. Skills are reusable procedures that teach your agent how to perform specific tasks.", None),
        ("What Are Skills?", "Skills are markdown files with YAML frontmatter that contain instructions, workflows, and templates for your agent. Think of them as your agent's procedural memory. When Hermes encounters a task matching a skill, it loads that skill and follows its instructions.", None),
        ("Why Skills Matter", "Without skills, every conversation starts from scratch. With skills, your agent has pre-built knowledge for specific tasks. Skills encode best practices, workflows, and domain knowledge. They make your agent more capable, consistent, and efficient with every skill you add.", None),
        ("Built-in Skills Overview", "Hermes ships with over 48 built-in skills covering software development, DevOps, data science, research, creative work, system administration, and more. Skills are organized by category and loaded on demand. Each skill has a specific trigger scenario.", None),
        ("Creating Your First Skill", "Use the skill manage tool with action create. Provide a name, content with YAML frontmatter and markdown body, and an optional category. A good skill includes: trigger conditions, step-by-step numbered instructions, exact commands, pitfalls section, and verification steps.", None),
        ("Skill Anatomy", "A skill file has YAML frontmatter with name, description, version, author, tags, and platform compatibility. The body contains markdown instructions with sections for prerequisites, numbered steps, code examples, configuration references, troubleshooting, and verification.", None),
        ("Skill Categories", "Organize skills by domain: software-development for coding tasks, devops for deployment and infrastructure, data-science for analysis, mlops for machine learning, research for information gathering, creative for content generation, and productivity for workflow automation.", None),
        ("Skill Loading & Triggers", "Skills are loaded on demand when their description matches the current task. The agent scans skill descriptions and loads relevant ones. Use clear, descriptive skill names and descriptions so your agent finds the right skill at the right time.", None),
        ("Self-Improving Skills", "Skills learn from corrections. When you correct your agent's approach, the skill can be updated using the patch action on skill manage. Over time, your skills become more refined, handling edge cases and following your preferred workflow.", None),
        ("Skill Versioning", "Each skill has a version field. Track changes and update as workflows evolve. The curator automatically suggests improvements and consolidations for stale or duplicate skills. Skills that are unused for 30 days enter a stale period.", None),
        ("Template Variables", "Skills support template variables for dynamic content. Use double curly braces for variable substitution. Set template vars to true in config to enable. This lets you create generic skills that adapt to specific contexts.", None),
        ("Sharing & Community", "Skills can be shared with the community. Export your best skills and publish them. The Hermes ecosystem grows as users contribute skills. Build a reputation as a skill author. Discover new capabilities from other users.", None),
        ("Skill Pitfalls", "Common pitfalls: overly broad triggers that load too many skills, instructions that are too vague, missing verification steps, not handling edge cases, and forgetting to update skills as workflows change. Review and refine your skills regularly.", None),
        ("Advanced Skill Patterns", "Combine multiple skills for complex workflows. Create umbrella skills that reference sub-skills. Use conditional logic in skill instructions. Chain skills together where one skill's output feeds into another. This is where skills become truly powerful.", None),
        ("Module Summary", "Skills are the heart of Hermes Agent. They make your agent smarter over time, encode your workflows, and eliminate repetitive instruction. In Module 6, we will cover training your agent through memory, corrections, and user profiles.", None),
    ]),
    (6, "module-06-training.md", "Training Your Agent", [
        ("Welcome", "Welcome to Module 6 of the Hermes Agent Master Course. In this module, we cover how to train your agent to work the way you want through persistent memory, corrections, user profiles, and teaching workflows.", None),
        ("The Memory System", "Hermes has two memory tiers. Session memory lives for the current conversation only. Persistent memory survives restarts and is injected into every future conversation. Use the memory tool to save durable facts that should always be available.", None),
        ("What to Save in Memory", "Save user preferences, environment details, project conventions, tool quirks, and stable configuration facts. Do not save task progress, temporary state, or completed work logs. The most valuable memory prevents you from having to repeat yourself.", None),
        ("Memory Best Practices", "Write memories as declarative facts. For example, user prefers concise responses rather than always respond concisely. Keep memory compact and focused. Prioritize user preferences and corrections over procedural knowledge. Review and clean memory periodically.", None),
        ("Correction Workflows", "When your agent gets something wrong, correct it. Say no, that is not right, here is how to do it. The agent learns from the correction. Over time, repeated corrections shape your agent's behavior to match your preferences exactly.", None),
        ("User Profiles", "The user profile stores who you are: your name, role, preferences, communication style, and pet peeves. Set this up in the memory system with target equals user. The agent reads your profile before every interaction.", None),
        ("Teaching by Example", "Show your agent how you want things done. When it suggests an approach you dislike, provide your preferred alternative. Demonstrate your workflow once; the agent remembers and defaults to your way next time.", None),
        ("The Learning Loop", "Every interaction is training data. The agent observes: when you accept its suggestions, when you correct it, when you provide alternatives, and when you reject its approach. This feedback loop continuously improves your agent.", None),
        ("Session Search for Recall", "Use session search to find past conversations. FTS5-powered retrieval finds relevant sessions by keywords. This lets your agent recall what was discussed weeks ago. Use it when the user references something from a past conversation.", None),
        ("Skill Creation from Corrections", "After completing a complex task or fixing a tricky error, save the approach as a skill. This codifies your workflow so the agent can reproduce it perfectly next time. Skills created from real corrections are the most valuable.", None),
        ("Training Cadence", "Be patient. The agent learns gradually. Spend 5 minutes after each session teaching and correcting. Over a week, your agent becomes noticeably better. Over a month, it is tuned specifically to your workflow.", None),
        ("Multi-User Training", "In a shared setup, each user has their own profile and memory. The agent adjusts its behavior per user. This is powerful for team deployments where different roles need different assistant behavior.", None),
        ("Memory Hygiene", "Periodically review what is in memory. Remove stale facts that no longer apply. Update preferences that have changed. The curator tool helps by suggesting memory cleanups for information older than 30 days.", None),
        ("Context Window Management", "Hermes uses compression to fit more context into each conversation. The compression engine summarizes older messages while preserving key information. Memory is always injected fresh, so important facts never get compressed away.", None),
        ("Module Summary", "Training your agent is an ongoing process. Use memory for durable facts, corrections for behavior tuning, skills for reusable workflows, and patience for gradual improvement. Your agent gets smarter every day with consistent training.", None),
    ]),
    (7, "module-07-gateway.md", "Multi-Platform Gateway", [
        ("Welcome", "Welcome to Module 7 of the Hermes Agent Master Course. In this module, we will connect your agent to messaging platforms using the Hermes Gateway. Your agent will work on Telegram, Discord, WhatsApp, and more.", None),
        ("What is the Gateway?", "The Hermes Gateway is a service that bridges your agent to messaging platforms. It runs as a background service and handles message routing, platform authentication, and delivery. Once configured, you can message your agent from any connected platform.", None),
        ("Telegram Setup", "To connect Telegram, create a bot using BotFather on Telegram. Send slash newbot, choose a name, get your bot token. Then configure the telegram section in your config.yaml with the token. Restart the gateway and your agent is live on Telegram.", None),
        ("Discord Setup", "For Discord, create a bot application in the Discord Developer Portal. Enable the bot, message content intent, and server members intent. Invite the bot to your server. Configure the discord section in config.yaml with your bot credentials.", None),
        ("WhatsApp Connection", "WhatsApp requires a Meta Business Account. Set up a WhatsApp Business API account through the Meta Developer Portal. Configure webhooks for message handling. The whatsapp section in config.yaml handles connection settings.", None),
        ("Cross-Platform Operation", "The same agent works on all platforms simultaneously. Start a task on Telegram, check progress on Discord, receive results via WhatsApp. The agent maintains context across platforms within the same conversation.", None),
        ("Platform Features", "Each platform offers unique capabilities. Telegram supports inline keyboards, voice messages, and media attachments. Discord has threaded conversations and rich embeds. WhatsApp provides end-to-end encryption and business messaging features.", None),
        ("Gateway Configuration", "The gateway runs as a background service. Start it with hermes gateway run or install it as a systemd service with hermes gateway install. Configure multiple profiles for different environments. Each profile can have different platform connections.", None),
        ("Security Considerations", "Platform gateways expose your agent to external users. Configure allowed chats and channels. Use approval modes for sensitive operations. Set up webhook secret verification. Monitor gateway logs for unusual activity.", None),
        ("Use Case: Server Alerts", "Connect your agent to send server alerts via Telegram. Set up a cron job to check system health every hour. If disk usage exceeds 90 percent, your agent sends an alert. Critical issues can escalate to phone notifications.", None),
        ("Use Case: Customer Support", "Deploy your agent on Discord for customer support. It handles common questions, triages issues, and escalates complex ones. Use skills for knowledge base queries. Track response times and satisfaction ratings.", None),
        ("Use Case: Personal Assistant", "Connect WhatsApp as your personal assistant. Ask your agent to check your calendar, summarize your emails, set reminders, or research topics. The agent uses web search and file tools to fulfill requests.", None),
        ("Gateway Troubleshooting", "Common issues: incorrect bot tokens, missing intents for Discord, webhook verification failures, and rate limiting. Use hermes gateway status to check connections. Review gateway logs for error messages. Test with a simple ping first.", None),
        ("Advanced Gateway Features", "The gateway supports channel prompts for different behavior per channel. Configure auto-thread for Discord conversations. Set up reactions for message acknowledgment. Use channel-specific configurations for fine-grained control.", None),
        ("Module Summary", "Your agent is now multi-platform. Connect it to the platforms your audience uses. In Module 8, we will deploy your agent to a VPS for 24-7 operation, ensuring it stays online and responsive around the clock.", None),
    ]),
    (8, "module-08-vps.md", "VPS Deployment", [
        ("Welcome", "Welcome to Module 8 of the Hermes Agent Master Course. In this module, we will deploy your agent to a cloud VPS for 24-7 operation. You will learn VPS setup, security hardening, systemd service configuration, and monitoring.", None),
        ("Choosing a VPS Provider", "DigitalOcean, Hetzner, and Vultr offer reliable VPS instances starting at 5 dollars per month. Choose a plan with at least 1 GB RAM and 25 GB storage. Ubuntu 22.04 LTS is recommended for compatibility. Deploy in a region close to your users.", None),
        ("Initial Server Setup", "After deploying, SSH into your server using the root password or SSH key. Update the system with sudo apt update and sudo apt upgrade. Set the hostname, configure the timezone, and create a non-root user with sudo access.", None),
        ("SSH Key Authentication", "Generate an SSH key pair on your local machine with ssh-keygen. Copy the public key to your server with ssh-copy-id. Disable password authentication in SSH config. This prevents brute force attacks on your SSH port.", None),
        ("Firewall Configuration", "Configure UFW, the uncomplicated firewall. Allow only SSH, HTTP, and HTTPS ports. Deny all other incoming connections. Allow outgoing connections for package updates and API access. Enable UFW and verify the rules are active.", None),
        ("Installing Hermes on VPS", "SSH into your VPS as the non-root user. Run the one-line installer. The installer handles all dependencies. After installation, run the setup wizard to configure your API keys and model provider. Test with a quick conversation.", None),
        ("Systemd Service Setup", "Create a systemd service file at etc systemd system slash hermes-gateway dot service. Define the service to run Hermes gateway as your non-root user. Set restart always and start limit interval to ensure the service stays up.", None),
        ("Service Management", "Enable the service to start on boot with systemctl enable. Start it with systemctl start. Check status with systemctl status. View logs with journalctl minus u hermes-gateway. Restart after configuration changes.", None),
        ("Security Hardening", "Go beyond basics. Install fail2ban to block repeated SSH failures. Set up automatic security updates. Configure a reverse proxy like Nginx if exposing webhooks. Use AppArmor or SELinux for additional isolation. Regular security audits.", None),
        ("Monitoring Setup", "Configure resource monitoring. Set up disk usage alerts with a cron job. Monitor memory and CPU usage. Install netdata or Prometheus for real-time metrics. Configure Telegram alerts for critical events like high CPU or low disk space.", None),
        ("Database Backups", "Hermes stores data in dot hermes. Set up automated backups to a remote location. Use cron jobs with rsync or rclone to copy data daily. Test your restore process. Without backups, a server failure means losing all your agent's training.", None),
        ("Scaling Considerations", "As your usage grows, scale vertically with a larger VPS or horizontally by splitting services across multiple servers. Consider separate servers for the gateway and the agent. Use Redis for session caching in high-availability setups.", None),
        ("Cost Optimization", "A 5 dollar VPS runs Hermes comfortably for personal use. For production deployments with multiple users, a 10 to 20 dollar VPS is sufficient. Monitor your API usage costs separately. Total monthly cost is typically under 15 dollars.", None),
        ("Disaster Recovery", "Document your server setup. Keep a recovery playbook. Store SSH keys and API keys in a secure password manager. Have a plan for migrating to a new VPS. Practice the restore process before you need it.", None),
        ("Module Summary", "Your agent is now deployed on a VPS, running 24-7 with monitoring, backups, and security hardening. In Module 9, we will explore monetization strategies to turn your agent into a revenue source.", None),
    ]),
    (9, "module-09-monetization.md", "Monetization Strategies", [
        ("Welcome", "Welcome to Module 9 of the Hermes Agent Master Course. In this module, we cover seven proven ways to monetize your Hermes Agent installation. From freelancing to SaaS, these strategies can generate income from 500 to over 10,000 dollars per month.", None),
        ("Strategy 1: Agent as a Service", "Build custom Hermes agents for clients. Each client gets their own agent with custom skills for their business. Charge a monthly setup and maintenance fee. Example: a real estate agent gets an agent that automates listing updates, lead follow-ups, and market research.", None),
        ("Strategy 2: White-Label Solutions", "Rebrand Hermes as your own product. Deploy multi-tenant instances where each client sees your branding. Sell access by subscription tier. This is the highest-margin model because the infrastructure cost per client is near zero.", None),
        ("Strategy 3: Skills Marketplace", "Create premium skills and sell them. Businesses need custom automations. Build a library of industry-specific skills. Charge per skill or offer a subscription to your skill vault. Skills are low overhead and highly scalable.", None),
        ("Strategy 4: Consulting & Training", "Offer Hermes consulting services. Help businesses set up and optimize their agents. Conduct training workshops. Charge 150 to 300 dollars per hour for consulting. Package training as a course for passive income.", None),
        ("Strategy 5: Automation Agency", "Run an automation agency. Client gives you a workflow problem, you build and deploy a Hermes solution. Recurring maintenance contracts provide steady income. Focus on high-value niches like e-commerce automation, lead generation, or customer support.", None),
        ("Strategy 6: Content Generation Service", "Use Hermes for automated content production. Generate blog posts, social media content, newsletters, and marketing copy at scale. Charge monthly retainers for content packages. Hermes handles research, writing, and formatting automatically.", None),
        ("Strategy 7: SaaS Product", "Build a full SaaS platform around Hermes. Multi-user, multi-tenant, with subscription tiers. Features like usage analytics, team management, premium skills, and priority support. This requires more development but has the highest revenue potential.", None),
        ("Pricing Your Services", "Basic setup and monthly maintenance: 500 dollars per month. White-label with custom skills: 1,000 to 2,500 dollars per month. Enterprise with SLA and dedicated support: 5,000 to 10,000 dollars per month. Price based on value delivered, not effort.", None),
        ("Finding Clients", "Start with your network. Offer free setup to one business in exchange for a testimonial. Join business automation groups on Facebook and LinkedIn. Cold outreach to real estate agents, e-commerce stores, and service businesses. Build case studies.", None),
        ("Scaling Your Operation", "Automate client setup with scripts and templates. Use a single VPS with multiple profiles for different clients. Create a standardized onboarding process. Develop reusable skill templates that adapt to each client's needs.", None),
        ("Legal Considerations", "Use written contracts with clear scope of work. Include SLA terms, data privacy clauses, and termination policies. Consider liability insurance for enterprise clients. Consult a lawyer for your specific jurisdiction.", None),
        ("Upsell Opportunities", "Every client is a recurring revenue opportunity. Upsell premium skills, priority support, custom integrations, training sessions, and monitoring services. Annual contracts with 10 to 20 percent discount provide predictable revenue.", None),
        ("Building Passive Income", "Create digital products: skill packs, training videos, templates, and guides. Sell on your own platform or marketplaces. Course sales, digital downloads, and subscription content generate income while you sleep.", None),
        ("Module Summary", "Monetization turns your Hermes skills into income. Start with one strategy, get your first client, build a case study, then expand. The skills you have built in this course are the foundation of your service offerings.", None),
    ]),
    (10, "module-10-advanced.md", "Advanced Use Cases", [
        ("Welcome", "Welcome to the final module of the Hermes Agent Master Course. In this module, we explore advanced use cases: trading bots, content automation, code review assistants, customer support, and data pipelines. These are production-grade applications.", None),
        ("Use Case 1: Trading Bots", "Build automated trading bots. Hermes monitors market data, analyzes trends, and executes trades based on your strategy. Connect to exchange APIs like Binance or Alpaca. Set up cron jobs for periodic analysis. Use subagents for concurrent market monitoring.", None),
        ("Trading Bot Architecture", "The trading system uses multiple subagents. One monitors price data, another analyzes technical indicators, a third manages risk and position sizing. A coordinator agent aggregates their outputs and makes trading decisions. All agents share a common trading log.", None),
        ("Use Case 2: Content Automation", "Automate content creation pipelines. Hermes researches topics, generates scripts, creates voiceovers with Edge TTS, renders videos with FFmpeg, and publishes to YouTube. Set up weekly content calendars with cron jobs.", None),
        ("Content Pipeline Details", "A content pipeline flows: Venice AI generates a script, Edge TTS creates voiceover, Python PIL generates visuals, FFmpeg composites the video, and the Zernio API publishes to social platforms. Each step can be parallelized with subagents.", None),
        ("Use Case 3: Code Review Assistant", "Deploy Hermes as an automated code reviewer. Connect it to your GitHub repository via webhooks. When a pull request is opened, Hermes reviews the code, checks for bugs, security issues, and style violations, then comments on the PR.", None),
        ("Code Review Setup", "Configure a GitHub webhook to trigger your agent on pull request events. Use the terminal tool to fetch and examine the code. Write a detailed review. Post inline comments using GitHub's API. Track review metrics over time.", None),
        ("Use Case 4: Customer Support", "Automate customer support with Hermes. Connect to your support platform via API. Hermes handles common questions, triages issues, searches knowledge base, drafts responses, and escalates complex problems to human agents.", None),
        ("Support System Architecture", "Multiple support agents handle different tiers. Tier one handles common FAQs. Tier two handles technical issues. Tier three escalates to humans. Conversation context is shared across tiers. Performance is measured by resolution time.", None),
        ("Use Case 5: Data Pipelines", "Build automated ETL pipelines. Hermes extracts data from APIs or databases, transforms it with Python scripts, and loads it into your warehouse. Set up scheduled runs with cron jobs. Monitor pipeline health with alerts.", None),
        ("Data Pipeline Example", "A daily pipeline: Hermes fetches sales data from Stripe API, transforms it into reporting format, generates a dashboard with matplotlib, saves it to storage, and sends the report via Telegram. All automated with no human intervention.", None),
        ("Use Case 6: Personal Research Assistant", "Deploy a dedicated research agent. Give it topics to investigate. It searches academic papers on ArXiv, summarizes findings, extracts key insights, and builds a knowledge base. Schedule weekly research digests.", None),
        ("Use Case 7: DevOps Automation", "Automate infrastructure management. Monitor server health, deploy updates, manage SSL certificates, rotate logs, scale resources, and respond to incidents. Use webhooks from monitoring tools like Grafana or Datadog.", None),
        ("Combining Multiple Use Cases", "The most powerful setup combines several use cases. A single Hermes instance can run trading strategies, manage content pipelines, review code, handle support tickets, and manage infrastructure, all simultaneously through subagent delegation.", None),
        ("Course Conclusion", "Congratulations! You have completed all 10 modules of the Hermes Agent Master Course. You have installed Hermes, configured it, trained it, deployed it, and built monetizable applications. You are now ready to build production-grade AI agent systems.", None),
        ("Next Steps", "Keep learning. Join the Hermes community. Share your skills. Build for clients. The agent ecosystem is growing fast and you are ahead of the curve. Thank you for taking this course and happy building with Hermes Agent.", None),
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
        duration = get_audio_duration(out_path)
        print(f"  Narration already exists: {duration:.1f}s")
        return out_path
    
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
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        font_footer = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        font_code = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Mono.ttf", 24)
    except:
        font_title = font_body = font_footer = font_code = ImageFont.load_default()
    
    # Grid background
    for x in range(0, W, 60):
        for y in range(0, H, 60):
            draw.point((x, y), fill=(12, 12, 28))
    
    # Subtle radial gradient overlay
    for y in range(H):
        r = 5 + int(8 * (1 - y / H))
        g = 5 + int(6 * (1 - y / H))
        b = 11 + int(10 * (1 - y / H))
        for x in range(0, W, 4):
            draw.point((x, y), fill=(r, g, b))
    
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
        alpha = min(255, int(255 * progress))
        
        # Big module number behind
        num_label = f"0{frame_num // 100 + 1}" if frame_num // 100 + 1 < 10 else f"{frame_num // 100 + 1}"
        draw.text((W // 2 - 400, 60), f"Module {num_label}", fill=(int(alpha * 0.06), int(alpha * 0.04), int(alpha * 0.10)), font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 140))
        
        # Module badge
        bbox = draw.textbbox((0, 0), f"MODULE {num_label}", font=font_footer)
        tw = bbox[2] - bbox[0]
        draw.rounded_rectangle([W // 2 - tw // 2 - 20, 230, W // 2 + tw // 2 + 20, 270], radius=8, fill=(108, 92, 231, int(alpha * 0.25)))
        draw.text((W // 2 - tw // 2, 235), f"MODULE {num_label}", fill=(int(alpha), int(alpha * 0.8), int(alpha * 1.0)), font=font_footer)
        
        # Title
        lines = textwrap.wrap(title, width=22)
        for li, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_title)
            tw = bbox[2] - bbox[0]
            c = int(alpha * 0.9)
            draw.text(((W - tw) // 2, 320 + li * 70), line, fill=(c, c, min(255, c + 20)), font=font_title)
    
    elif slide_type == "content":
        # Title at top
        c = int(255 * progress)
        bbox = draw.textbbox((0, 0), title, font=font_title)
        draw.text((100, 60), title, fill=(0, c, int(c * 0.9)), font=font_title)
        
        # Separator line
        draw.rectangle([100, 115, W - 100, 117], fill=(int(c * 0.08), int(c * 0.12), int(c * 0.15)))
        
        # Body text - fade in line by line
        for li, line in enumerate(body_lines):
            line_alpha = max(0, min(255, int(255 * (progress * len(body_lines) * 1.2 - li * 0.8))))
            if line_alpha <= 0:
                continue
            
            c2 = int(line_alpha * 0.85)
            y = 150 + li * 55
            
            if line.startswith("- "):
                # Bullet point
                draw.ellipse([95, y + 8, 105, y + 18], fill=(int(c2 * 0.5), c2, int(c2 * 0.5)))
                draw.text((120, y), line[2:], fill=(c2, c2, c2), font=font_body)
            else:
                draw.text((100, y), line, fill=(c2, c2, c2), font=font_body)
    
    elif slide_type == "outro":
        alpha = min(255, int(255 * progress))
        
        # Terminal-style box
        draw.rounded_rectangle([350, 250, 1570, 550], radius=14, fill=(10, 10, 20), outline=(int(alpha * 0.3), int(alpha * 0.2), int(alpha * 0.4)))
        draw.rounded_rectangle([350, 250, 1570, 290], radius=14, fill=(15, 15, 30))
        draw.rectangle([350, 275, 1570, 290], fill=(15, 15, 30))
        
        # Title bar dots
        for dx in [370, 390, 410]:
            draw.ellipse([dx, 260, dx + 8, 268], fill=(int(alpha * 0.3), int(alpha * 0.15), int(alpha * 0.2)))
        
        for li, line in enumerate(body_lines):
            c = int(alpha * 0.9)
            color = (int(c * 0.7), c, int(c * 0.6)) if li == 0 else (c, c, c)
            draw.text((420, 310 + li * 48), line, fill=color, font=font_body)
        
        # Cursor blink
        if frame_num % 12 < 6:
            last_len = len(body_lines[-1]) if body_lines else 0
            draw.text((420 + last_len * 15, 310 + (len(body_lines) - 1) * 48), "_", fill=(0, 206, 201), font=font_body)
    
    return img


def generate_module_video(num, title, slides_data, narration_text):
    """Generate a complete module walkthrough video."""
    out_path = os.path.join(OUTPUT_DIR, f"module-{num:02d}-walkthrough.mp4")
    if os.path.exists(out_path):
        size = os.path.getsize(out_path) / 1024 / 1024
        print(f"  Walkthrough already exists: {size:.1f} MB")
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
    num_slides = len(slides_data) + 2  # title + content slides + outro
    frames_per_slide = total_frames // num_slides
    
    # 4. Render frames
    print(f"  Rendering {total_frames} frames ({audio_duration:.1f}s audio, {num_slides} slides)...")
    
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
    
    # Content slides
    for slide_title, slide_body, code_block in slides_data:
        body_lines = textwrap.wrap(slide_body, width=85)
        for i in range(frames_per_slide):
            progress = i / frames_per_slide
            img = make_slide("content", slide_title, body_lines, progress, i, frames_per_slide)
            img.save(os.path.join(frames_dir, f"frame_{frame_idx:06d}.png"))
            frame_idx += 1
    
    # Outro slide
    outro_lines = [
        "Module complete!",
        f"Continue to the next module for more advanced concepts.",
        "",
        "Hermes Agent Master Course",
        "hermes-course@agentmail.to",
    ]
    for i in range(frames_per_slide):
        progress = i / frames_per_slide
        img = make_slide("outro", "Module Complete", outro_lines, progress, i, frames_per_slide)
        img.save(os.path.join(frames_dir, f"frame_{frame_idx:06d}.png"))
        frame_idx += 1
    
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
    """Build a detailed narration script from slide data."""
    lines = [f"Welcome to Module {num}: {title}."]
    lines.append("")
    
    for slide_title, slide_body, code_block in slides_data:
        lines.append(slide_body)
    
    lines.append("")
    lines.append(f"This concludes Module {num}: {title}.")
    lines.append("Continue to the next module for more advanced concepts.")
    lines.append("Happy building with Hermes Agent!")
    
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("GENERATING UPGRADED MODULE WALKTHROUGH VIDEOS")
    print("15+ slides per module, 2-3 minute narration each")
    print("=" * 60)
    
    for num, filename, title, slides_data in MODULE_DATA:
        print(f"\nModule {num}: {title} ({len(slides_data)} slides)")
        
        # Build narration
        narration = build_narration_script(num, title, slides_data)
        
        # Generate video
        generate_module_video(num, title, slides_data, narration)
        
        print(f"  Done!")
    
    print("\n" + "=" * 60)
    print("ALL MODULE WALKTHROUGH VIDEOS COMPLETE!")
    print("=" * 60)
    
    # List generated videos
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if "walkthrough" in f:
            path = os.path.join(OUTPUT_DIR, f)
            size = os.path.getsize(path) / 1024 / 1024
            print(f"  {f} - {size:.1f} MB")


if __name__ == "__main__":
    main()
