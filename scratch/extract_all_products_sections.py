import re

with open("pages/all-products-pages/all-products-v1.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find matches for <div class="section ...">
matches = list(re.finditer(r'<div\s+class="section[^"]*"[^>]*>', content))
print(f"Total section containers matching pattern: {len(matches)}")

for i, match in enumerate(matches):
    start = match.start()
    # Find matching closing div tag
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
    preview = re.sub(r'<[^>]+>', ' ', sec_content).strip()[:150]
    # Replace non-ascii chars for console printing
    preview_clean = preview.encode('ascii', errors='ignore').decode('utf-8')
    print(f"Section {i+1} (tag: {match.group(0)}):")
    print(f"  Preview: {preview_clean}")
    
    # Save the section contents to a file
    with open(f"C:/Users/ravik/.gemini/antigravity-ide/brain/70a26aa0-84b9-41a4-bb6e-06a64a180c35/scratch/all_products_sec_{i+1}.html", "w", encoding="utf-8") as out:
        out.write(sec_content)
