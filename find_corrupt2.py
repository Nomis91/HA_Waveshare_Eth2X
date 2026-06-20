import os
import sys

# Avoid the literal strings that get transformed
s1 = chr(91) + 'ADDRESS' + chr(93)
s2 = chr(91) + 'PERSON_NAME' + chr(93)

root = r'c:\Users\Simon\SynologyDrive\HomeAssistant\HA_Waveshare_Eth2X\custom_components\ha_waveshare_eth2x'

found = False
for dirpath, dirnames, filenames in os.walk(root):
    for f in sorted(filenames):
        if f.endswith('.py'):
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
            if s1 in content or s2 in content:
                found = True
                print(f'CORRUPTED: {os.path.relpath(path, root)}')
                for i, line in enumerate(content.split('\n'), 1):
                    if s1 in line or s2 in line:
                        print(f'  Line {i}: {line.strip()}')

if not found:
    print('No corrupted files found.')

# Also check for null bytes in all files
print()
print('Checking for null bytes...')
for dirpath, dirnames, filenames in os.walk(root):
    for f in sorted(filenames):
        if f.endswith('.py'):
            path = os.path.join(dirpath, f)
            with open(path, 'rb') as fh:
                data = fh.read()
            if b'\x00' in data:
                null_positions = [i for i, b in enumerate(data) if b == 0]
                print(f'NULL BYTES in: {os.path.relpath(path, root)}')
                print(f'  Positions: {null_positions[:20]}')
                # Show context around null bytes
                for pos in null_positions[:3]:
                    start = max(0, pos - 50)
                    end = min(len(data), pos + 50)
                    context = data[start:end]
                    print(f'  Around pos {pos}: {context}')

print('Done.')
