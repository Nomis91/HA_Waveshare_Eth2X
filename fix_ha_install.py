"""Repair helper for the 'Invalid handler specified' error.

Run this on the machine running Home Assistant (or copy-paste the
paths into a shell) when the config flow shows:

    Der Konfigurationsfluss konnte nicht geladen werden:
        {"message":"Invalid handler specified"}

Root cause
----------
After renaming the integration folder, Home Assistant's
`.storage/core.config_entries` (and possibly the in-memory
import cache) still references the old folder / old flow handler.
The frontend tries to start a config flow for the domain
``waveshare_eth2x`` but HA cannot resolve a matching
``config_flow.py`` because the package is loaded from a folder
that no longer matches the registered integration.

What this script does
---------------------
1.  Detects both the old (``waveshare_eth2x``) and new
    (``ha_waveshare_eth2x``) integration folders in the given
    Home Assistant ``custom_components`` directory.
2.  Reports the situation and prints the exact shell commands
    the user should run to fix it.

It does NOT modify the Home Assistant config files itself;
the user must do that (or, preferably, just rename the folder
inside HA's ``custom_components`` and reload).
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


OLD_NAME = "waveshare_eth2x"
NEW_NAME = "ha_waveshare_eth2x"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "ha_custom_components",
        type=Path,
        help="Path to Home Assistant's custom_components directory "
        "(e.g. ~/.homeassistant/custom_components)",
    )
    args = parser.parse_args()
    cc = args.ha_custom_components.expanduser().resolve()
    old = cc / OLD_NAME
    new = cc / NEW_NAME

    print(f"HA custom_components: {cc}")
    print(f"  old folder ({OLD_NAME}) exists: {old.is_dir()}")
    print(f"  new folder ({NEW_NAME}) exists: {new.is_dir()}")
    print()

    if old.is_dir() and new.is_dir():
        print("BOTH folders exist. Pick one (the new one is canonical):")
        print(f"  - Remove the old folder:    rm -rf {old}")
        print(f"  - Keep the new folder:      {new}")
        print("  Then in Home Assistant: Developer Tools -> YAML -> Reloads")
        print("  Or simply restart Home Assistant.")
        return 1
    if old.is_dir() and not new.is_dir():
        print("Only the OLD folder exists. Rename it:")
        print(f"  mv {old} {new}")
        print("Then restart Home Assistant.")
        return 2
    if new.is_dir() and not old.is_dir():
        print("Only the NEW folder exists - this is the correct state.")
        print("If the error persists, clear the HA import cache:")
        print("  - Stop Home Assistant")
        print("  - Delete the contents of <config>/__pycache__ (HA's own cache)")
        print("  - Delete <config>/.storage/core.config_entries if you had an")
        print("    entry under the old name (or just delete the broken entry")
        print("    via Settings -> Devices & Services).")
        print("  - Start Home Assistant again.")
        return 0
    print("Neither folder exists in the given custom_components directory.")
    print(f"Copy the integration to: {new}")
    return 3


if __name__ == "__main__":
    sys.exit(main())
