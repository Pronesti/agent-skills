#!/usr/bin/env python3
"""Compare pinned author revisions with remote HEADs without changing files."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def check(entry):
    name, source = entry
    result = {"source": name, "pinned": source["revision"]}
    try:
        remote = subprocess.run(
            ["git", "ls-remote", source["url"], "HEAD"],
            capture_output=True, text=True, check=True, timeout=45,
        ).stdout.split()[0]
        result.update(remote=remote, status="current" if remote == source["revision"] else "review_update")
    except (subprocess.SubprocessError, OSError, IndexError) as exc:
        result.update(status="check_failed", error=str(exc))
    return result


if __name__ == "__main__":
    sources = json.loads((ROOT / "upstreams.json").read_text())["sources"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, sources.items()))
    print(json.dumps(results, indent=2))
    sys.exit(1 if any(r["status"] == "check_failed" for r in results) else 0)
