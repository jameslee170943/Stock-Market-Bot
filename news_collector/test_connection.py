"""
네이버 뉴스 검색 API가 잘 연결되는지 확인해보는 테스트 코드입니다.
"AI"라는 단어로 뉴스를 검색해서, 결과가 잘 오는지만 확인합니다.
"""

import os
from dotenv import load_dotenv
import requests

# .env 파일에 적어둔 값들을 이 프로그램 안으로 불러옵니다.
load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

# 키가 아예 없으면 여기서 바로 알려주고 멈춥니다.
if not client_id or not client_secret:
    print("❌ .env 파일에서 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 값을 찾을 수 없어요.")
    print("   .env 파일이 프로젝트 최상위 폴더에 있는지, 값이 채워져 있는지 확인해주세요.")
    raise SystemExit(1)

# 네이버 뉴스 검색 API 주소입니다.
url = "https://openapi.naver.com/v1/search/news.json"

# 네이버에게 "나 이 키 가진 사람이야"라고 알려주는 부분입니다.
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret,
}

# 어떤 검색어로, 몇 개의 결과를 가져올지 지정합니다.
params = {
    "query": "AI",
    "display": 3,   # 결과 3개만 받아봅니다.
    "sort": "date",  # 최신순으로 정렬합니다.
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    print("✅ 연결 성공! 최신 'AI' 뉴스 3개를 가져왔어요.\n")
    items = response.json()["items"]
    for i, item in enumerate(items, start=1):
        # 제목에 섞인 HTML 태그(<b>, </b> 등)를 간단히 제거합니다.
        title = item["title"].replace("<b>", "").replace("</b>", "").replace("&quot;", '"')
        print(f"{i}. {title}")
else:
    print(f"❌ 연결 실패 (상태 코드: {response.status_code})")
    print(response.text)
