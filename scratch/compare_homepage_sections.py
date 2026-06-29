import re

with open("pages/home-pages/home-v1.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's locate the page-wrapper element: <div class="page-wrapper" ...>
wrapper_match = re.search(r'<div class="page-wrapper"[^>]*>(.*)</div>\s*<div class="w-commerce-commercecartwrapper"', content, re.DOTALL)
if not wrapper_match:
    wrapper_match = re.search(r'<div class="page-wrapper"[^>]*>(.*)</body>', content, re.DOTALL)

if wrapper_match:
    body_content = wrapper_match.group(1)
    # Find direct section divs under page-wrapper
    # Let's find tags like <div class="section ..."> or <div class="header-wrapper ..."> or <div class="footer ...">
    # We can match tags that have class containing 'section' or 'header' or 'footer'
    sections = re.findall(r'<div class="([^"]*(?:section|header|footer|wrapper)[^"]*)"([^>]*)>', body_content)
    print(f"Found {len(sections)} sections in Home V1:")
    for i, (cls, attrs) in enumerate(sections):
        print(f"Section {i+1}: class=\"{cls}\" attrs=\"{attrs.strip()}\"")
else:
    print("Page wrapper not found in Home V1.")
