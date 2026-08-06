#!/usr/bin/env python3
"""Builds index.html from README.md. Stdlib only, no dependencies.

README.md stays the single source of truth. This script parses its fixed
section structure and renders a styled static page. Re-run whenever
README.md changes (the build-site workflow does this automatically).
"""
import re
import unicodedata
from html import escape
from pathlib import Path


def ascii_key(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^\w]+", "", normalized).lower()

ROOT = Path(__file__).resolve().parent.parent.parent
README = (ROOT / "README.md").read_text(encoding="utf-8")
SCREENSHOT_DIR = ROOT / "assets" / "screenshots"

# ---------------------------------------------------------------------------
# Inline markdown -> HTML (bold, code, links, images — this repo's README
# never uses anything richer than that inside a line)
# ---------------------------------------------------------------------------


def inline(text: str) -> str:
    text = escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# ---------------------------------------------------------------------------
# Parse README.md into sections split on horizontal rules
# ---------------------------------------------------------------------------

blocks = re.split(r"\n-{3,}\n", README.strip())
intro_block, *section_blocks = blocks

# --- Intro: name, title, contact links, bio paragraphs ---------------------
name = re.search(r"^#\s+(.+)$", intro_block, re.M).group(1).strip()
title = re.search(r"^\*\*(.+)\*\*$", intro_block, re.M).group(1).strip()

contact_links = []
for line in intro_block.splitlines():
    m = re.match(r"^([^\w\s])\s*\[([^\]]+)\]\(([^)]+)\)$", line.strip())
    if m:
        icon, label, href = m.groups()
        contact_links.append((icon, label, href))
location_m = re.search(r"^📍\s*(.+)$", intro_block, re.M)
location = location_m.group(1).strip() if location_m else ""

bio_paragraphs = [
    p.strip()
    for p in intro_block.split("\n\n")
    if p.strip()
    and not p.strip().startswith("#")
    and not p.strip().startswith("**")
    and not re.match(r"^[^\w\s]", p.strip())
]

# --- Generic section parser --------------------------------------------------


def parse_section(block: str):
    heading = re.search(r"^##\s+(.+)$", block, re.M)
    heading_text = heading.group(1).strip() if heading else ""
    body = block[heading.end() :].strip() if heading else block.strip()
    return heading_text, body


sections = {}
projects_body = ""
for block in section_blocks:
    heading_text, body = parse_section(block)
    key = ascii_key(heading_text)
    if "proyectos" in key and "destacado" not in key:
        projects_body = body
    else:
        sections[key] = (heading_text, body)


def bullet_items(body: str):
    return [
        line[2:].strip()
        for line in body.splitlines()
        if line.strip().startswith("- ")
    ]


# --- Actividad reciente ------------------------------------------------------
actividad_heading, actividad_body = sections.get("actividadreciente", ("", ""))
actividad_body_clean = re.sub(r"<!--.*?-->", "", actividad_body, flags=re.S)
actividad_items = bullet_items(actividad_body_clean)
contribution_graph_m = re.search(r"^!\[[^\]]*\]\([^)]+\)", actividad_body_clean, re.M)
contribution_graph_line = contribution_graph_m.group(0) if contribution_graph_m else ""

# --- Proyecto destacado -----------------------------------------------------
_, destacado_body = sections.get("proyectodestacado", ("", ""))
destacado_lines = [l for l in destacado_body.splitlines() if l.strip()]
destacado_intro = destacado_lines[0] if destacado_lines else ""
destacado_bullets = bullet_items(destacado_body)

# --- Proyectos (categorized) ------------------------------------------------
categories = []
current_cat = None
for line in projects_body.splitlines():
    cat_m = re.match(r"^###\s+(.+)$", line)
    item_m = re.match(r"^- \*\*\[([^\]]+)\]\(([^)]+)\)\*\*\s*—\s*(.+)$", line)
    if cat_m:
        current_cat = {"name": cat_m.group(1).strip(), "projects": []}
        categories.append(current_cat)
    elif item_m and current_cat is not None:
        pname, purl, pdesc = item_m.groups()
        # Optional trailing " · [Demo](url)" becomes a separate card action
        demo_m = re.search(r"\s*·\s*\[Demo\]\(([^)]+)\)\s*$", pdesc)
        demo_url = demo_m.group(1) if demo_m else ""
        if demo_m:
            pdesc = pdesc[: demo_m.start()].rstrip()
        current_cat["projects"].append(
            {
                "name": pname,
                "url": purl,
                "desc": pdesc,
                "demo": demo_url,
                "slug": slugify(pname),
            }
        )

# --- Stack --------------------------------------------------------------------
_, stack_body = sections.get("stack", ("", ""))
stack_items = re.findall(r"`([^`]+)`", stack_body)

# --- Footer note (CV refresh instructions) ----------------------------------
footer_note = ""
if blocks:
    tail = blocks[-1].strip()
    if tail.startswith("<sub>"):
        footer_note = re.sub(r"</?sub>", "", tail).strip()

# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

bio_html = "\n".join(f"<p>{inline(p)}</p>" for p in bio_paragraphs)
contact_html = " &middot; ".join(
    f'<a href="{href}">{icon} {escape(label)}</a>' for icon, label, href in contact_links
)
location_html = f" &middot; 📍 {escape(location)}" if location else ""

activity_html = (
    "\n".join(f"<li>{inline(item)}</li>" for item in actividad_items)
    or "<li><em>Sin actividad pública reciente.</em></li>"
)
contribution_graph_html = (
    f'<div class="contribution-graph">{inline(contribution_graph_line)}</div>'
    if contribution_graph_line
    else ""
)

destacado_bullets_html = "\n".join(
    f"<li>{inline(b)}</li>" for b in destacado_bullets
)

# Simple inline SVG diagram for the flagship (private, no screenshot possible)
FLAGSHIP_DIAGRAM = """
<svg viewBox="0 0 400 160" class="flagship-diagram" role="img" aria-label="Diagrama de arquitectura de meta-projects">
  <g class="node"><rect x="10" y="10" width="170" height="55" rx="8"/><text x="95" y="32">Framework agéntico</text><text x="95" y="50">multicapa</text></g>
  <g class="node"><rect x="220" y="10" width="170" height="55" rx="8"/><text x="305" y="32">Orquestación</text><text x="305" y="50">en dos etapas</text></g>
  <g class="node"><rect x="10" y="95" width="170" height="55" rx="8"/><text x="95" y="117">Guardrails de</text><text x="95" y="135">seguridad</text></g>
  <g class="node"><rect x="220" y="95" width="170" height="55" rx="8"/><text x="305" y="117">Gobernanza de</text><text x="305" y="135">estándares</text></g>
  <line x1="180" y1="37" x2="220" y2="37" class="edge"/>
  <line x1="95" y1="65" x2="95" y2="95" class="edge"/>
  <line x1="305" y1="65" x2="305" y2="95" class="edge"/>
  <line x1="180" y1="122" x2="220" y2="122" class="edge"/>
</svg>
"""

FALLBACK_ICONS = {
    "agentic-evals": "🧪",
    "reel-forge-ts": "🎬",
    "translate-and-teach": "🗣️",
    "ollama-open-webui": "🦙",
    "btc-predictor": "₿",
    "avocadodash": "🥑",
    "homicides-rate-visualizer": "📉",
    "judicial-candidates-mx": "⚖️",
    "dockyard2sail-py": "🐍",
    "dockyard2sail-ts": "🚢",
    "diplomado-ciencia-datos": "🎓",
}


def project_visual(slug: str, name: str) -> str:
    img_path = SCREENSHOT_DIR / f"{slug}.png"
    if img_path.exists():
        return f'<img class="project-thumb" src="assets/screenshots/{slug}.png" alt="Screenshot de {escape(name)}" loading="lazy">'
    icon = FALLBACK_ICONS.get(slug, "📦")
    return f'<div class="project-thumb project-thumb--fallback" aria-hidden="true"><span>{icon}</span></div>'


category_html_parts = []
for cat in categories:
    cards = []
    for p in cat["projects"]:
        demo_action = (
            f'<a class="project-action project-action--demo" href="{p["demo"]}">Demo ↗</a>'
            if p["demo"]
            else ""
        )
        cards.append(
            f"""
            <article class="project-card">
              {project_visual(p['slug'], p['name'])}
              <div class="project-card__body">
                <h4><a href="{p['url']}">{escape(p['name'])}</a></h4>
                <p>{inline(p['desc'])}</p>
                <div class="project-card__actions"><a class="project-action" href="{p['url']}">Código</a>{demo_action}</div>
              </div>
            </article>"""
        )
    category_html_parts.append(
        f"""
        <div class="category">
          <h3>{escape(cat['name'])}</h3>
          <div class="project-grid">{''.join(cards)}</div>
        </div>"""
    )
categories_html = "\n".join(category_html_parts)

stack_html = " ".join(f'<span class="badge">{escape(s)}</span>' for s in stack_items)

bio_first_line = bio_paragraphs[0] if bio_paragraphs else ""
meta_description = re.sub(r"\s+", " ", re.sub(r"[*_`\[\]()]", "", bio_first_line)).strip()
page_title = f"{name} — {title.split('—')[0].strip()}"

HTML = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(page_title)}</title>
<meta name="description" content="{escape(meta_description)}">
<link rel="canonical" href="https://cuauhtemocbe.github.io/">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">

<meta property="og:type" content="website">
<meta property="og:url" content="https://cuauhtemocbe.github.io/">
<meta property="og:title" content="{escape(page_title)}">
<meta property="og:description" content="{escape(meta_description)}">
<meta property="og:image" content="https://cuauhtemocbe.github.io/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(page_title)}">
<meta name="twitter:description" content="{escape(meta_description)}">
<meta name="twitter:image" content="https://cuauhtemocbe.github.io/assets/og-image.jpg">

<style>
:root {{
  --bg: #ffffff; --bg-alt: #f5f6f8; --text: #1c1f24; --text-dim: #565d68;
  --accent: #2a6df5; --border: #e3e6ea; --code-bg: #eef1f5;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #0f1216; --bg-alt: #171b21; --text: #e8eaed; --text-dim: #9aa3af;
    --accent: #6ea8ff; --border: #2a2f37; --code-bg: #1d2229;
  }}
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--bg); color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.55;
}}
main {{ max-width: 780px; margin: 0 auto; padding: 2.5rem 1.25rem 4rem; }}
h1 {{ font-size: 1.9rem; margin: 0 0 0.25rem; }}
h2 {{ font-size: 1.3rem; border-bottom: 1px solid var(--border); padding-bottom: 0.4rem; margin-top: 2.5rem; }}
h3 {{ font-size: 1.05rem; margin-bottom: 0.75rem; }}
h4 {{ margin: 0 0 0.25rem; font-size: 0.98rem; }}
p {{ color: var(--text-dim); }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
code {{ background: var(--code-bg); padding: 0.1rem 0.35rem; border-radius: 4px; font-size: 0.85em; }}
.subtitle {{ color: var(--text-dim); font-weight: 600; margin: 0 0 1rem; }}
.contact {{ margin-bottom: 1.25rem; font-size: 0.95rem; }}
.contact a {{ color: var(--text); }}
ul {{ padding-left: 1.1rem; color: var(--text-dim); }}
li {{ margin-bottom: 0.4rem; }}
.contribution-graph {{ background: #f5f6f8; border-radius: 10px; padding: 0.75rem; margin-bottom: 1rem; overflow-x: auto; }}
.contribution-graph img {{ display: block; min-width: 640px; }}
.activity-list {{ list-style: none; padding: 0; }}
.activity-list li {{ padding: 0.5rem 0.75rem; background: var(--bg-alt); border-radius: 8px; margin-bottom: 0.5rem; font-size: 0.92rem; }}
.project-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.9rem; margin-bottom: 1.5rem; }}
.project-card {{ display: flex; flex-direction: column; border: 1px solid var(--border); border-radius: 10px; overflow: hidden; background: var(--bg-alt); }}
.project-card:hover {{ border-color: var(--accent); }}
.project-thumb {{ width: 100%; height: 110px; object-fit: cover; display: block; background: var(--code-bg); }}
.project-thumb--fallback {{ display: flex; align-items: center; justify-content: center; font-size: 2.2rem; }}
.project-card__body {{ padding: 0.75rem 0.9rem; display: flex; flex-direction: column; flex: 1; }}
.project-card__body p {{ font-size: 0.85rem; margin: 0; }}
.project-card__actions {{ display: flex; gap: 0.4rem; margin-top: auto; padding-top: 0.7rem; }}
.project-action {{ border: 1px solid var(--border); border-radius: 6px; padding: 0.2rem 0.6rem; font-size: 0.8rem; color: var(--text-dim); background: var(--bg); }}
.project-action:hover {{ border-color: var(--accent); color: var(--accent); text-decoration: none; }}
.project-action--demo {{ border-color: var(--accent); color: var(--accent); }}
.badge {{ display: inline-block; background: var(--code-bg); border-radius: 6px; padding: 0.2rem 0.6rem; margin: 0.15rem; font-size: 0.85rem; }}
.flagship-diagram {{ width: 100%; max-width: 420px; height: auto; margin: 1rem 0; }}
.flagship-diagram rect {{ fill: var(--code-bg); stroke: var(--border); }}
.flagship-diagram text {{ fill: var(--text); font-size: 11px; text-anchor: middle; font-family: inherit; }}
.flagship-diagram .edge {{ stroke: var(--accent); stroke-width: 2; }}
footer {{ margin-top: 3rem; font-size: 0.8rem; color: var(--text-dim); }}
</style>
</head>
<body>
<main>
  <h1>{escape(name)}</h1>
  <p class="subtitle">{inline(title)}</p>
  <p class="contact">{contact_html}{location_html}</p>
  {bio_html}

  <h2>Proyectos</h2>
  {categories_html}

  <h2>Proyecto destacado</h2>
  <p>{inline(destacado_intro)}</p>
  {FLAGSHIP_DIAGRAM}
  <ul>{destacado_bullets_html}</ul>

  <h2>🔭 Actividad reciente</h2>
  {contribution_graph_html}
  <ul class="activity-list">{activity_html}</ul>

  <h2>Stack</h2>
  <p>{stack_html}</p>

  <footer>{inline(footer_note) + "<br>" if footer_note else ""}Generado automáticamente desde README.md — no editar index.html a mano.</footer>
</main>
</body>
</html>
"""

(ROOT / "index.html").write_text(HTML, encoding="utf-8")
print("index.html generated from README.md")
