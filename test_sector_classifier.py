import unittest
from sector_classifier import classify_sector, build_sector_ranking


class SectorClassifierTests(unittest.TestCase):
    def test_major_names(self):
        expected={'SK하이닉스':'반도체','한화오션':'조선·해운','두산에너빌리티':'전력·원전',
            '알테오젠':'바이오·헬스케어','KB금융':'금융','에이피알':'화장품'}
        for name,sector in expected.items(): self.assertEqual(classify_sector(name),sector)
        self.assertEqual(classify_sector('분류근거없는회사'),'기타')

    def test_sector_ranking(self):
        rows=[{'name':'A','sector':'반도체','score':90,'change':3},
              {'name':'B','sector':'반도체','score':80,'change':1},
              {'name':'C','sector':'기타','score':99,'change':9},
              {'name':'D','sector':'조선·해운','score':70,'change':2}]
        result=build_sector_ranking(rows)
        self.assertEqual(result[0]['sector'],'반도체')
        self.assertEqual(result[0]['leaders'],['A','B'])
        self.assertNotIn('기타',[x['sector'] for x in result])


if __name__=='__main__': unittest.main()
