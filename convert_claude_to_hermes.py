#!/usr/bin/env python3
"""
Convert Claude Code skills to Hermes Agent skills.
Reads from claude-code-skills/plugins/*/skills/*/SKILL.md
Writes to ~/.hermes/skills/<category>/<name>/SKILL.md
"""
import os, re, sys, yaml, shutil, textwrap
from pathlib import Path

CLAUDE_SKILLS_DIR = "/root/claude-code-skills/plugins"
HERMES_SKILLS_DIR = os.path.expanduser("~/.hermes/skills")

# Map Claude Code plugins to Hermes categories
PLUGIN_CATEGORY_MAP = {
    "agile-workflow": "software-development",
    "codebase-audit-suite": "software-development",
    "community-engagement": "software-development",  # or github
    "documentation-pipeline": "software-development",
    "optimization-suite": "software-development",
    "project-bootstrap": "software-development",
    "setup-environment": "devops",
}

# Tools that need conversion from Claude Code → Hermes
TOOL_MAP = {
    "Bash": "terminal",
    "Read": "read_file",
    "Write": "write_file",
    "Grep": "search_files",
    "Glob": "search_files(target='files')",
    "Edit": "patch",
    "WebFetch": "web_extract",
    "WebSearch": "web_search",
    "Git": "terminal(git ...)",
}

def slugify(name):
    """Convert skill name to Hermes-compatible slug."""
    name = name.lower()
    name = re.sub(r'[^a-z0-9-]', '-', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    return name

def parse_claude_skill(filepath):
    """Parse a Claude Code SKILL.md into components."""
    with open(filepath) as f:
        content = f.read()
    
    # Extract frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return None
    
    fm_text = fm_match.group(1)
    frontmatter = yaml.safe_load(fm_text)
    
    # Extract body (after frontmatter)
    body = content[fm_match.end():].strip()
    
    return {
        "frontmatter": frontmatter,
        "body": body,
        "all": content
    }

def extract_title(body):
    """Extract the main title from the body."""
    m = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    return m.group(1).strip() if m else ""

def extract_overview(body):
    """Extract overview/intro paragraph(s)."""
    # Get text before first ## heading
    parts = re.split(r'^##\s+', body, 1, re.MULTILINE)
    if len(parts) > 1:
        intro = parts[0].strip()
        # Remove the # title line
        intro = re.sub(r'^#\s+.*$', '', intro, flags=re.MULTILINE).strip()
        # Remove path marker and metadata
        intro = re.sub(r'> \*\*Paths:.*?\*\*', '', intro)
        intro = re.sub(r'\*\*Type:.*?\*\*', '', intro)
        intro = re.sub(r'\*\*Category:.*?\*\*', '', intro)
        intro = re.sub(r'\*\*Invocation:.*?\*\*', '', intro)
        return intro.strip()
    return ""

def extract_phases(body):
    """Extract phase sections as actionable steps."""
    phases = []
    # Split by ## Phase N: 
    for match in re.finditer(r'^##\s+(Phase\s+\d+[^:]*:|.*?)\s*$', body, re.MULTILINE | re.IGNORECASE):
        start = match.end()
        # Find next phase or end
        next_match = re.search(r'^##\s+(Phase\s+\d+|Overview|Arguments)', body[start:], re.MULTILINE | re.IGNORECASE)
        if next_match:
            phase_content = body[start:start + next_match.start()].strip()
        else:
            phase_content = body[start:].strip()
        
        title = match.group(1).strip()
        phases.append((title, phase_content))
    
    return phases

def extract_bash_commands(text):
    """Extract bash commands from code blocks."""
    cmds = re.findall(r'```(?:bash|sh)?\n(.*?)```', text, re.DOTALL)
    return [c.strip() for c in cmds if c.strip()]

def convert_to_hermes(claude_skill, plugin_name):
    """Convert a parsed Claude Code skill to Hermes format."""
    fm = claude_skill["frontmatter"]
    body = claude_skill["body"]
    
    name = slugify(fm.get("name", "unnamed-skill"))
    description = fm.get("description", f"Converted from Claude Code skill: {fm.get('name', 'unknown')}")
    
    # Truncate description if too long
    if len(description) > 1024:
        description = description[:1021] + "..."
    
    title = extract_title(body)
    overview = extract_overview(body)
    phases = extract_phases(body)
    
    # Build Hermes SKILL.md
    hermes = []
    
    # Frontmatter
    hermes.append("---")
    hermes.append(f"name: {name}")
    hermes.append(f"description: \"{description}\"")
    hermes.append("version: 1.0.0")
    hermes.append("author: Claude Code → Hermes Converter")
    hermes.append("license: MIT")
    
    tags = [slugify(plugin_name)]
    if "setup" in name or "dev" in name or "env" in name:
        tags.append("setup")
    if "audit" in name or "code" in name or "review" in name:
        tags.append("code-quality")
    if "doc" in name or "readme" in name:
        tags.append("documentation")
    if "agile" in name or "sprint" in name or "task" in name or "story" in name:
        tags.append("workflow")
    
    hermes.append("metadata:")
    hermes.append("  hermes:")
    hermes.append(f"    tags: [{', '.join(tags)}]")
    hermes.append("---")
    hermes.append("")
    
    # Title
    hermes.append(f"# {title or name}")
    hermes.append("")
    
    # Overview
    if overview:
        # Determine what this skill does
        hermes.append("## Overview")
        hermes.append("")
        hermes.append(overview)
        hermes.append("")
    
    # When to Use
    hermes.append("## When to Use")
    hermes.append("")
    hermes.append(f"- Trigger: {description}")
    if "audit" in name or "review" in name or "check" in name:
        hermes.append("- Run this when you need to analyze or review code")
        hermes.append("- Combine with other skills for comprehensive workflow")
    elif "setup" in name or "init" in name or "bootstrap" in name or "create" in name:
        hermes.append("- Run this at project start or when setting up new components")
    elif "doc" in name:
        hermes.append("- Run when documentation needs to be generated or updated")
    else:
        hermes.append("- Run this when the task matches the skill description")
    hermes.append("")
    
    # Phases → Actionable Steps
    if phases:
        hermes.append("## Steps")
        hermes.append("")
        
        for i, (phase_title, phase_content) in enumerate(phases, 1):
            # Clean up the phase content
            cleaned = phase_content
            
            # Extract and convert mandatory reads
            mandatory_refs = re.findall(r'\*\*MANDATORY READ:\*\*\s*Load\s+`?([^`\n]+)`?', cleaned)
            for ref in mandatory_refs:
                cleaned = cleaned.replace(f"**MANDATORY READ:** Load `{ref}`", f"  ⚠ First load: `{ref}`")
                cleaned = cleaned.replace(f"**MANDATORY READ:** Load {ref}", f"  ⚠ First load: {ref}")
            
            # Convert $ARGUMENTS references
            cleaned = cleaned.replace("$ARGUMENTS", "[user-provided parameters]")
            
            # Clean up the phase text
            hermes.append(f"### {i}. {phase_title}")
            hermes.append("")
            hermes.append(cleaned)
            hermes.append("")
    
    # Convert bash commands to Hermes terminal commands
    all_cmds = extract_bash_commands(body)
    if all_cmds:
        hermes.append("### Example Commands")
        hermes.append("")
        hermes.append("Run these in your terminal via Hermes:")
        hermes.append("")
        for cmd in all_cmds[:5]:  # Limit to first 5
            hermes.append(f"```bash")
            hermes.append(cmd[:300])  # Truncate very long commands
            hermes.append("```")
            hermes.append("")
    
    # Common Pitfalls (original if any, else generic)
    original_pitfalls = re.findall(r'(?:##\s+(?:Pitfalls|Common Issues|Troubleshooting|Gotchas).*?)(?:\n##\s|\Z)', body, re.DOTALL | re.IGNORECASE)
    if original_pitfalls:
        hermes.append("## Common Pitfalls")
        hermes.append("")
        for pit in original_pitfalls:
            # Remove the heading
            pit_clean = re.sub(r'^##\s+.*$', '', pit, flags=re.MULTILINE).strip()
            hermes.append(pit_clean)
            hermes.append("")
    else:
        hermes.append("## Common Pitfalls")
        hermes.append("")
        hermes.append("1. **Missing dependencies** — Ensure required tools (gh, git, etc.) are installed")
        hermes.append("2. **Authentication issues** — Verify you're logged in before running commands")
        hermes.append("3. **Scope too broad** — Narrow the task scope if the agent gets overwhelmed")
        hermes.append("")
    
    # Verification Checklist
    hermes.append("## Verification Checklist")
    hermes.append("")
    hermes.append("- [ ] Task output matches expected results")
    hermes.append("- [ ] No errors in terminal output")
    hermes.append("- [ ] Changes are reviewed and correct")
    hermes.append("")
    
    result = "\n".join(hermes)
    
    # Validate size
    if len(result) > 100000:
        # Truncate by removing example commands section
        result = re.sub(r'### Example Commands.*?(?=\n## Common Pitfalls|\Z)', '', result, flags=re.DOTALL)
    
    return result, name

def convert_all():
    """Convert all Claude Code skills to Hermes skills."""
    converted = []
    skipped = []
    
    plugin_dirs = sorted(os.listdir(CLAUDE_SKILLS_DIR))
    
    for plugin in plugin_dirs:
        plugin_path = os.path.join(CLAUDE_SKILLS_DIR, plugin)
        if not os.path.isdir(plugin_path):
            continue
        
        skills_dir = os.path.join(plugin_path, "skills")
        if not os.path.isdir(skills_dir):
            continue
        
        category = PLUGIN_CATEGORY_MAP.get(plugin, "software-development")
        
        for skill_name in sorted(os.listdir(skills_dir)):
            skill_path = os.path.join(skills_dir, skill_name, "SKILL.md")
            if not os.path.isfile(skill_path):
                continue
            
            print(f"  Converting {plugin}/{skill_name}...", end=" ")
            
            try:
                claude_skill = parse_claude_skill(skill_path)
                if not claude_skill:
                    print("⏭ No frontmatter")
                    skipped.append(f"{plugin}/{skill_name}")
                    continue
                
                hermes_content, hermes_name = convert_to_hermes(claude_skill, plugin)
                
                # Write to Hermes skills directory
                hermes_dir = os.path.join(HERMES_SKILLS_DIR, category, hermes_name)
                os.makedirs(hermes_dir, exist_ok=True)
                
                with open(os.path.join(hermes_dir, "SKILL.md"), 'w') as f:
                    f.write(hermes_content)
                
                converted.append(f"{plugin}/{skill_name} → {category}/{hermes_name}")
                print(f"✅")
                
            except Exception as e:
                print(f"❌ {e}")
                skipped.append(f"{plugin}/{skill_name}")
    
    print(f"\n{'='*60}")
    print(f"Converted: {len(converted)} skills")
    print(f"Skipped: {len(skipped)} skills")
    print(f"{'='*60}")
    
    # Summary by category
    cats = {}
    for c in converted:
        cat = c.split("→")[1].strip().split("/")[0]
        cats[cat] = cats.get(cat, 0) + 1
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count} skills")
    
    return converted, skipped

if __name__ == "__main__":
    print("🚀 Converting Claude Code Skills → Hermes Agent Skills")
    print(f"{'='*60}")
    print(f"Source: {CLAUDE_SKILLS_DIR}")
    print(f"Target: {HERMES_SKILLS_DIR}")
    print(f"{'='*60}\n")
    
    converted, skipped = convert_all()
