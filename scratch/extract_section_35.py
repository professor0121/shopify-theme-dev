import re

with open("pages/home-pages/home-v1.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find matches for <div class="section" ...>
matches = re.finditer(r'<div\s+class="section"[^>]*>', content)
for i, match in enumerate(matches):
    start = match.start()
    # Find closing tag matching this nesting level
    depth = 1
    end = start + len(match.group(0))
    while depth > 0 and end < len(content):
        next_open = content.find("<div", end)
        next_close = content.find("</div>", end)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            end = next_open + 4
        else:
            depth -= 1
            end = next_close + 6
    
    sec_content = content[start:end]
    preview = re.sub(r'<[^>]+>', ' ', sec_content).strip()[:100]
    print(f"Section {i+1}: preview='{preview}'")
    if "Newsletter" in sec_content or "Subscribe" in sec_content or "newsletter" in sec_content:
        print("  -> Is newsletter section")
    if "filter:blur" in match.group(0):
        print(f"  -> Has blur style. Writing index {i+1} content...")
        with open(f"C:/Users/ravik/.gemini/antigravity-ide/brain/70a26aa0-84b9-41a4-bb6e-06a64a180c35/scratch/section_blur_{i+1}.html", "w", encoding="utf-8") as out:
            out.write(sec_content)
