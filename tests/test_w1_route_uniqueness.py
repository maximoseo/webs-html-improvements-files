from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / 'server.py'

TOUCHED_HANDLER_PATTERNS = [
    "if parsed.path in ('/api/auth/request-reset', '/api/reset-password'):",
    "if parsed.path == '/api/auth/reset':",
    "if parsed.path == '/api/n8n-fixer/validate':",
    "if parsed.path == '/api/kwr/start':",
    "if parsed.path == '/api/kwr/swarm':",
    "if parsed.path == '/api/dashboard/clear-cache':",
    "if parsed.path == '/api/projects/star':",
    "if parsed.path == '/api/settings/theme':",
]


def test_w1_touched_post_route_handlers_are_unique_and_after_real_do_post():
    source = SERVER.read_text(encoding='utf-8')
    do_post_pos = source.index('    def do_POST(self):')
    assert source.count('    def do_POST(self):') == 1
    for pattern in TOUCHED_HANDLER_PATTERNS:
        positions = []
        start = 0
        while True:
            pos = source.find(pattern, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        assert len(positions) == 1, f'{pattern} appears {len(positions)} times at {positions}'
        assert positions[0] > do_post_pos, f'{pattern} appears before active do_POST'
