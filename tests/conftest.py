"""Pytest harness configuration.

Keep repo-root modules importable for legacy tests that import modules such as
`server`, `backup`, and `kwr_backend` directly.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
