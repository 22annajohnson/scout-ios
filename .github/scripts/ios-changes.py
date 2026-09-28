#!/usr/bin/env python3
"""Skip macOS only for known documentation-only changes; default to running it."""
import os
import subprocess


def should_run(event, base, head):
    if event == "workflow_dispatch" or not base or set(base) == {"0"}:
        return True
    try:
        # --no-renames retains both paths, so moving source to docs still runs CI.
        result = subprocess.run(
            ["git", "diff", "--no-renames", "--name-only", "-z", base, head, "--"],
            check=True, capture_output=True,
        )
    except subprocess.CalledProcessError:
        return True
    paths = result.stdout.split(b"\0")
    return any(path and not path.lower().endswith(b".md") for path in paths)


if __name__ == "__main__":
    run = should_run(
        os.environ.get("EVENT_NAME", ""),
        os.environ.get("BASE_SHA", ""),
        os.environ.get("HEAD_SHA", "HEAD"),
    )
    value = str(run).lower()
    print(f"Run iOS build and tests: {value}")
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        output.write(f"should-run-ios={value}\n")
