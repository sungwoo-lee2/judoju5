import unittest
from unittest.mock import patch
import analytics_v7 as a


class AnalyticsConnectionTests(unittest.TestCase):
    def test_lifecycle_and_performance_start_on_first_scan(self):
        state={'days':[],'tracks':{},'detections':{}}
        def save(value):
            state.clear();state.update(value);return 'test'
        row={'ticker':'000001','name':'테스트','sector':'반도체','score':80,
             'close':10000,'stage':'일별 후보','change':1,'amount':1}
        with patch.object(a,'_load',side_effect=lambda:state),patch.object(a,'_save',side_effect=save),patch.object(a,'_date_key',return_value='2026-10-02'):
            lifecycle,rotations,performance=a.update_history([row],[row],[])
        self.assertEqual(lifecycle[0]['lifecycle_status'],'오늘 첫 포착')
        self.assertEqual(rotations,[])
        self.assertEqual(performance['total'],1)
        self.assertEqual(performance['detections'][0]['current_return'],0)


if __name__=='__main__': unittest.main()
