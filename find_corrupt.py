import os

root = r'c:\Users\Simon\SynologyDrive\HomeAssistant\HA_Waveshare_Eth2X\custom_components\ha_waveshare_eth2x'
placeholder1 = '[ADDRESS]'
placeholder2 = '[PERSON_NAME]'

found_any = False
for dirpath, dirnames, filenames in os.walk(root):
    for f in sorted(filenames):
        if f.endswith('.py'):
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
            if placeholder1 in content or placeholder2 in content:
                found_any = True
                print(f'CORRUPTED: {os.path.relpath(path, root)}')
                for i, line in enumerate(content.split('\n'), 1):
                    if placeholder1 in line or placeholder2 in line:
                        print(f'  Line {i}: {line.strip()}')

if not found_any:
    print('No corrupted files found.')
else:
    print('\nDone.')