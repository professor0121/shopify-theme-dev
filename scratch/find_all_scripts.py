import re

with open("pages/home-pages/home-v1.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find script tags using regex
script_tags = re.findall(r'<script\b[^>]*>(.*?)</script>', content, re.DOTALL)
script_srcs = re.findall(r'<script\b[^>]*src="([^"]+)"', content)

print(f"Found {len(script_srcs)} script files:")
for src in script_srcs:
    print(f"  Src: {src}")

print(f"\nFound {len(script_tags)} script tags in total. Inline content snippets:")
for i, tag_content in enumerate(script_tags):
    trimmed = tag_content.strip()
    if trimmed:
        print(f"\n--- Script {i+1} ---")
        # Replace non-ascii chars to avoid printing failures in console
        clean = trimmed.encode('ascii', errors='replace').decode('ascii')
        print(clean[:300] + ("..." if len(clean) > 300 else ""))
