import os
import re
from pathlib import Path

REPO = Path(".").resolve()

# Windows forbidden characters in filenames
bad = re.compile(r'[<>:"/\\|?*]')

def sanitize(name: str) -> str:
    # Also replace & to keep names simple across tools
    name = name.replace("&", "_")
    name = bad.sub("_", name)
    return name

renames = []
for p in REPO.rglob("*"):
    if not p.is_file():
        continue
    if p.name != sanitize(p.name):
        new_name = sanitize(p.name)
        new_path = p.with_name(new_name)

        # Avoid collisions: if the sanitized target already exists, append a number
        if new_path.exists():
            stem = new_path.stem
            suffix = new_path.suffix
            i = 2
            while True:
                candidate = new_path.with_name(f"{stem}__{i}{suffix}")
                if not candidate.exists():
                    new_path = candidate
                    break
                i += 1

        renames.append((p, new_path))

# Do renames
for old, new in renames:
    new.parent.mkdir(parents=True, exist_ok=True)
    old.rename(new)
    print(f"RENAMED:\n  {old}\n  -> {new}\n")

print(f"Total renamed: {len(renames)}")
