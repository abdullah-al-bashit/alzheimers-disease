from playwright.sync_api import sync_playwright
import os

def html_to_png(html_file, output_file, scale=3):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1200, 'height': 900}, device_scale_factor=scale)
        
        # Convert to absolute path
        full_path = os.path.abspath(html_file)
        page.goto(f'file://{full_path}')
        
        page.screenshot(path=output_file, full_page=True)
        browser.close()
        print(f'Saved: {output_file} ({scale}x resolution)')

# Usage

# 2 = Good for web
# 3 = Recommended (sharp on retina displays)
# 4 = Best quality (larger file size)

# html_to_png('projects/alzheimers.html', 'assets/research/research_alzheimers.png', 3)
# html_to_png('projects/copd.html', 'assets/research/research_copd.png', 3)
# html_to_png('projects/copd_circular.html', 'assets/research/research_copd.png', 3)