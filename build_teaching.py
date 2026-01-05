#!/usr/bin/env python3
"""
Build script for teaching.html page.
Uses sidebar.py module for shared components.

This script generates the teaching page for the academic portfolio,
displaying teaching philosophy, courses taught, and mentoring experience.

Usage:
    python build_teaching.py

Required files:
    - sidebar.json: Profile, links, and footer configuration
    - content_teaching.json: Teaching and mentoring data
    - sidebar.py: Shared module with CSS and HTML generation functions

Output:
    - teaching.html: Complete HTML page ready for deployment
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

def load_content(path: Path = Path("content_teaching.json")) -> dict[str, Any]:
    """
    Load teaching content from JSON file.
    
    Args:
        path: Path to the content JSON configuration file.
              Defaults to "content_teaching.json" in current directory.
    
    Returns:
        Dictionary containing teaching data including:
        - meta: Page title and description
        - philosophy: Teaching philosophy statement
        - courses: List of course role groups
        - mentoring: List of mentoring categories
    """
    # Open file with UTF-8 encoding for international character support
    with open(path, "r", encoding="utf-8") as f:
        # Parse JSON and return as dictionary
        return json.load(f)


# ============================================
# HTML GENERATION FUNCTIONS
# ============================================

def generate_course_html(course: dict[str, Any]) -> str:
    """
    Generate HTML for a single course entry (bullet item).
    
    Args:
        course: Dictionary containing course data:
               - code: Course code (e.g., "EECE 2323")
               - name: Course name
               - semesters: List of semesters taught
    
    Returns:
        HTML string for the course entry.
    """
    # Join semesters with comma
    semesters = ", ".join(course["semesters"])
    
    # Build course entry HTML - bullet item
    html = f'''<li class="course-list-item">
            <span class="course-code">{course["code"]}</span>
            <span class="course-name">{course["name"]}</span>
            <span class="course-semesters">({semesters})</span>
          </li>'''
    
    return html


def generate_role_section_html(role_group: dict[str, Any]) -> str:
    """
    Generate HTML for a role section (e.g., Teaching Assistant, Lecturer).
    
    Args:
        role_group: Dictionary containing:
                   - role: Role title
                   - institution: Institution name
                   - location: Location
                   - period: Time period
                   - description: Role description
                   - courses_list: List of course dictionaries
    
    Returns:
        HTML string for the role section.
    """
    # Get role info
    role = role_group["role"]
    institution = role_group["institution"]
    location = role_group["location"]
    period = role_group["period"]
    description = role_group["description"]
    
    # Generate HTML for each course in this role
    courses_html = "\n          ".join(
        generate_course_html(course)
        for course in role_group["courses_list"]
    )
    
    # Build role section HTML - courses first, description second, affiliation last
    html = f'''<div class="role-section">
        <ul class="course-list">
          {courses_html}
        </ul>
        <p class="role-description">{description}</p>
        <div class="role-meta">
          <span class="role-title">{role}</span>, 
          <span class="role-institution">{institution}</span>, 
          <span class="role-location">{location}</span>
          <span class="role-period">({period})</span>
        </div>
      </div>'''
    
    return html


def generate_courses_html(courses: list[dict[str, Any]]) -> str:
    """
    Generate HTML for all course sections.
    
    Args:
        courses: List of role group dictionaries.
    
    Returns:
        HTML string with all role sections.
    """
    # Generate HTML for each role section
    sections = []
    
    for role_group in courses:
        sections.append(generate_role_section_html(role_group))
    
    # Join all sections with newlines
    return "\n      ".join(sections)


def generate_student_html(student: dict[str, str]) -> str:
    """
    Generate HTML for a single student entry.
    
    Args:
        student: Dictionary containing student data:
                - name: Student name
                - program: Degree program
                - period: Mentoring period
                - institution: Institution and expected graduation
    
    Returns:
        HTML string for the student entry.
    """
    html = f'''<div class="student-item">
            <div class="student-name">{student["name"]}</div>
            <div class="student-program">{student["program"]} ({student["period"]})</div>
            <div class="student-institution">{student["institution"]}</div>
          </div>'''
    
    return html


def generate_mentoring_category_html(category: dict[str, Any]) -> str:
    """
    Generate HTML for a mentoring category (e.g., Graduate Students).
    
    Args:
        category: Dictionary containing:
                 - type: Category title
                 - students: List of student dictionaries
    
    Returns:
        HTML string for the mentoring category.
    """
    # Get category type
    category_type = category["type"]
    
    # Generate HTML for each student
    students_html = "\n          ".join(
        generate_student_html(student)
        for student in category["students"]
    )
    
    # Build category section HTML
    html = f'''<div class="mentoring-category">
          <h4 class="category-heading">{category_type}</h4>
          {students_html}
        </div>'''
    
    return html


def generate_mentoring_html(mentoring: list[dict[str, Any]]) -> str:
    """
    Generate HTML for all mentoring sections.
    
    Args:
        mentoring: List of mentoring category dictionaries.
    
    Returns:
        HTML string with all mentoring categories.
    """
    # Generate HTML for each category
    categories = []
    
    for category in mentoring:
        categories.append(generate_mentoring_category_html(category))
    
    # Join all categories with newlines
    return "\n        ".join(categories)


def get_teaching_css() -> str:
    """
    Generate additional CSS specific to teaching page.
    
    Returns:
        CSS string for teaching page styling.
    """
    return '''
    /* ============================================
       TEACHING PAGE STYLES
       Styles specific to the teaching page
       ============================================ */
    
    /* Section headings */
    .section-heading {
      font-family: 'Roboto Slab', serif;  /* Serif font */
      font-size: 1.4rem;               /* Heading size */
      font-weight: 700;                /* Bold */
      color: var(--text-color);        /* Text color */
      margin-bottom: 0.6rem;           /* Reduced space below heading */
      padding-bottom: 0.4rem;          /* Padding above border */
      border-bottom: 1px solid var(--border-color);  /* Underline border */
    }

    /* Courses section */
    .courses-section {
      margin-bottom: 2rem;             /* Space below section */
    }

    /* Role section (TA, Lecturer, etc.) */
    .role-section {
      margin-bottom: 0.75rem;          /* Space between role sections */
      padding-bottom: 0.75rem;         /* Padding above border */
      border-bottom: 1px solid var(--border-color);  /* Bottom border */
    }
    
    /* Remove border from last role section */
    .role-section:last-child {
      border-bottom: none;             /* No border on last item */
      padding-bottom: 0;               /* No padding */
    }

    /* Course list - first element */
    .course-list {
      list-style: none;                /* Remove default bullets */
      padding-left: 0;                 /* Remove left padding */
      margin: 0;                       /* No margin */
    }

    /* Course list item */
    .course-list-item {
      padding: 0.05rem 0;              /* Minimal vertical padding */
      padding-left: 1rem;              /* Indent */
      position: relative;              /* For bullet positioning */
      font-size: 0.9rem;               /* Font size */
    }
    
    /* Custom bullet */
    .course-list-item::before {
      content: "•";                    /* Bullet */
      position: absolute;              /* Position absolutely */
      left: 0;                         /* At left edge */
      color: var(--text-color);        /* Text color */
    }
    
    /* Course code */
    .course-code {
      font-weight: 600;                /* Semi-bold */
      color: var(--text-color);        /* Text color */
      margin-right: 0.25rem;           /* Space after code */
    }
    
    /* Course name */
    .course-name {
      color: var(--text-color);        /* Text color */
    }

    /* Course semesters */
    .course-semesters {
      color: var(--text-color);        /* Text color */
      font-size: 0.85rem;              /* Smaller font */
      margin-left: 0.25rem;            /* Space before */
    }

    /* Role description - second element */
    .role-description {
      font-size: 0.9rem;               /* Smaller font */
      color: var(--text-color);        /* Text color */
      line-height: 1.6;                /* Line height */
      margin: 0.2rem 0;                /* Small vertical margin */
    }

    /* Role meta - last element (role, institution, location, period) */
    .role-meta {
      font-size: 0.85rem;              /* Smaller font */
      color: var(--text-muted);        /* Muted color */
      margin-top: 0.15rem;             /* Small space above */
    }
    
    /* Role title (Teaching Assistant, Lecturer, etc.) */
    .role-title {
      font-weight: 400;                /* Normal weight - no bold */
      color: var(--text-color);        /* Black color */
    }
    
    /* Role institution */
    .role-institution {
      font-weight: 400;                /* Normal weight */
    }
    
    /* Role period */
    .role-period {
      color: var(--text-muted);        /* Muted color */
    }

    /* Mentoring section */
    .mentoring-section {
      margin-bottom: 2rem;             /* Space below section */
    }

    /* Mentoring category */
    .mentoring-category {
      margin-bottom: 0.75rem;          /* Space between categories */
    }
    
    /* Category heading */
    .category-heading {
      font-family: 'Roboto Slab', serif;  /* Serif font */
      font-size: 1rem;                 /* Standard size */
      font-weight: 600;                /* Semi-bold */
      color: var(--accent-color);      /* Accent color from theme */
      margin-bottom: 0.5rem;           /* Space below heading */
    }

    /* Individual student item */
    .student-item {
      margin-bottom: 0.75rem;          /* Space between students */
      padding-left: 1rem;              /* Indent */
      border-left: 2px solid var(--border-color);  /* Left border */
    }
    
    /* Student name */
    .student-name {
      font-weight: 600;                /* Semi-bold */
      color: var(--text-color);        /* Text color */
    }
    
    /* Student program */
    .student-program {
      font-size: 0.85rem;              /* Smaller font */
      color: var(--text-color);        /* Text color */
    }
    
    /* Student institution */
    .student-institution {
      font-size: 0.85rem;              /* Smaller font */
      color: var(--text-color);        /* Muted color */
      font-style: italic;              /* Italic */
    }
'''


# ============================================
# MAIN BUILD FUNCTION
# ============================================

def build_html(content: dict[str, Any], sidebar: dict[str, Any]) -> str:
    """
    Build complete teaching HTML page.
    
    Combines all components into a complete HTML document:
    - Head section with meta tags, base CSS, and teaching CSS
    - Navigation bar with brand and links
    - Left sidebar with profile and social links
    - Main content area with philosophy, courses, and mentoring
    - Footer with copyright
    - JavaScript for interactivity
    
    Args:
        content: Page content dictionary from content_teaching.json
        sidebar: Sidebar configuration dictionary from sidebar.json
    
    Returns:
        Complete HTML document as string.
    """
    # Get base head HTML
    head_html = get_head_html(content["meta"]["title"], content["meta"]["description"], sidebar)
    
    # Insert additional teaching CSS before closing </style> tag
    teaching_css = get_teaching_css()
    head_html = head_html.replace("</style>", f"{teaching_css}</style>")
    
    # Generate courses HTML
    courses_html = generate_courses_html(content["courses"])
    
    # Generate mentoring HTML
    mentoring_html = generate_mentoring_html(content["mentoring"])
    
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
      
      <!-- Navigation links - teaching is active -->
      <ul class="nav-links">
        {get_nav_html("teaching")}
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
      <!-- Courses Section -->
      <section class="courses-section">
        <h2 class="section-heading">Courses</h2>
        {courses_html}
      </section>

      <!-- Mentoring Section -->
      <section class="mentoring-section">
        <h2 class="section-heading">Mentoring</h2>
        {mentoring_html}
      </section>
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
    4. Load teaching content from content_teaching.json
    5. Build complete HTML document
    6. Write HTML to teaching.html output file
    
    Returns:
        0 on success, 1 on error (for use as exit code).
    """
    # Define file paths
    sidebar_path = Path("sidebar.json")           # Shared sidebar configuration
    content_path = Path("content_teaching.json")  # Page-specific content
    output_path = Path("teaching.html")           # Output HTML file
    
    # Validate sidebar.json exists
    if not sidebar_path.exists():
        # Print error message and return error code
        print(f"Error: {sidebar_path} not found.")
        return 1
    
    # Validate content_teaching.json exists
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
    print("Building teaching.html...")
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