import os
import sys

# Encode the search strings to avoid rendering corruption
s1 = "[" + "ADDRESS" + "]"
s2 = "[" + "PERSON" + "_NAME" + "]"

root = r"c:\Users\Simon\SynologyDrive\HomeAssistant\HA_Waveshare_Eth2X\custom_components\ha_waveshare_eth2x"

found = False
for dirpath, dirnames, filenames in os.walk(root):
    for f in sorted(filenames):
        if f.endswith(".py"):
            path = os.path.join(dirpath, f)
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
            if s1 in content or s2 in content:
                found = True
                print(f"CORRUPTED: {os.path.relpath(path, root)}")
                for i, line in enumerate(content.split("\n"), 1):
                    if s1 in line or s2 in line:
                        print(f"  Line {i}: {line.strip()}")

if not found:
    print("No corrupted files found.")

# Also check for null bytes
print()
print("Checking for null bytes...")
for dirpath, dirnames, filenames in os.walk(root):
    for f in sorted(filenames):
        if f.endswith(".py"):
            path = os.path.join(dirpath, f)
            with open(path, "rb") as fh:
                data = fh.read()
            nulls = [i for i, b in enumerate(data) if b == 0]
            if nulls:
                print(f"NULL BYTES in: {os.path.relpath(path, root)}")
                print(f"  Count: {len(nulls)}, Positions: {nulls[:20]}")
                for pos in nulls[:3]:
                    start = max(0, pos - 30)
                    end = min(len(data), pos + 30)
                    context = data[start:end]
                    print(f"  Around pos {pos}: {context}")

print("Done.")
