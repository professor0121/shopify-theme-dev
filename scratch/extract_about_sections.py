import re

with open("pages/about.html", "r", encoding="utf-8") as f:
    content = f.read()

# page-wrapper search
wrapper_match = re.search(r'<div class="page-wrapper"[^>]*>(.*)</div>\s*<div class="w-commerce-commercecartwrapper"', content, re.DOTALL)
if not wrapper_match:
    wrapper_match = re.search(r'<div class="page-wrapper"[^>]*>(.*)</body>', content, re.DOTALL)

if wrapper_match:
    body_content = wrapper_match.group(1)
    sections = re.findall(r'<div class="([^"]*(?:section|header|footer|wrapper)[^"]*)"([^>]*)>', body_content)
    print(f"Found {len(sections)} sections in about.html:")
    for i, (cls, attrs) in enumerate(sections):
        print(f"Section {i+1}: class=\"{cls}\" attrs=\"{attrs.strip()}\"")
else:
    print("Page wrapper not found in about.html.")
