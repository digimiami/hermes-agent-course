#!/usr/bin/env python3
"""Convert all Hermes Course markdown modules to styled HTML pages."""
import os, re

OUTPUT_DIR = "/root/hermes-course/course"
MODULES = [
    ("module-01-intro.md",           "What is Hermes Agent & Why It Matters"),
    ("module-02-installation.md",    "Installation & First Run"),
    ("module-03-configuration.md",   "Configuration Deep Dive"),
    ("module-04-usage.md",           "Daily Usage & Power Features"),
    ("module-05-skills.md",          "Skills System - The Killer Feature"),
    ("module-06-training.md",        "Training Your Agent"),
    ("module-07-gateway.md",         "Multi-Platform Gateway"),
    ("module-08-vps.md",             "VPS Deployment"),
    ("module-09-monetization.md",    "Monetization Strategies"),
    ("module-10-advanced.md",        "Advanced Use Cases"),
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AI Agents: Master Hermes Agent</title>
    <link rel="icon" type="image/x-icon" href="../assets/favicon.ico">
    <link rel="icon" type="image/png" href="../assets/favicon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: #05050b;
            color: #d0d0d8;
            line-height: 1.7;
        }
        .bg-grid {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: linear-gradient(rgba(108,92,231,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(108,92,231,0.03) 1px, transparent 1px);
            background-size: 60px 60px;
            pointer-events: none; z-index: 0;
        }
        .container { max-width: 840px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 1; }
        .course-header {
            padding: 40px 0 20px;
            border-bottom: 1px solid rgba(108,92,231,0.08);
            margin-bottom: 40px;
        }
        .course-header .back {
            color: #6c5ce7; text-decoration: none; font-size: 0.85em; font-weight: 600;
            display: inline-flex; align-items: center; gap: 6px; margin-bottom: 16px;
        }
        .course-header .back:hover { color: #00cec9; }
        .course-header h1 {
            font-size: 2em; font-weight: 800;
            background: linear-gradient(135deg, #a78bfa, #00cec9);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .course-header .meta { color: #606080; font-size: 0.85em; margin-top: 6px; }
        .course-header .nav-links {
            display: flex; gap: 12px; margin-top: 18px; flex-wrap: wrap;
        }
        .course-header .nav-links a {
            padding: 8px 18px; border-radius: 8px; font-size: 0.82em; font-weight: 600;
            text-decoration: none; transition: all 0.2s;
        }
        .nav-prev { background: rgba(108,92,231,0.08); color: #a78bfa; border: 1px solid rgba(108,92,231,0.1); }
        .nav-prev:hover { background: rgba(108,92,231,0.15); }
        .nav-next { background: linear-gradient(135deg, #6c5ce7, #00cec9); color: #fff; }
        .nav-next:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(108,92,231,0.3); }
        .nav-index { background: rgba(108,92,231,0.06); color: #808098; border: 1px solid rgba(108,92,231,0.08); }
        .nav-index:hover { color: #fff; }
        .content { padding-bottom: 60px; }
        .content h2 { color: #a78bfa; font-size: 1.4em; font-weight: 700; margin-top: 36px; margin-bottom: 12px; }
        .content h3 { color: #c0c0e0; font-size: 1.15em; font-weight: 700; margin-top: 28px; margin-bottom: 10px; }
        .content h4 { color: #e0e0e8; font-size: 1em; font-weight: 700; margin-top: 24px; margin-bottom: 8px; }
        .content p { margin-bottom: 16px; color: #a0a0b0; font-size: 0.95em; }
        .content ul, .content ol { margin: 0 0 16px 24px; color: #a0a0b0; font-size: 0.95em; }
        .content li { margin-bottom: 6px; }
        .content strong { color: #e0e0e8; }
        .content code {
            background: rgba(108,92,231,0.08); padding: 2px 8px; border-radius: 4px;
            font-family: 'JetBrains Mono', monospace; font-size: 0.88em; color: #a0e0a0;
        }
        .content pre {
            background: rgba(10,10,20,0.8); border: 1px solid rgba(108,92,231,0.1);
            border-radius: 10px; padding: 18px 22px; margin: 20px 0; overflow-x: auto;
        }
        .content pre code { background: none; padding: 0; font-size: 0.85em; color: #b0d0b0; }
        .content blockquote {
            border-left: 3px solid #6c5ce7; padding: 12px 20px; margin: 20px 0;
            background: rgba(108,92,231,0.04); border-radius: 0 10px 10px 0;
            color: #9090a8; font-size: 0.92em;
        }
        .content table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.88em; }
        .content th, .content td { padding: 10px 14px; border: 1px solid rgba(108,92,231,0.08); text-align: left; }
        .content th { background: rgba(108,92,231,0.06); color: #c0c0d8; font-weight: 600; }
        .content td { color: #9090a8; }
        .content hr { border: none; border-top: 1px solid rgba(108,92,231,0.08); margin: 36px 0; }
        .content .module-nav-bottom {
            display: flex; justify-content: space-between; align-items: center;
            padding: 24px 0; margin-top: 40px;
            border-top: 1px solid rgba(108,92,231,0.08);
        }
        @media (max-width: 600px) {
            .course-header h1 { font-size: 1.4em; }
            .content h2 { font-size: 1.15em; }
        }
    </style>
</head>
<body>
<div class="bg-grid"></div>
<div class="container">
    <div class="course-header">
        <a href="index.html" class="back">Back to Course Dashboard</a>
        <h1>MODULE_TITLE_HERE</h1>
        <p class="meta">Module MODULE_NUM_HERE of 10</p>
        <div class="nav-links">
            PREV_LINK_HERE
            <a href="index.html" class="nav-index">All Modules</a>
            NEXT_LINK_HERE
        </div>
    </div>
"""

FOOTER_TEMPLATE = """
    <div class="module-nav-bottom">
        PREV_BOTTOM_HERE
        <a href="index.html" style="color:#606080;font-size:0.85em;text-decoration:none;">Dashboard</a>
        NEXT_BOTTOM_HERE
    </div>
</div>
</body>
</html>"""

def build_prev_link(num):
    if num <= 1:
        return '<span></span>'
    prev_fn = MODULES[num-2][0].replace('.md', '.html')
    prev_title = MODULES[num-2][1][:25]
    return '<a href="' + prev_fn + '" class="nav-prev">' + prev_title + '</a>'

def build_next_link(num):
    if num >= 10:
        return '<span></span>'
    next_fn = MODULES[num][0].replace('.md', '.html')
    next_title = MODULES[num][1][:25]
    return '<a href="' + next_fn + '" class="nav-next">Next: ' + next_title + '</a>'

def build_prev_bottom(num):
    if num <= 1:
        return '<span></span>'
    prev_fn = MODULES[num-2][0].replace('.md', '.html')
    style = 'padding:10px 20px;border-radius:8px;font-size:0.85em;font-weight:600;text-decoration:none;background:rgba(108,92,231,0.08);color:#a78bfa;border:1px solid rgba(108,92,231,0.1);'
    n = num - 1
    return '<a href="' + prev_fn + '" class="nav-prev" style="' + style + '">Module ' + str(n) + '</a>'

def build_next_bottom(num):
    if num >= 10:
        return '<span></span>'
    next_fn = MODULES[num][0].replace('.md', '.html')
    style = 'padding:10px 20px;border-radius:8px;font-size:0.85em;font-weight:600;text-decoration:none;background:linear-gradient(135deg,#6c5ce7,#00cec9);color:#fff;'
    n = num + 1
    return '<a href="' + next_fn + '" class="nav-next" style="' + style + '">Module ' + str(n) + '</a>'

def convert_md_to_html(md_text):
    """Simple markdown to HTML converter for our module format."""
    lines = md_text.split('\n')
    html_lines = []
    in_code = False
    in_table = False

    for line in lines:
        if line.startswith('```'):
            if in_code:
                html_lines.append('</code></pre>')
                in_code = False
            else:
                html_lines.append('<pre><code>')
                in_code = True
            continue
        if in_code:
            safe = line.replace('<', '&lt;').replace('>', '&gt;')
            html_lines.append(safe)
            continue

        if line.startswith('##### '):
            html_lines.append('<h4>' + line[6:] + '</h4>')
        elif line.startswith('#### '):
            html_lines.append('<h4>' + line[5:] + '</h4>')
        elif line.startswith('### '):
            html_lines.append('<h3>' + line[4:] + '</h3>')
        elif line.startswith('## '):
            html_lines.append('<h2>' + line[3:] + '</h2>')
        elif line.startswith('# '):
            html_lines.append('<h1>' + line[2:] + '</h1>')
        elif line.startswith('> '):
            html_lines.append('<blockquote>' + line[2:] + '</blockquote>')
        elif line.strip() == '---' or line.strip() == '***':
            if in_table:
                html_lines.append('</tbody></table>')
                in_table = False
            html_lines.append('<hr>')
        elif line.startswith('|') and line.endswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(c.startswith('-') or c == '' for c in cells):
                continue
            if not in_table:
                in_table = True
                html_lines.append('<table><thead><tr>')
                for c in cells:
                    html_lines.append('<th>' + c + '</th>')
                html_lines.append('</tr></thead><tbody>')
            else:
                html_lines.append('<tr>')
                for c in cells:
                    html_lines.append('<td>' + c + '</td>')
                html_lines.append('</tr>')
        else:
            if in_table:
                html_lines.append('</tbody></table>')
                in_table = False
            if not line.strip():
                continue
            html_lines.append('<p>' + line + '</p>')

    if in_table:
        html_lines.append('</tbody></table>')
    if in_code:
        html_lines.append('</code></pre>')

    return '\n'.join(html_lines)

def build():
    for i, (filename, title) in enumerate(MODULES, 1):
        num = i
        filepath = os.path.join("/root/hermes-course", filename)
        if not os.path.exists(filepath):
            print("SKIP: " + filename + " not found")
            continue

        with open(filepath) as f:
            md_content = f.read()

        # Strip the first h1 line (already in header template)
        md_content = re.sub(r'^# .*\n?', '', md_content.strip())

        html_body = convert_md_to_html(md_content)

        full_html = HEADER_TEMPLATE
        full_html = full_html.replace('MODULE_TITLE_HERE', title)
        full_html = full_html.replace('MODULE_NUM_HERE', str(num))
        full_html = full_html.replace('PREV_LINK_HERE', build_prev_link(num))
        full_html = full_html.replace('NEXT_LINK_HERE', build_next_link(num))

        full_html += '<div class="content">\n' + html_body + '\n</div>'

        footer = FOOTER_TEMPLATE
        footer = footer.replace('PREV_BOTTOM_HERE', build_prev_bottom(num))
        footer = footer.replace('NEXT_BOTTOM_HERE', build_next_bottom(num))
        full_html += footer

        out_fn = filename.replace('.md', '.html')
        out_path = os.path.join(OUTPUT_DIR, out_fn)
        with open(out_path, 'w') as f:
            f.write(full_html)

        print("Module " + str(num) + ": " + title + " -> " + out_fn)

    print("All " + str(len(MODULES)) + " modules converted!")

if __name__ == '__main__':
    build()
