import os

root = r'c:\Users\Simon\SynologyDrive\HomeAssistant\HA_Waveshare_Eth2X\custom_components\waveshare_eth2x'
found = []
for dirpath, dirnames, filenames in os.walk(root):
    for f in filenames:
        if f.endswith('.py'):
            path = os.path.join(dirpath, f)
            with open(path, 'rb') as fh:
                content = fh.read()
            if b'[ADDRESS]' in content or b'[PERSON_NAME]' in content:
                found.append(path)
                print(f'FOUND in: {path}')
                for i, line in enumerate(content.split(b'\n')):
                    if b'[ADDRESS]' in line or b'[PERSON_NAME]' in line:
                        print(f'  Line {i+1}: {line.decode("utf-8", errors="replace").strip()}')
if not found:
    print('No corrupted tokens found. Searching for other issues...')
    # Check all files for syntax errors
    import py_compile
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            if f.endswith('.py'):
                path = os.path.join(dirpath, f)
                try:
                    py_compile.compile(path, doraise=True)
                except py_compile.PyCompileError as e:
                    print(f'SYNTAX ERROR in {path}: {e}')
