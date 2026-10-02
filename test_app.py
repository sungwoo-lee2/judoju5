import unittest
from fastapi.testclient import TestClient
import app as webapp


class HomeCompatibilityTests(unittest.TestCase):
    def test_old_early_leader_without_optional_fields_renders(self):
        original = webapp.get_snapshot
        webapp.get_snapshot = lambda: {
            'items': [],
            'early_leaders': [{
                'ticker': '000000', 'name': '테스트', 'sector': '미분류',
                'early_rank': 1, 'early_score': 50,
            }],
        }
        try:
            response = TestClient(webapp.app).get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('초기 주도주 후보', response.text)
        finally:
            webapp.get_snapshot = original


if __name__ == '__main__':
    unittest.main()
