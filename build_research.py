#!/usr/bin/env python3
"""
Build script for research.html page.
Uses sidebar.py module for shared components.

This script generates the research page for the academic portfolio,
displaying research interests and project descriptions with images.

Usage:
    python build_research.py

Required files:
    - sidebar.json: Profile, links, and footer configuration
    - content_research.json: Research interests and projects data
    - sidebar.py: Shared module with CSS and HTML generation functions

Output:
    - research.html: Complete HTML page ready for deployment
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

def load_content(path: Path = Path("content_research.json")) -> dict[str, Any]:
    """
    Load research content from JSON file.
    
    Args:
        path: Path to the content JSON configuration file.
              Defaults to "content_research.json" in current directory.
    
    Returns:
        Dictionary containing research data including:
        - meta: Page title and description
        - interests: List of research interest keywords
        - projects: List of research project dictionaries
    """
    # Open file with UTF-8 encoding for international character support
    with open(path, "r", encoding="utf-8") as f:
        # Parse JSON and return as dictionary
        return json.load(f)


# ============================================
# HTML GENERATION FUNCTIONS
# ============================================

def generate_interests_html(interests: list[str]) -> str:
    """
    Generate research interests as comma-separated list.
    
    Args:
        interests: List of research interest keywords.
    
    Returns:
        HTML string with formatted interests.
    """
    # Join interests with comma and space
    return ", ".join(interests)


def generate_project_html(project: dict[str, Any]) -> str:
    """
    Generate HTML for a single research project.
    
    Creates structured HTML showing:
    - Project title as heading
    - Optional image on the left with customizable width
    - Description paragraphs
    
    Args:
        project: Dictionary containing project data:
                - title: Project title
                - image: Path to project image (optional)
                - image_width: Desired width in pixels (optional, defaults to 700)
                - description: List of paragraph strings
    
    Returns:
        HTML string for the project entry.
    """
    # Get project image path if provided
    image = project.get("image", "")
    
    # Get custom image width; fall back to 700px
    image_width = project.get("image_width", 700)
    
    # Generate image HTML if image path exists
    image_html = ""
    if image:
        image_html = f'''<div class="project-image" style="width: {image_width}px;">
            <img src="{image}" alt="{project["title"]}">
          </div>'''
    
    # Generate description paragraphs
    desc_html = "\n          ".join(
        f"<p>{para}</p>" 
        for para in project["description"]
    )
    
    # Build project entry HTML structure
    html = f'''<div class="project-item">
        <h3 class="project-title">{project["title"]}</h3>
        <div class="project-content">
          {image_html}
          <div class="project-description">
            {desc_html}
          </div>
        </div>
      </div>'''
    
    return html


def generate_projects_html(projects: list[dict[str, Any]]) -> str:
    """
    Generate HTML for all research projects.
    
    Args:
        projects: List of project dictionaries.
    
    Returns:
        HTML string with all project entries.
    """
    # Generate HTML for each project
    project_entries = []
    
    for project in projects:
        project_entries.append(generate_project_html(project))
    
    # Join all projects with newlines
    return "\n      ".join(project_entries)


def get_research_css() -> str:
    """
    Generate additional CSS specific to research page.
    
    Returns:
        CSS string for research page styling.
    """
    return '''
    /* ============================================
       RESEARCH PAGE STYLES
       Styles specific to the research page
       ============================================ */
    
    /* Page introduction section */
    .research-intro {
      margin-bottom: 2rem;             /* Space below intro */
    }
    
    /* Research interests heading */
    .research-intro h1 {
      font-family: 'Roboto Slab', serif;  /* Serif font */
      font-size: 1.6rem;               /* Large heading */
      font-weight: 700;                /* Bold */
      color: var(--text-color);        /* Text color */
      margin-bottom: 0.75rem;          /* Space below */
    }
    
    /* Research interests list */
    .research-interests {
      color: var(--text-color);        /* Text color */
      font-size: 1rem;                 /* Standard size */
      font-style: italic;              /* Italic for emphasis */
      margin-bottom: 1.5rem;           /* Space below */
      padding-bottom: 1rem;            /* Padding above border */
      border-bottom: 1px solid var(--border-color);  /* Bottom border */
    }

    /* Research projects section heading */
    .projects-heading {
      font-family: 'Roboto Slab', serif;  /* Serif font */
      font-size: 1.4rem;               /* Heading size */
      font-weight: 700;                /* Bold */
      color: var(--text-color);        /* Text color */
      margin-bottom: 1.5rem;           /* Space below heading */
      padding-bottom: 0.4rem;          /* Padding above border */
      border-bottom: 1px solid var(--border-color);  /* Underline border */
    }

    /* Individual project item */
    .project-item {
      margin-bottom: 2.5rem;           /* Space between projects */
      padding-bottom: 2rem;            /* Padding above border */
      border-bottom: 1px solid var(--border-color);  /* Bottom border separator */
    }
    
    /* Remove border from last project */
    .project-item:last-child {
      border-bottom: none;             /* No border on last item */
      margin-bottom: 0;                /* No bottom margin */
      padding-bottom: 0;               /* No padding */
    }

    /* Project title */
    .project-title {
      font-family: 'Roboto Slab', serif;  /* Serif font */
      font-size: 1.15rem;              /* Slightly larger */
      font-weight: 600;                /* Semi-bold */
      color: var(--accent-color);      /* Accent color from theme */
      margin-bottom: 1rem;             /* Space below title */
      line-height: 1.4;                /* Line height */
    }

    /* Project content container (image + description) */
    .project-content {
      display: block;                  /* Block layout for float */
    }

    /* Project image container */
    .project-image {
      float: left;                     /* Float image to left */
      width: 700px;                    /* Larger fixed width */
      margin-right: 1.5rem;            /* Space between image and text */
      margin-bottom: 0.75rem;          /* Space below image */
      border-radius: 4px;              /* Rounded corners */
      overflow: hidden;                /* Hide overflow */
      border: 1px solid var(--border-color);  /* Border around image */
    }
    
    /* Project image */
    .project-image img {
      width: 100%;                     /* Fill container width */
      height: auto;                    /* Maintain aspect ratio */
      display: block;                  /* Remove inline spacing */
    }

    /* Project description container */
    .project-description {
      /* No overflow hidden - allows text to wrap under floated image */
    }

    /* Project description paragraphs */
    .project-description p {
      color: var(--text-color);        /* Text color */
      font-size: 0.95rem;              /* Slightly smaller */
      line-height: 1.7;                /* Comfortable line height */
      margin-bottom: 0.75rem;          /* Space between paragraphs */
      text-align: justify;             /* Justify text */
    }
    
    /* Remove margin from last paragraph */
    .project-description p:last-child {
      margin-bottom: 0;                /* No bottom margin */
    }

    /* Clear float after project content */
    .project-content::after {
      content: "";
      display: table;
      clear: both;
    }

    /* ============================================
       RESPONSIVE STYLES FOR RESEARCH
       ============================================ */
    @media (max-width: 900px) {
      /* Stack project content vertically on tablet/mobile */
      .project-image {
        float: none;                   /* Remove float */
        width: 100%;                   /* Full width */
        max-width: 520px;              /* Maximum width */
        margin-right: 0;               /* Remove right margin */
        margin-bottom: 1rem;           /* Space below */
      }
    }
'''


# ============================================
# MAIN BUILD FUNCTION
# ============================================

def build_html(content: dict[str, Any], sidebar: dict[str, Any]) -> str:
    """
    Build complete research HTML page.
    
    Combines all components into a complete HTML document:
    - Head section with meta tags, base CSS, and research CSS
    - Navigation bar with brand and links
    - Left sidebar with profile and social links
    - Main content area with interests and projects
    - Footer with copyright
    - JavaScript for interactivity
    
    Args:
        content: Page content dictionary from content_research.json
        sidebar: Sidebar configuration dictionary from sidebar.json
    
    Returns:
        Complete HTML document as string.
    """
    # Get base head HTML
    head_html = get_head_html(content["meta"]["title"], content["meta"]["description"], sidebar)
    
    # Insert additional research CSS before closing </style> tag
    research_css = get_research_css()
    head_html = head_html.replace("</style>", f"{research_css}</style>")
    
    # Generate interests HTML
    interests_html = generate_interests_html(content["interests"])
    
    # Generate projects HTML
    projects_html = generate_projects_html(content["projects"])
    
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
      
      <!-- Navigation links - research is active -->
      <ul class="nav-links">
        {get_nav_html("research")}
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
      <!-- Research Interests Section -->
      <div class="research-intro">
        <h1>Research Interests</h1>
        <p class="research-interests">{interests_html}</p>
      </div>

      <!-- Research Projects Section -->
      <h2 class="projects-heading">Research Projects</h2>
      {projects_html}
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
    4. Load research content from content_research.json
    5. Build complete HTML document
    6. Write HTML to research.html output file
    
    Returns:
        0 on success, 1 on error (for use as exit code).
    """
    # Define file paths
    sidebar_path = Path("sidebar.json")           # Shared sidebar configuration
    content_path = Path("content_research.json")  # Page-specific content
    output_path = Path("research.html")           # Output HTML file
    
    # Validate sidebar.json exists
    if not sidebar_path.exists():
        # Print error message and return error code
        print(f"Error: {sidebar_path} not found.")
        return 1
    
    # Validate content_research.json exists
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
    print("Building research.html...")
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
