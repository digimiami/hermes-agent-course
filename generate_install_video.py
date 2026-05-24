#!/usr/bin/env python3
"""Generate a step-by-step Hermes Agent installation video using the video-walkthrough-generator skill."""
import os, sys, importlib.util
spec = importlib.util.spec_from_file_location("gen", "/root/.hermes/skills/creative/video-walkthrough-generator/scripts/generate_video.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)
generate_video = gen.generate_video

SLIDES = [
    # (heading, body_text, code_or_none, demo_key_or_none)
    
    ("How to Install Hermes Agent",
     "Welcome! In this step-by-step tutorial, you will learn how to install Hermes Agent on your machine from scratch. By the end, you will have a fully working AI agent ready to chat.",
     None, None),
    
    ("What You Will Need",
     "To get started, you only need a terminal and Git installed. On Linux, run sudo apt install git. On macOS, use xcode-select —install. Everything else, including Python and Node.js, is installed automatically by the Hermes installer.",
     None, None),
    
    ("Get an API Key",
     "Hermes needs an LLM provider to work. The easiest option for beginners is OpenRouter. Go to openrouter.ai forward slash keys, create a free account, and generate an API key. The free tier gives you plenty of credits to get started. Top up with 5 dollars to access 200 plus models.",
     None, None),
    
    ("One-Line Install Command",
     "Open your terminal and run this single command. It downloads and runs the official Hermes installer. The script is signed and verified by Nous Research.",
     "curl -fsSL https://hermes.sh | bash", None),
    
    ("What the Installer Does",
     "The installer clones the Hermes repository, creates a Python virtual environment, installs all Python dependencies, sets up Node.js for browser automation, installs Playwright browsers, and adds the hermes command to your PATH. It takes about 2 minutes on a typical connection.",
     None, None),
    
    ("Install Complete",
     "After the installer finishes, you see a success message. Hermes is now installed in your home directory at dot hermes. The command is ready to use in your terminal.",
     "✓ Hermes installed successfully!\n✓ Python 3.11 configured\n✓ Node.js + Playwright ready\n✓ 'hermes' command available", None),
    
    ("Run the Setup Wizard",
     "After installation, run source dot bashrc or just restart your terminal. Then type hermes and press Enter. The interactive setup wizard will guide you through choosing your model provider, entering your API key, and naming your agent.",
     None, "hermes_setup"),
    
    ("Setup Wizard in Action",
     "The wizard presents a clean interface. Select OpenRouter as your provider if you want access to 200 plus models. Enter the API key you generated earlier. Give your agent a name. The whole process takes under 2 minutes and your configuration is saved automatically.",
     None, None),
    
    ("Your First Chat",
     "Once setup is complete, you are dropped directly into an interactive chat session. Try asking your agent a question like, What tools do you have available? The agent will list dozens of built-in capabilities, from file operations to web browsing to code execution.",
     None, "hermes_chat"),
    
    ("Verify Everything Works",
     "Run hermes doctor to check that everything is configured correctly. The doctor checks your Python version, virtual environment, configuration files, API keys, and installed dependencies. All green checks mean you are good to go.",
     None, "hermes_doctor"),
    
    ("Explore Configuration",
     "Run hermes config show to see your current setup. You can see your default model, provider, toolsets, and any connected platforms. Switch providers at any time with the hermes model command.",
     None, "hermes_config"),
    
    ("Installation Complete",
     "You have successfully installed Hermes Agent! In just a few minutes you went from zero to a fully functional AI agent with terminal access, file operations, web browsing, and more. Your agent is ready to help with coding, research, automation, and everything in between.",
     None, None),
    
    ("What is Next",
     "From here you can connect Hermes to Telegram or Discord via the gateway system, create custom skills to teach your agent new abilities, set up cron jobs for automated tasks, or deploy on a VPS for 24/7 operation. The official documentation has guides for all of these.",
     None, None),
    
    ("Thanks for Watching",
     "Thank you for following along. You now have a powerful AI agent running on your own machine, fully private and under your control. Subscribe to the channel for more tutorials on skills, deployment, and advanced automation with Hermes Agent.",
     None, None),
]

print("🎬 Generating step-by-step Hermes Agent installation video...\n")
result = generate_video(0, "How to Install Hermes Agent", SLIDES, output_dir="/root/hermes-course/course/videos")

if result:
    import subprocess
    dur = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",result], capture_output=True, text=True).stdout.strip()
    print(f"\n✅ Installation video ready!")
    print(f"   Path: {result}")
    print(f"   Duration: {float(dur):.0f}s ({float(dur)/60:.1f} min)")
    print(f"   Size: {os.path.getsize(result)/(1024*1024):.1f} MB")
else:
    print(f"\n❌ Video generation failed")
