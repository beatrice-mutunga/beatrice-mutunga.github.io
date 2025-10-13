#!/usr/bin/env python3
"""
generate_lab_pages.py
Generates lab-data/index.json and projects/<slug>.html from markdown files in lab-data/.
Run: python generate_lab_pages.py
"""

import os, json, pathlib, sys
import markdown
import yaml
from jinja2 import Template

ROOT = pathlib.Path(__file__).parent.resolve()
LAB_DIR = ROOT / 'lab-data'
OUT_DIR = ROOT / 'projects'
INDEX_FILE = LAB_DIR / 'index.json'
TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{{ title }} — Writeup | Beatrice Mutunga</title>
<link rel="stylesheet" href="../style.css" />
<style>
  body{background:#0d1117;color:#c9d1d9;font-family:Inter,Segoe UI,system-ui,Roboto,Arial;}
  .wrap{max-width:900px;margin:22px auto;padding:20px;background:linear-gradient(180deg,rgba(255,255,255,0.02),rgba(255,255,255,0.01));border-radius:10px;}
  h1{color:#fff}
  .meta{color:#9aa5b1}
  .md-content img{max-width:100%;border-radius:8px}
  pre{background:#071025;padding:12px;border-radius:8px;overflow:auto;color:#d6deff}
  .flag{display:inline-block;background:linear-gradient(90deg,rgba(245,197,66,0.06),rgba(88,166,255,0.02));padding:8px 12px;border-radius:6px;color:#fff}
</style>
</head>
<body>
  <div class="wrap">
    <h1>{{ title }}</h1>
    <div class="meta">{{ date }} • {{ tags }}</div>
    <article class="md-content">{{ content | safe }}</article>
    <p style="margin-top:18px;"><a href="../lab.html">← Back to Lab Challenges</a></p>
    <footer style="color:#8b949e;margin-top:20px">© 2025 Beatrice Mutheu Mutunga</footer>
  </div>
</body>
</html>
"""

def parse_md_file(path):
    text = path.read_text(encoding='utf8')
    # attempt YAML frontmatter
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            _, fm_raw, md = parts
            fm = yaml.safe_load(fm_raw)
            return fm, md.strip()
    # fallback: no frontmatter
    return {}, text

def ensure_dirs():
    LAB_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)

def slugify(s):
    return ''.join(c if c.isalnum() or c in '-_' else '-' for c in s.lower()).strip('-')

def main():
    ensure_dirs()
    entries = []
    for md_path in sorted(LAB_DIR.glob('*.md')):
        fm, md_body = parse_md_file(md_path)
        title = fm.get('title') or md_path.stem
        date = fm.get('date','')
        slug = fm.get('slug') or slugify(md_path.stem)
        thumbnail = fm.get('thumbnail','/assets/img/default-thumb.png')
        tags = fm.get('tags','')
        excerpt = fm.get('excerpt') or (md_body[:200].replace('\n',' ') + '...')
        # convert markdown to html
        html_body = markdown.markdown(md_body, extensions=['fenced_code','codehilite','tables'])
        # write projects/<slug>.html
        out_html = Template(TEMPLATE).render(title=title, date=date, tags=tags, content=html_body)
        out_file = OUT_DIR / f'{slug}.html'
        out_file.write_text(out_html, encoding='utf8')
        entries.append({
            'title': title,
            'date': date,
            'slug': slug,
            'thumbnail': thumbnail,
            'tags': tags,
            'excerpt': excerpt,
            'file': md_path.name
        })
        print('Generated', out_file)
    # write index.json
    INDEX_FILE.write_text(json.dumps(entries, indent=2), encoding='utf8')
    print('Wrote index:', INDEX_FILE)

if __name__=='__main__':
    main()
