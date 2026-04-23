#!/usr/bin/env python3
"""
Sidebar module for academic portfolio website.
Contains only shared components: navigation bar, left sidebar, footer.

Page-specific CSS should be added by individual build scripts.

Usage:
    from sidebar import (
        load_sidebar,
        get_base_head_html,
        get_nav_html,
        get_sidebar_html,
        get_footer_html,
        get_js_code,
        get_nav_brand,
    )
"""

import json
from pathlib import Path
from typing import Any


def load_sidebar(path: Path = Path("sidebar.json")) -> dict[str, Any]:
    """Load sidebar configuration from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _generate_profile_image(profile: dict[str, str]) -> str:
    """Generate HTML for profile image or fallback icon."""
    if profile.get("image"):
        return f'<img src="{profile["image"]}" alt="{profile["name"]}">'
    return '<i class="fas fa-user"></i>'


def _generate_sidebar_links(links: list[dict[str, Any]]) -> str:
    """Generate sidebar links (vertical list with icons)."""
    items = []
    for link in links:
        icon = link.get("icon", "fas fa-link")
        label = link.get("label", "")
        url = link.get("url")
        
        if url:
            items.append(
                f'<li><a href="{url}" target="_blank" rel="noopener">'
                f'<i class="{icon}" aria-hidden="true"></i> {label}</a></li>'
            )
        else:
            items.append(
                f'<li><i class="{icon}" aria-hidden="true"></i> {label}</li>'
            )
    
    return "\n          ".join(items)


def get_nav_brand(sidebar: dict[str, Any]) -> str:
    """Get navigation brand name."""
    return sidebar["nav_brand"]


def get_sidebar_html(sidebar: dict[str, Any]) -> str:
    """Generate left sidebar HTML."""
    profile = sidebar["profile"]
    links = sidebar.get("sidebar_links", [])
    
    bio_html = ""
    if profile.get("bio_lines"):
        bio_items = "".join(f'<span class="bio-line">{line}</span>' for line in profile["bio_lines"])
        bio_html = f'<div class="author__bio">{bio_items}</div>'
    elif profile.get("bio"):
        bio_html = f'<p class="author__bio">{profile["bio"]}</p>'
    
    return f'''<aside class="sidebar">
      <div class="sidebar-content">
        <div class="author__avatar">
          {_generate_profile_image(profile)}
        </div>
        <div class="author__content">
          <h3 class="author__name">{profile["name"]}</h3>
          {bio_html}
        </div>
        <div class="author__urls-wrapper">
          <ul class="author__urls">
            {_generate_sidebar_links(links)}
          </ul>
        </div>
      </div>
    </aside>'''


def get_footer_html(sidebar: dict[str, Any]) -> str:
    """Generate footer HTML."""
    footer = sidebar["footer"]
    return f'''<footer>
    <p class="footer-text">
      © {footer["copyright_year"]} {footer["copyright_name"]}.
    </p>
  </footer>'''


def get_nav_html(active_page: str = "bio", sidebar: dict = None) -> str:
    """Generate navigation links with active page highlighted."""
    cv_file = sidebar.get("cv_file", "cv.pdf") if sidebar else "cv.pdf"
    
    pages = [
        ("bio", "index.html", "Biography", False),
        ("research", "research.html", "Research", False),
        ("publications", "publications.html", "Publications", False),
        ("teaching", "teaching.html", "Teaching", False),
        ("cv", cv_file, "CV", True),
    ]
    
    links = []
    for page_id, href, label, new_tab in pages:
        active_class = ' class="active"' if page_id == active_page else ""
        target = ' target="_blank" rel="noopener"' if new_tab else ""
        links.append(f'<li><a href="{href}"{active_class}{target}>{label}</a></li>')
    
    return "\n        ".join(links)


def get_base_css(sidebar: dict[str, Any] = None) -> str:
    """
    Return base CSS for navigation, sidebar, footer, and layout.
    Page-specific CSS should be added by individual build scripts.
    
    Args:
        sidebar: Optional sidebar configuration with theme colors.
    """
    # Get theme colors from sidebar config, or use defaults
    if sidebar and "theme" in sidebar:
        light = sidebar["theme"].get("light", {})
        dark = sidebar["theme"].get("dark", {})
    else:
        light = {}
        dark = {}
    
    # Light mode colors (defaults if not specified)
    accent_light = light.get("accent_color", "#0D9488")
    accent_hover_light = light.get("accent_hover", "#0F766E")
    link_color_light = light.get("link_color", "#0066cc")
    link_hover_light = light.get("link_hover", "#004499")
    
    # Dark mode colors (defaults if not specified)
    accent_dark = dark.get("accent_color", "#2DD4BF")
    accent_hover_dark = dark.get("accent_hover", "#5EEAD4")
    link_color_dark = dark.get("link_color", "#60A5FA")
    link_hover_dark = dark.get("link_hover", "#93C5FD")
    
    return f'''
    /* ============================================
       CSS VARIABLES
       ============================================ */
    :root {{
      --primary-color: #494e52;
      --link-color: #494e52;
      --link-hover: #000000;
      --text-color: #494e52;
      --text-muted: #494e52;
      --bg-color: #ffffff;
      --bg-sidebar: #ffffff;
      --border-color: #e0e0e0;
      --shadow: 0 1px 1px rgba(0,0,0,0.125);
      --sidebar-width: 260px;
      --nav-height: 50px;
      --accent-color: {accent_light};
      --accent-hover: {accent_hover_light};
      --action-link-color: {link_color_light};
      --action-link-hover: {link_hover_light};
    }}

    /* ============================================
       BASE STYLES
       ============================================ */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 16px;
      line-height: 1.6;
      color: var(--text-color);
      background-color: var(--bg-color);
    }}

    a {{ color: var(--link-color); text-decoration: none; transition: color 0.2s ease; }}
    a:hover {{ color: var(--link-hover); text-decoration: underline; }}

    /* ============================================
       NAVIGATION BAR
       ============================================ */
    nav {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: var(--nav-height);
      background: var(--bg-color);
      border-bottom: 1px solid var(--border-color);
      z-index: 1000;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .nav-container {{
      width: 100%;
      max-width: 1400px;
      padding: 0 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .nav-brand {{
      font-family: 'Roboto Slab', serif;
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-color);
      letter-spacing: -0.5px;
    }}
    .nav-brand:hover {{ text-decoration: none; color: var(--link-color); }}

    .nav-links {{ display: flex; gap: 1.5rem; list-style: none; }}
    .nav-links a {{ 
      color: var(--text-muted); 
      font-size: 0.85rem; 
      font-weight: 400; 
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .nav-links a:hover, .nav-links a.active {{ color: var(--text-color); text-decoration: none; }}

    .nav-toggle {{
      display: none;
      background: none;
      border: none;
      font-size: 1.25rem;
      cursor: pointer;
      color: var(--text-color);
    }}

    .theme-toggle {{
      background: none;
      border: none;
      cursor: pointer;
      font-size: 1rem;
      color: var(--text-muted);
      padding: 0.4rem;
      border-radius: 50%;
    }}
    .theme-toggle:hover {{ color: var(--text-color); }}

    /* ============================================
       PAGE LAYOUT
       ============================================ */
    .page-wrapper {{
      display: flex;
      margin-top: var(--nav-height);
      min-height: calc(100vh - var(--nav-height));
      max-width: 1400px;
      margin-left: auto;
      margin-right: auto;
    }}

    /* ============================================
       LEFT SIDEBAR
       ============================================ */
    .sidebar {{
      width: var(--sidebar-width);
      flex-shrink: 0;
      background: var(--bg-color);
      border-right: 1px solid var(--border-color);
    }}

    .sidebar-content {{
      position: sticky;
      top: calc(var(--nav-height) + 1rem);
      padding: 1.5rem 1rem;
    }}

    .author__avatar {{
      display: block;
      width: 180px;
      height: 180px;
      margin: 0 0 0.75rem 0;
    }}

    .author__avatar img {{
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
      border: 1px solid var(--border-color);
      padding: 3px;
      background: var(--bg-color);
    }}

    .author__content {{
      text-align: left;
      margin-bottom: 1rem;
    }}

    .author__name {{
      font-family: 'Roboto Slab', serif;
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-color);
      margin-bottom: 0.25rem;
    }}

    .author__bio {{
      font-size: 0.85rem;
      color: var(--text-color);
      line-height: 1.5;
    }}

    .author__bio .bio-line {{
      display: block;
      margin-bottom: 0;
    }}

    .author__urls-wrapper {{ margin-top: 1rem; }}

    .author__urls {{
      list-style: none;
      font-size: 0.8rem;
    }}

    .author__urls li {{
      white-space: nowrap;
      padding: 0.2rem 0;
      color: var(--text-muted);
    }}

    .author__urls li i {{
      width: 1.25em;
      text-align: center;
      margin-right: 0.4rem;
      color: var(--text-muted);
    }}

    .author__urls a {{ color: var(--text-color); }}
    .author__urls a:hover {{ color: var(--link-color); text-decoration: underline; }}
    .author__urls a i {{ color: var(--text-muted); }}

    /* ============================================
       MAIN CONTENT AREA
       ============================================ */
    .main-content {{
      flex: 1;
      padding: 2rem 3rem 2rem 2.5rem;
    }}

    /* Section headings */
    .main-content h2 {{
      font-family: 'Roboto Slab', serif;
      font-size: 1.4rem;
      font-weight: 700;
      color: var(--text-color);
      margin-bottom: 0.6rem;
      padding-bottom: 0.4rem;
      border-bottom: 1px solid var(--border-color);
    }}

    /* Section container */
    .section {{ margin-bottom: 2rem; }}

    /* Default paragraph styling for sections */
    .section > p {{
      color: var(--text-color);
      margin-bottom: 1.25rem;
      text-align: justify;
      font-size: 1.05rem;
      line-height: 1.7;
    }}

    /* ============================================
       FOOTER
       ============================================ */
    footer {{
      padding: 1.25rem 1.5rem;
      background: var(--bg-color);
      border-top: 1px solid var(--border-color);
      text-align: center;
    }}

    .footer-text {{ color: var(--text-muted); font-size: 0.8rem; }}
    .footer-text a {{ color: var(--text-muted); }}

    /* ============================================
       DARK MODE
       ============================================ */
    [data-theme="dark"] {{
      --primary-color: #e2e2e2;
      --link-color: #e2e2e2;
      --link-hover: #ffffff;
      --text-color: #e2e2e2;
      --text-muted: #e2e2e2;
      --bg-color: #252a34;
      --bg-sidebar: #252a34;
      --border-color: #3a3f4b;
      --accent-color: {accent_dark};
      --accent-hover: {accent_hover_dark};
      --action-link-color: {link_color_dark};
      --action-link-hover: {link_hover_dark};
    }}

    /* ============================================
       RESPONSIVE - TABLET (<=900px)
       ============================================ */
    @media (max-width: 900px) {{
      .page-wrapper {{ flex-direction: column; }}

      .sidebar {{
        width: 100%;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
      }}

      .sidebar-content {{
        position: static;
        padding: 1.25rem;
        display: flex;
        flex-direction: column;
        align-items: center;
      }}

      .author__avatar {{ width: 100px; height: 100px; }}

      .author__urls {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem 1rem;
      }}

      .main-content {{ padding: 1.5rem; max-width: 100%; }}
    }}

    /* ============================================
       RESPONSIVE - MOBILE (<=768px)
       ============================================ */
    @media (max-width: 768px) {{
      .nav-links {{
        display: none;
        position: absolute;
        top: var(--nav-height);
        left: 0;
        right: 0;
        background: var(--bg-color);
        flex-direction: column;
        padding: 1rem 1.5rem;
        gap: 0.75rem;
        border-bottom: 1px solid var(--border-color);
        box-shadow: var(--shadow);
      }}
      .nav-links.active {{ display: flex; }}
      .nav-toggle {{ display: block; }}
    }}
'''


def get_base_head_html(title: str, description: str, page_css: str = "", sidebar: dict[str, Any] = None) -> str:
    """
    Generate HTML head with base CSS and optional page-specific CSS.
    
    Args:
        title: Page title
        description: Meta description
        page_css: Additional CSS for this specific page
        sidebar: Optional sidebar configuration for theme colors
    """
    return f'''<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{description}">
  <title>{title}</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Slab:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/jpswalsh/academicons@1/css/academicons.min.css">
  
  <style>
{get_base_css(sidebar)}
{page_css}
  </style>
</head>'''


def get_js_code() -> str:
    """Return shared JavaScript for navigation and theme toggle."""
    return '''
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    navToggle.addEventListener('click', () => navLinks.classList.toggle('active'));

    const themeToggle = document.querySelector('.theme-toggle');
    const themeIcon = themeToggle.querySelector('i');
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    themeIcon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';

    themeToggle.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      themeIcon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => navLinks.classList.remove('active'));
    });
'''


# Backward compatibility
def get_head_html(title: str, description: str, sidebar: dict[str, Any] = None) -> str:
    """Backward compatibility wrapper."""
    return get_base_head_html(title, description, sidebar=sidebar)
