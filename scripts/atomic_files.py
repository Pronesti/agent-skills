"""Atomic file writes shared by the installer scripts."""
import os
from pathlib import Path
import tempfile


def write_atomic(target, content, mode, *, replace):
    """Write bytes to target through a temporary file in the same directory.

    With replace=True an existing file is swapped atomically. With replace=False the
    file is created exclusively; returns False, leaving the target untouched, when it
    appeared concurrently. Returns True when the content was written.
    """
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f'.{target.name}-',
                                         delete=False) as output:
            temporary = Path(output.name)
            output.write(content)
        temporary.chmod(mode)
        if replace:
            temporary.replace(target)
        else:
            try:
                os.link(temporary, target)
            except FileExistsError:
                return False
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return True
