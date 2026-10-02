"""Transparent rule-based sector labels for actively traded Korean stocks."""

SECTOR_TERMS = {
    '반도체': ['삼성전자','SK하이닉스','DB하이텍','한미반도체','HPSP','리노공업','ISC','테크윙','주성엔지니어링','원익IPS','유진테크','제주반도체','심텍','대덕전자','이수페타시스','가온칩스','에이직랜드','넥스트칩'],
    '방산·항공우주': ['한화에어로스페이스','현대로템','LIG넥스원','한화시스템','한국항공우주','KAI','쎄트렉아이','풍산','SNT다이내믹스','휴니드'],
    '조선·해운': ['한화오션','삼성중공업','HD한국조선해양','HD현대중공업','HD현대미포','현대힘스','세진중공업','HMM','팬오션','대한해운'],
    '전력·원전': ['HD현대일렉트릭','효성중공업','LS ELECTRIC','산일전기','제룡전기','일진전기','대한전선','가온전선','LS에코에너지','두산에너빌리티','한전기술','한전KPS','우리기술','비에이치아이','우진'],
    '2차전지': ['LG에너지솔루션','삼성SDI','에코프로비엠','에코프로','포스코퓨처엠','엘앤에프','금양','SK아이이테크놀로지','나노신소재','대주전자재료','천보','엔켐','피엔티','윤성에프앤씨'],
    '바이오·헬스케어': ['삼성바이오로직스','셀트리온','알테오젠','리가켐바이오','HLB','유한양행','한미약품','보령','대웅제약','에이비엘바이오','펩트론','오스코텍','휴젤','파마리서치','클래시스'],
    '로봇·자동화': ['레인보우로보틱스','두산로보틱스','로보티즈','에스피지','로보스타','유일로보틱스','뉴로메카','티로보틱스','하이젠알앤엠','에스비비테크'],
    '자동차': ['현대차','기아','현대모비스','HL만도','한온시스템','현대위아','에스엘','서연이화','화신','성우하이텍','명신산업'],
    '인터넷·게임': ['NAVER','카카오','크래프톤','넷마블','엔씨소프트','펄어비스','카카오게임즈','위메이드','SOOP','더블유게임즈'],
    '엔터·콘텐츠': ['하이브','HYBE','JYP Ent.','에스엠','와이지엔터테인먼트','스튜디오드래곤','CJ ENM','디어유','콘텐트리중앙'],
    '화장품': ['아모레퍼시픽','LG생활건강','에이피알','코스맥스','한국콜마','클리오','실리콘투','브이티','마녀공장','아이패밀리에스씨'],
    '금융': ['KB금융','신한지주','하나금융지주','우리금융지주','카카오뱅크','기업은행','메리츠금융지주','미래에셋증권','한국금융지주','삼성증권','키움증권','NH투자증권','삼성화재','DB손해보험','현대해상','한화생명','삼성생명'],
    '식품·유통': ['삼양식품','농심','오리온','CJ제일제당','동원F&B','대상','풀무원','빙그레','롯데웰푸드','BGF리테일','GS리테일','이마트','호텔신라'],
    '건설·기계': ['현대건설','대우건설','DL이앤씨','GS건설','HDC현대산업개발','두산밥캣','HD현대인프라코어','HD현대건설기계','두산'],
    '철강·소재': ['POSCO홀딩스','현대제철','동국제강','고려아연','영풍','세아베스틸지주','TCC스틸','포스코엠텍'],
    '화학·정유': ['LG화학','롯데케미칼','금호석유','한화솔루션','SK이노베이션','S-Oil','GS','OCI홀딩스','효성티앤씨'],
    '통신': ['SK텔레콤','KT','LG유플러스','케이엠더블유','쏠리드'],
    '항공·여행': ['대한항공','아시아나항공','제주항공','진에어','티웨이항공','하나투어','모두투어'],
}

GENERIC_TERMS = {
    '금융': ['금융지주','증권','손해보험','생명보험'],
    '조선·해운': ['조선','해운'],
    '바이오·헬스케어': ['바이오','제약'],
    '로봇·자동화': ['로봇'],
}


def classify_sector(name: str) -> str:
    normalized=(name or '').replace(' ','').lower()
    for sector,names in SECTOR_TERMS.items():
        if any(term.replace(' ','').lower() in normalized for term in names):
            return sector
    for sector,terms in GENERIC_TERMS.items():
        if any(term.replace(' ','').lower() in normalized for term in terms):
            return sector
    return '기타'


def build_sector_ranking(rows: list[dict]) -> list[dict]:
    groups={}
    for row in rows:
        sector=row.get('sector','기타')
        if sector=='기타':
            continue
        groups.setdefault(sector,[]).append(row)
    ranked=[]
    for sector,members in groups.items():
        # More representatives improve reliability without allowing group size
        # to overwhelm the actual stock scores.
        average=sum(float(x.get('score',0)) for x in members)/len(members)
        breadth=min(5,len(members))*1.5
        score=round(min(100,average+breadth),1)
        ranked.append({'sector':sector,'score':score,
            'change':round(sum(float(x.get('change',0)) for x in members)/len(members),2),
            'leaders':[x['name'] for x in sorted(members,key=lambda x:x.get('score',0),reverse=True)[:3]],
            'count':len(members)})
    return sorted(ranked,key=lambda x:(x['score'],x['count']),reverse=True)[:10]
