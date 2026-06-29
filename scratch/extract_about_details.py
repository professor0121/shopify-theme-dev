import re

with open("pages/about.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's locate the page-wrapper element
wrapper_match = re.search(r'<div class="page-wrapper"[^>]*>(.*)</div>\s*<div class="w-commerce-commercecartwrapper"', content, re.DOTALL)
if not wrapper_match:
    wrapper_match = re.search(r'<div class="page-wrapper"[^>]*>(.*)</body>', content, re.DOTALL)

body_content = wrapper_match.group(1) if wrapper_match else content

# Find matches for top-section, section, and card-full-width-image---img-wrapper
# Let's search inside body_content for top-section, sections, and the card wrapper
matches = list(re.finditer(r'<div\s+class="(top-section|section[^"]*|card-full-width-image---img-wrapper[^"]*)"[^>]*>', body_content))
print(f"Total blocks matching: {len(matches)}")

for i, match in enumerate(matches):
    start = match.start()
    depth = 1
    end = start + len(match.group(0))
    while depth > 0 and end < len(body_content):
        next_open = body_content.find("<div", end)
        next_close = body_content.find("</div>", end)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            end = next_open + 4
        else:
            depth -= 1
            end = next_close + 6
            
    sec_content = body_content[start:end]
    preview = re.sub(r'<[^>]+>', ' ', sec_content).strip()[:120]
    preview_clean = preview.encode('ascii', errors='ignore').decode('utf-8')
    print(f"Block {i+1} (tag: {match.group(0)}):")
    print(f"  Preview: {preview_clean}")
    
    with open(f"C:/Users/ravik/.gemini/antigravity-ide/brain/70a26aa0-84b9-41a4-bb6e-06a64a180c35/scratch/about_block_{i+1}.html", "w", encoding="utf-8") as out:
        out.write(sec_content)
