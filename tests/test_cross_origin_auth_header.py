from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


class CrossOriginAuthHeaderTests(unittest.TestCase):
    def test_fetch_wrapper_only_adds_authorization_for_same_origin_requests(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('if (tok && _sameOrigin(url)) _setHeader(opts.headers, \'Authorization\', \'Bearer \' + tok);', html)


if __name__ == '__main__':
    unittest.main()
