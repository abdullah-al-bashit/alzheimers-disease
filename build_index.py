#!/usr/bin/env python3
"""
Build script for index.html (Biography page).
Uses sidebar.py for shared components, adds page-specific CSS.

Usage:
    python build_index.py
"""

import json
from pathlib import Path
from typing import Any

from sidebar import (
    load_sidebar,
    get_base_head_html,
    get_nav_html,
    get_sidebar_html,
    get_footer_html,
    get_js_code,
    get_nav_brand,
)


# ============================================
# PAGE-SPECIFIC CSS
# ============================================

def get_index_css() -> str:
    """Return CSS specific to the index/biography page."""
    return '''
    /* ============================================
       AFFILIATIONS SECTION
       ============================================ */
    .affiliation-item {
      display: flex;
      gap: 0.5rem;
      align-items: stretch;
      margin-bottom: 0.5rem;
    }

    .affiliation-logo {
      width: 100px;
      min-height: 100px;
      flex-shrink: 0;
      background-size: contain;
      background-repeat: no-repeat;
      background-position: center;
    }

    .affiliation-logo i {
      font-size: 2.5rem;
      color: var(--text-muted);
    }

    .affiliation-info {
    }

    .affiliation-logo i {
      font-size: 1.5rem;
      color: var(--text-muted);
    }

    .affiliation-info h3 {
      font-family: 'Roboto Slab', serif;
      font-size: 1rem;
      font-weight: 700;
      color: var(--text-color);
      margin: 0;
      line-height: 1.4;
    }

    .affiliation-info p {
      margin: 0;
      font-size: 0.9rem;
      line-height: 1.4;
    }

    .affiliation-info .role {
      color: var(--text-color);
    }

    .affiliation-info .department {
      color: var(--text-muted);
    }

    /* ============================================
       DEGREES SECTION
       ============================================ */
    .degrees-list {
      list-style: disc;
      padding-left: 1.5rem;
      margin: 0;
    }

    .degrees-list li {
      margin-bottom: 0.5rem;
      font-size: 1rem;
      line-height: 1.5;
    }

    /* ============================================
       NEWS SECTION
       ============================================ */
    .news-container {
      max-height: 350px;
      overflow-y: auto;
      border: 1px solid var(--border-color);
      padding: 0.75rem 1rem;
      border-radius: 4px;
    }

    .news-list { 
      list-style: none;
      padding-left: 0;
      margin: 0;
    }

    .news-item {
      padding: 0.3rem 0;
      line-height: 1.5;
      font-size: 0.9rem;
    }

    .news-date {
      font-weight: 700;
      color: var(--text-color);
    }

    .news-date::after {
      content: ": ";
    }

    .news-content { 
      color: var(--text-color);
    }

    /* ============================================
       BIO SECTION LINKS
       ============================================ */
    .section p a {
      color: var(--action-link-color);
    }

    .section p a:hover {
      color: var(--action-link-hover);
      text-decoration: underline;
    }

    /* ============================================
       SPONSORS SECTION
       ============================================ */
    .sponsors-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 1.5rem 2.5rem;
      align-items: center;
      justify-content: flex-start;
    }

    .sponsor-logo {
      height: 40px;
      width: auto;
      max-width: 280px;
      object-fit: contain;
    }

    /* Dark mode: invert logos for visibility */
    [data-theme="dark"] .sponsor-logo {
      filter: invert(1) hue-rotate(180deg);
    }
'''


# ============================================
# CONTENT LOADING
# ============================================

def load_content(path: Path = Path("content_index.json")) -> dict[str, Any]:
    """Load page content from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================
# HTML GENERATORS
# ============================================

def generate_bio_paragraphs(bio: list[str]) -> str:
    """Generate bio paragraphs HTML."""
    return "\n        ".join(f"<p>{p}</p>" for p in bio)


def generate_affiliations(affiliations: list[dict[str, Any]]) -> str:
    """Generate affiliations HTML with logo (supports both images and icons)."""
    items = []
    for aff in affiliations:
        dept_lines = "<br>".join(aff.get("department", []))
        logo_icon = aff.get("logo_icon", "fa-university")
        
        # Check if logo_icon is an image path or a Font Awesome icon
        if logo_icon.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp')):
            logo_html = f'<div class="affiliation-logo" style="background-image: url(\'{logo_icon}\');"></div>'
        else:
            logo_html = f'<div class="affiliation-logo"><i class="fas {logo_icon}"></i></div>'
        
        item = f'''<div class="affiliation-item">
          {logo_html}
          <div class="affiliation-info">
            <h3>{aff["institution"]}</h3>
            <p class="role">{aff["role"]}</p>
            <p class="department">{dept_lines}</p>
          </div>
        </div>'''
        items.append(item)
    
    return "\n        ".join(items)


def generate_degrees(degrees: list[dict[str, str]]) -> str:
    """Generate degrees list HTML."""
    items = []
    for d in degrees:
        item = f'<li><strong>{d["degree"]}, {d["field"]},</strong> {d["institution"]}, {d["location"]}</li>'
        items.append(item)
    return "\n            ".join(items)


def generate_news(news: list[dict[str, str]]) -> str:
    """Generate news items HTML."""
    items = []
    for n in news:
        item = f'''<li class="news-item">
          <span class="news-date">{n["date"]}</span><span class="news-content">{n["content"]}</span>
        </li>'''
        items.append(item)
    
    return "\n        ".join(items)


def generate_sponsors(sponsors: list[dict[str, str]]) -> str:
    """Generate sponsors/affiliations logos HTML."""
    items = []
    for s in sponsors:
        item = f'<img src="{s["logo"]}" alt="{s["name"]}" class="sponsor-logo">'
        items.append(item)
    return "\n          ".join(items)


# ============================================
# PAGE BUILDER
# ============================================

def build_html(content: dict[str, Any], sidebar: dict[str, Any]) -> str:
    """Build complete HTML page."""
    
    # Get head HTML with page-specific CSS
    head_html = get_base_head_html(
        content["meta"]["title"],
        content["meta"]["description"],
        get_index_css()
    )
    
    html = f'''<!DOCTYPE html>
<html lang="en">
{head_html}
<body>
  <nav>
    <div class="nav-container">
      <a href="index.html" class="nav-brand">{get_nav_brand(sidebar)}</a>
      <button class="nav-toggle" aria-label="Toggle navigation">
        <i class="fas fa-bars"></i>
      </button>
      <ul class="nav-links">
        {get_nav_html("bio", sidebar)}
      </ul>
      <button class="theme-toggle" aria-label="Toggle dark mode">
        <i class="fas fa-moon"></i>
      </button>
    </div>
  </nav>

  <div class="page-wrapper">
    {get_sidebar_html(sidebar)}

    <main class="main-content">
      <section class="section">
        <h2>Biography</h2>
        {generate_bio_paragraphs(content["bio"])}
      </section>

      <section class="section">
        <h2>Current Affiliations</h2>
        {generate_affiliations(content["affiliations"])}
      </section>

      <section class="section">
        <h2>Degrees</h2>
        <ul class="degrees-list">
          {generate_degrees(content.get("degrees", []))}
        </ul>
      </section>

      <section class="section">
        <h2>News</h2>
        <div class="news-container">
          <ul class="news-list">
            {generate_news(content["news"])}
          </ul>
        </div>
      </section>

      <section class="section">
        <h2>Affiliations &amp; Sponsors</h2>
        <div class="sponsors-grid">
          {generate_sponsors(content.get("sponsors", []))}
        </div>
      </section>
    </main>
  </div>

  {get_footer_html(sidebar)}

  <script>{get_js_code()}</script>
</body>
</html>'''
    
    return html


# ============================================
# MAIN
# ============================================

def main():
    """Main build function."""
    sidebar_path = Path("sidebar.json")
    content_path = Path("content_index.json")
    output_path = Path("index.html")
    
    if not sidebar_path.exists():
        print(f"Error: {sidebar_path} not found.")
        return 1
    
    if not content_path.exists():
        print(f"Error: {content_path} not found.")
        return 1
    
    print(f"Loading sidebar from {sidebar_path}...")
    sidebar = load_sidebar(sidebar_path)
    
    print(f"Loading content from {content_path}...")
    content = load_content(content_path)
    
    print("Building index.html...")
    html = build_html(content, sidebar)
    
    print(f"Writing to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print("Done!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())