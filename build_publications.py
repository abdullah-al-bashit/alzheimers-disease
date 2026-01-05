#!/usr/bin/env python3
"""
Build script for publications.html page.
Uses sidebar.py module for shared components.

This script generates the publications page for the academic portfolio,
displaying papers grouped by year with thumbnails and action links.

Usage:
    python build_publications.py

Required files:
    - sidebar.json: Profile, links, and footer configuration
    - content_publications.json: Publications data grouped by year
    - sidebar.py: Shared module with CSS and HTML generation functions

Output:
    - publications.html: Complete HTML page ready for deployment
"""

# ============================================
# IMPORTS
# ============================================

# Standard library imports
import json  # For parsing JSON configuration files
from pathlib import Path  # For cross-platform file path handling
from typing import Any  # For type hints with generic dictionaries

# Local module imports - shared components from sidebar.py
from sidebar import (
    load_sidebar,       # Load sidebar.json configuration
    get_head_html,      # Generate <head> section with CSS
    get_nav_html,       # Generate navigation links
    get_sidebar_html,   # Generate left sidebar HTML
    get_footer_html,    # Generate footer HTML
    get_js_code,        # Generate JavaScript code
    get_nav_brand,      # Get brand name for navigation
)


# ============================================
# CONTENT LOADING FUNCTIONS
# ============================================

def load_content(path: Path = Path("content_publications.json")) -> dict[str, Any]:
    """
    Load publications content from JSON file.
    
    Args:
        path: Path to the content JSON configuration file.
              Defaults to "content_publications.json" in current directory.
    
    Returns:
        Dictionary containing publications data including:
        - meta: Page title and description
        - intro: Introduction text and external links
        - publications: List of year groups with papers
    """
    # Open file with UTF-8 encoding for international character support
    with open(path, "r", encoding="utf-8") as f:
        # Parse JSON and return as dictionary
        return json.load(f)


# ============================================
# HTML GENERATION FUNCTIONS
# ============================================

def generate_intro_links(links: list[dict[str, str]]) -> str:
    """
    Generate introduction links (Google Scholar, Semantic Scholar, etc.).
    
    Args:
        links: List of link dictionaries containing:
               - label: Display text for the link
               - url: URL to link to
    
    Returns:
        HTML string with formatted links.
    """
    # Create list of formatted link elements
    link_elements = []
    
    # Iterate through each link
    for link in links:
        # Create link with brackets around label
        link_elements.append(
            f'<a href="{link["url"]}" target="_blank" rel="noopener">[{link["label"]}]</a>'
        )
    
    # Join links with " / " separator
    return " / ".join(link_elements)


def generate_paper_links(links: list[dict[str, str]]) -> str:
    """
    Generate action links for a paper (abstract, link, bibtex, etc.).
    
    Args:
        links: List of link dictionaries containing:
               - label: Link text (e.g., "abstract", "bibtex", "pdf")
               - url: URL or anchor to link to
    
    Returns:
        HTML string with pipe-separated links.
    """
    # Create list of formatted link elements
    link_elements = []
    
    # Iterate through each link
    for link in links:
        # Create link with brackets around label, opens in new tab
        link_elements.append(
            f'<a href="{link["url"]}" class="paper-link" target="_blank" rel="noopener">[{link["label"]}]</a>'
        )
    
    # Join links with " | " separator (pipe)
    return " | ".join(link_elements)


def generate_paper_html(paper: dict[str, Any], show_image: bool = True) -> str:
    """
    Generate HTML for a single paper entry.
    
    Creates structured HTML showing:
    - Thumbnail image on the left (optional)
    - Title, authors, venue, and action links on the right
    
    Args:
        paper: Dictionary containing paper data:
               - title: Paper title
               - authors: Author string
               - venue: Publication venue
               - image: Path to thumbnail image
               - links: List of action links
               - abstract: Optional abstract text
        show_image: Whether to display thumbnail image (default True)
    
    Returns:
        HTML string for the paper entry.
    """
    # Get authors string
    authors = paper.get("authors", "")
    
    # Generate action links HTML
    links_html = generate_paper_links(paper.get("links", []))
    
    if show_image:
        # Get thumbnail image path, use placeholder if not provided
        image = paper.get("image", "assets/img/pub_placeholder.png")
        
        # Build paper entry HTML structure with image
        html = f'''<div class="paper-item">
          <div class="paper-image">
            <img src="{image}" alt="{paper["title"]}">
          </div>
          <div class="paper-content">
            <h3 class="paper-title">{paper["title"]}</h3>
            <p class="paper-authors">{authors}</p>
            <p class="paper-venue">{paper["venue"]}</p>
            <div class="paper-links">
              {links_html}
            </div>
          </div>
        </div>'''
    else:
        # Build paper entry HTML structure without image
        html = f'''<div class="paper-item no-image">
          <div class="paper-content">
            <h3 class="paper-title">{paper["title"]}</h3>
            <p class="paper-authors">{authors}</p>
            <p class="paper-venue">{paper["venue"]}</p>
            <div class="paper-links">
              {links_html}
            </div>
          </div>
        </div>'''
    
    return html


def generate_year_section(year_group: dict[str, Any], show_image: bool = True) -> str:
    """
    Generate HTML for a year section containing multiple papers.
    
    Args:
        year_group: Dictionary containing:
                   - year: Year label (e.g., "2024", "2021 & Earlier") - OPTIONAL
                   - papers: List of paper dictionaries
        show_image: Whether to display thumbnail images (default True)
    
    Returns:
        HTML string for the year section.
    """
    # Get year label (optional)
    year = year_group.get("year", None)
    
    # Generate HTML for each paper in this year
    papers_html = "\n        ".join(
        generate_paper_html(paper, show_image=show_image) 
        for paper in year_group["papers"]
    )
    
    # Build year section HTML structure
    if year:
        # With year heading
        html = f'''<div class="year-section">
        <h2 class="year-heading">{year}</h2>
        {papers_html}
      </div>'''
    else:
        # Without year heading
        html = f'''<div class="year-section no-year">
        {papers_html}
      </div>'''
    
    return html


def generate_publications_html(publications: list[dict[str, Any]]) -> str:
    """
    Generate HTML for all publication year sections.
    
    Args:
        publications: List of year group dictionaries.
    
    Returns:
        HTML string with all year sections.
    """
    # Generate HTML for each year section
    sections = []
    
    for year_group in publications:
        sections.append(generate_year_section(year_group))
    
    # Join all sections with newlines
    return "\n      ".join(sections)


def generate_conference_abstracts_html(abstracts: list[dict[str, Any]]) -> str:
    """
    Generate HTML for conference abstracts section.
    
    Args:
        abstracts: List of year group dictionaries for conference abstracts.
    
    Returns:
        HTML string with conference abstracts sections.
    """
    if not abstracts:
        return ""
    
    # Generate HTML for each year section (no images for abstracts)
    sections = []
    
    for year_group in abstracts:
        sections.append(generate_year_section(year_group, show_image=False))
    
    # Join all sections with newlines
    return "\n      ".join(sections)


def get_publications_css() -> str:
    """
    Generate additional CSS specific to publications page.
    
    Returns:
        CSS string for publications styling.
    """
    return '''
    /* ============================================
       PUBLICATIONS PAGE STYLES
       Styles specific to the publications listing
       ============================================ */
    
    /* Section divider for Conference Abstracts */
    .section-divider {
      margin-top: 0.75rem;               /* Space above */
      margin-bottom: 0.3rem;             /* Space below */
    }
    
    /* Section title (Conference Abstracts) */
    .section-title {
      font-family: 'Roboto Slab', serif;  /* Serif font */
      font-size: 1.3rem;                 /* Heading size */
      font-weight: 700;                  /* Bold */
      color: var(--text-color);          /* Text color */
      margin-bottom: 0.15rem;            /* Space below */
    }

    /* Page introduction section */
    .pub-intro {
      margin-bottom: 0.75rem;          /* Space below intro */
    }
    
    /* Introduction title */
    .pub-intro h1 {
      font-family: 'Roboto Slab', serif;  /* Serif font */
      font-size: 1.4rem;               /* Heading */
      font-weight: 700;                /* Bold */
      color: var(--text-color);        /* Text color */
      margin-bottom: 0.2rem;           /* Space below */
    }
    
    /* Introduction description and links */
    .pub-intro p {
      color: var(--text-color);        /* Text color */
      font-size: 0.9rem;               /* Smaller */
      margin-bottom: 0;                /* No bottom margin */
    }
    
    .pub-intro a {
      color: var(--text-color);        /* Link color */
      font-weight: 500;                /* Medium weight */
    }
    
    .pub-intro a:hover {
      text-decoration: underline;      /* Underline on hover */
    }

    /* Year section container */
    .year-section {
      margin-bottom: 1rem;             /* Space between year sections */
    }
    
    /* Year heading */
    .year-heading {
      font-family: 'Roboto Slab', serif;  /* Serif font */
      font-size: 1.2rem;               /* Heading size */
      font-weight: 700;                /* Bold */
      color: var(--text-color);        /* Text color */
      margin-bottom: 0.2rem;           /* Space from ruler to content */
      padding-bottom: 0.1rem;          /* Space from text to ruler */
      border-bottom: 1px solid var(--border-color);  /* Underline border */
    }
    
    /* Year section without year heading */
    .year-section.no-year {
      margin-top: 0.5rem;              /* Slight top margin */
    }

    /* Individual paper item */
    .paper-item {
      display: flex;                   /* Flexbox for image + content layout */
      gap: 0.75rem;                    /* Space between image and content */
      padding: 0.4rem 0;               /* Vertical padding */
    }
    
    /* Paper item without image */
    .paper-item.no-image {
      gap: 0;                          /* No gap needed */
      padding: 0.3rem 0;               /* Slightly less padding for abstracts */
    }
    
    /* Last paper in section */
    .paper-item:last-child {
      padding-bottom: 0;               /* No padding on last item */
    }

    /* Paper thumbnail image container */
    .paper-image {
      width: 100px;                    /* Fixed width for thumbnail */
      height: 65px;                    /* Fixed height for thumbnail */
      flex-shrink: 0;                  /* Prevent shrinking */
      overflow: hidden;                /* Hide overflow */
      border-radius: 4px;              /* Rounded corners */
      border: 1px solid var(--border-color);  /* Border around image */
      background: var(--bg-color);     /* Background color */
    }
    
    /* Paper thumbnail image */
    .paper-image img {
      width: 100%;                     /* Fill container width */
      height: 100%;                    /* Fill container height */
      object-fit: cover;               /* Cover entire area */
    }

    /* Paper content container */
    .paper-content {
      flex: 1;                         /* Fill remaining space */
      min-width: 0;                    /* Allow text truncation */
    }

    /* Reset paragraph styles inside paper content */
    .paper-content p {
      margin-bottom: 0;                /* Override main-content p margins */
      text-align: left;                /* Left align, not justify */
    }

    /* Paper title */
    .paper-content .paper-title {
      font-family: 'Roboto Slab', serif;  /* Serif font */
      font-size: 0.95rem;              /* Slightly smaller */
      font-weight: 600;                /* Semi-bold */
      color: var(--accent-color);      /* Accent color from theme */
      margin-bottom: 0;                /* No space below */
      line-height: 1.35;               /* Line height */
    }

    /* Paper authors */
    .paper-content .paper-authors {
      font-size: 0.8rem;               /* Smaller font */
      color: var(--text-color);        /* Text color */
      margin-bottom: 0;                /* No space below */
      line-height: 1.35;               /* Line height */
    }

    /* Paper venue (journal/conference) */
    .paper-content .paper-venue {
      font-size: 0.8rem;               /* Smaller font */
      color: var(--text-color);        /* Muted color */
      font-style: italic;              /* Italic for venue */
      margin-bottom: 0;                /* No space below */
    }

    /* Paper action links container */
    .paper-links {
      font-size: 0.75rem;              /* Small font for links */
    }

    /* Individual paper link */
    .paper-link {
      color: var(--action-link-color); /* Action link color from theme */
      margin-right: 0.25rem;           /* Space between links */
    }
    
    .paper-link:hover {
      color: var(--action-link-hover); /* Action link hover from theme */
      text-decoration: underline;      /* Underline on hover */
    }

    /* ============================================
       RESPONSIVE STYLES FOR PUBLICATIONS
       ============================================ */
    @media (max-width: 600px) {
      /* Stack paper items vertically on mobile */
      .paper-item {
        flex-direction: column;        /* Stack vertically */
      }
      
      /* Full width image on mobile */
      .paper-image {
        width: 100%;                   /* Full width */
        height: 150px;                 /* Taller height */
      }
    }
'''


# ============================================
# MAIN BUILD FUNCTION
# ============================================

def build_html(content: dict[str, Any], sidebar: dict[str, Any]) -> str:
    """
    Build complete publications HTML page.
    
    Combines all components into a complete HTML document:
    - Head section with meta tags, base CSS, and publications CSS
    - Navigation bar with brand and links
    - Left sidebar with profile and social links
    - Main content area with introduction and publications by year
    - Footer with copyright
    - JavaScript for interactivity
    
    Args:
        content: Page content dictionary from content_publications.json
        sidebar: Sidebar configuration dictionary from sidebar.json
    
    Returns:
        Complete HTML document as string.
    """
    # Get base head HTML
    head_html = get_head_html(content["meta"]["title"], content["meta"]["description"], sidebar)
    
    # Insert additional publications CSS before closing </style> tag
    publications_css = get_publications_css()
    head_html = head_html.replace("</style>", f"{publications_css}</style>")
    
    # Generate introduction links
    intro_links = generate_intro_links(content["intro"]["links"])
    
    # Generate publications sections
    publications_html = generate_publications_html(content["publications"])
    
    # Generate conference abstracts sections (if present)
    conference_abstracts = content.get("conference_abstracts", [])
    conference_abstracts_html = ""
    if conference_abstracts:
        conference_abstracts_html = f'''
      <!-- Conference Abstracts Section -->
      <div class="section-divider">
        <h1 class="section-title">Selected Conference Abstracts</h1>
      </div>
      {generate_conference_abstracts_html(conference_abstracts)}'''
    
    # Build complete HTML document using template string
    html = f'''<!DOCTYPE html>
<html lang="en">
{head_html}
<body>
  <!-- Navigation Bar -->
  <nav>
    <div class="nav-container">
      <!-- Brand/Logo link to home -->
      <a href="index.html" class="nav-brand">{get_nav_brand(sidebar)}</a>
      
      <!-- Mobile hamburger menu button -->
      <button class="nav-toggle" aria-label="Toggle navigation">
        <i class="fas fa-bars"></i>
      </button>
      
      <!-- Navigation links - publications is active -->
      <ul class="nav-links">
        {get_nav_html("publications")}
      </ul>
      
      <!-- Dark/light theme toggle button -->
      <button class="theme-toggle" aria-label="Toggle dark mode">
        <i class="fas fa-moon"></i>
      </button>
    </div>
  </nav>

  <!-- Two-Column Layout Container -->
  <div class="page-wrapper">
    <!-- Left Sidebar with Profile -->
    {get_sidebar_html(sidebar)}

    <!-- Main Content Area -->
    <main class="main-content">
      <!-- Introduction Section -->
      <div class="pub-intro">
        <h1>{content["intro"]["title"]}</h1>
        <p>{content["intro"]["description"]} {intro_links}</p>
      </div>

      <!-- Publications by Year -->
      {publications_html}
      {conference_abstracts_html}
    </main>
  </div>

  <!-- Page Footer -->
  {get_footer_html(sidebar)}

  <!-- JavaScript for Navigation and Theme Toggle -->
  <script>{get_js_code()}</script>
</body>
</html>'''
    
    # Return complete HTML document
    return html


# ============================================
# MAIN ENTRY POINT
# ============================================

def main():
    """
    Main build function - entry point for script execution.
    
    Performs the following steps:
    1. Define file paths for input and output
    2. Validate that required input files exist
    3. Load sidebar configuration from sidebar.json
    4. Load publications content from content_publications.json
    5. Build complete HTML document
    6. Write HTML to publications.html output file
    
    Returns:
        0 on success, 1 on error (for use as exit code).
    """
    # Define file paths
    sidebar_path = Path("sidebar.json")              # Shared sidebar configuration
    content_path = Path("content_publications.json")  # Page-specific content
    output_path = Path("publications.html")           # Output HTML file
    
    # Validate sidebar.json exists
    if not sidebar_path.exists():
        # Print error message and return error code
        print(f"Error: {sidebar_path} not found.")
        return 1
    
    # Validate content_publications.json exists
    if not content_path.exists():
        # Print error message and return error code
        print(f"Error: {content_path} not found.")
        return 1
    
    # Load sidebar configuration
    print(f"Loading sidebar from {sidebar_path}...")
    sidebar = load_sidebar(sidebar_path)
    
    # Load page content
    print(f"Loading content from {content_path}...")
    content = load_content(content_path)
    
    # Build HTML document
    print("Building publications.html...")
    html = build_html(content, sidebar)
    
    # Write output file
    print(f"Writing to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    # Print success message
    print("Done!")
    
    # Return success code
    return 0


# ============================================
# SCRIPT EXECUTION
# ============================================

# Only run main() if this script is executed directly (not imported)
if __name__ == "__main__":
    # Exit with return code from main()
    raise SystemExit(main())