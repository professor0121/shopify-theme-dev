import os
import re

files_to_check = [
    "pages/index.html",
    "pages/home-pages/home-v1.html",
    "pages/home-pages/home-v2.html",
    "pages/home-pages/home-v3.html",
    "pages/about.html",
    "pages/contact.html",
    "pages/product/wireless-mouse.html",
    "pages/collection-pages/collection-v1.html"
]

for filepath in files_to_check:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read(1000) # Read the beginning of the file where <html> tag is
            match = re.search(r'data-wf-page="([^"]+)"', content)
            match_site = re.search(r'data-wf-site="([^"]+)"', content)
            page_id = match.group(1) if match else "Not found"
            site_id = match_site.group(1) if match_site else "Not found"
            print(f"{filepath}: page_id={page_id}, site_id={site_id}")
    else:
        print(f"File not found: {filepath}")
