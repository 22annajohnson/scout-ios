#!/usr/bin/env python3
"""Select an available iPhone from the newest installed iOS runtime."""
import json
import re
import subprocess
import sys


def choose(devices):
    candidates = []
    for runtime, entries in devices.items():
        match = re.search(r"\.iOS-(\d+)-(\d+)(?:-(\d+))?$", runtime)
        if not match:
            continue
        version = tuple(int(part or 0) for part in match.groups())
        for device in entries:
            if device.get("isAvailable") and device["name"].startswith("iPhone"):
                candidates.append((version, device["name"], device["udid"]))
    if not candidates:
        raise ValueError("No available iPhone simulator. Install an iOS runtime in Xcode.")
    return max(candidates)[2]


if __name__ == "__main__":
    try:
        result = subprocess.run(
            ["xcrun", "simctl", "list", "devices", "available", "--json"],
            check=True, capture_output=True, text=True,
        )
        print(choose(json.loads(result.stdout)["devices"]))
    except (subprocess.CalledProcessError, ValueError, KeyError) as error:
        print(f"Simulator selection failed: {error}", file=sys.stderr)
        sys.exit(1)
