"""
관심 키워드(AI, 블록체인, 제조업)로 네이버 뉴스를 검색해서
data/ 폴더에 오늘 날짜 파일로 저장하는 코드입니다.
"""

import os
import json
from datetime import date
from dotenv import load_dotenv
import requests

load_dotenv()

CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# 관심 있는 분야 키워드 목록입니다. 나중에 필요하면 여기에 단어를 추가/삭제하면 돼요.
KEYWORDS = ["AI", "블록체인", "제조업"]


def clean_html(text):
    """네이버 API가 제목/설명에 섞어 보내는 HTML 태그를 사람이 읽기 좋게 정리합니다."""
    return (
        text.replace("<b>", "")
        .replace("</b>", "")
        .replace("&quot;", '"')
        .replace("&amp;", "&")
    )


def fetch_news(keyword, display=10):
    """네이버 뉴스 검색 API에 특정 키워드로 뉴스를 요청하고, 결과를 정리해서 돌려줍니다."""
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
    }
    params = {
        "query": keyword,
        "display": display,  # 키워드당 몇 개의 뉴스를 가져올지
        "sort": "date",       # 최신순 정렬
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # 요청이 실패하면 여기서 에러를 발생시켜 바로 알 수 있게 합니다.

    items = response.json()["items"]

    cleaned_items = []
    for item in items:
        cleaned_items.append(
            {
                "keyword": keyword,
                "title": clean_html(item["title"]),
                "description": clean_html(item["description"]),
                "link": item["link"],
                "pubDate": item["pubDate"],
            }
        )
    return cleaned_items


def main():
    all_news = []

    for keyword in KEYWORDS:
        print(f"'{keyword}' 뉴스 수집 중...")
        news_items = fetch_news(keyword)
        all_news.extend(news_items)
        print(f"  -> {len(news_items)}건 수집 완료")

    today_str = date.today().isoformat()
    save_path = f"data/news_{today_str}.json"

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 총 {len(all_news)}건의 뉴스를 '{save_path}' 파일에 저장했어요.")


if __name__ == "__main__":
    main()
