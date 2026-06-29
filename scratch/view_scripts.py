with open("pages/home-pages/home-v1.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines[-50:]):
    # Print clean representation to avoid terminal encoding errors
    clean_line = line.encode('ascii', errors='replace').decode('ascii')
    print(f"{len(lines)-50+i+1}: {clean_line}", end="")
