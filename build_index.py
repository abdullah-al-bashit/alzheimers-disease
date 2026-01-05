#!/usr/bin/env python3
"""
Build script for index.html (Bio page).
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
    """Return CSS specific to the index/bio page."""
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
       EXPERIENCE SECTION
       ============================================ */
    .experience-item {
      display: flex;
      gap: 1rem;
      padding: 1rem 0;
      border-bottom: 1px solid var(--border-color);
    }

    .experience-item:last-child { border-bottom: none; }

    .experience-logo {
      width: 45px;
      height: 45px;
      border-radius: 4px;
      background: transparent;
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .experience-logo i {
      font-size: 1.2rem;
      color: var(--text-muted);
    }

    .experience-content h3 {
      font-family: 'Roboto Slab', serif;
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-color);
      margin: 0 0 0.15rem 0;
    }

    .experience-content p {
      margin: 0;
    }

    .experience-content .position {
      color: var(--link-color);
      font-size: 0.85rem;
    }

    .experience-content .dates {
      color: var(--text-muted);
      font-size: 0.8rem;
      margin-top: 0.15rem;
    }

    .experience-content .department {
      color: var(--text-muted);
      font-size: 0.8rem;
    }

    /* ============================================
       NEWS SECTION
       ============================================ */
    .news-container {
      max-height: 200px;
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


def generate_logo_html(item: dict[str, Any]) -> str:
    """Generate logo HTML (icon or image)."""
    if item.get("logo_image"):
        return f'<img src="{item["logo_image"]}" alt="{item["institution"]}">'
    icon = item.get("logo_icon", "fa-university")
    return f'<i class="fas {icon}"></i>'


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


def generate_experience(experience: list[dict[str, Any]]) -> str:
    """Generate experience items HTML."""
    items = []
    for exp in experience:
        item = f'''<div class="experience-item">
        <div class="experience-logo">
          {generate_logo_html(exp)}
        </div>
        <div class="experience-content">
          <h3>{exp["institution"]}</h3>
          <p class="position">{exp["position"]}</p>
          <p class="dates">{exp["dates"]}</p>
          <p class="department">{exp["department"]}</p>
        </div>
      </div>'''
        items.append(item)
    
    return "\n      ".join(items)


def generate_news(news: list[dict[str, str]]) -> str:
    """Generate news items HTML."""
    items = []
    for n in news:
        item = f'''<li class="news-item">
          <span class="news-date">{n["date"]}</span><span class="news-content">{n["content"]}</span>
        </li>'''
        items.append(item)
    
    return "\n        ".join(items)


# ============================================
# PAGE BUILDER
# ============================================

def build_html(content: dict[str, Any], sidebar: dict[str, Any]) -> str:
    """Build complete HTML page."""
    
    # Get head HTML with page-specific CSS
    head_html = get_base_head_html(
        content["meta"]["title"],
        content["meta"]["description"],
        get_index_css(),
        sidebar
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
        <h2>Bio</h2>
        {generate_bio_paragraphs(content["bio"])}
      </section>

      <section class="section">
        <h2>Current Affiliations</h2>
        {generate_affiliations(content["affiliations"])}
      </section>

      <section class="section">
        <h2>News</h2>
        <div class="news-container">
          <ul class="news-list">
            {generate_news(content["news"])}
          </ul>
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