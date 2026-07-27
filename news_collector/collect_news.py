"""
관심 키워드(AI, 블록체인, 제조업)로 네이버 뉴스를 검색해서
data/ 폴더에 오늘 날짜 파일로 저장하는 코드입니다.
"""

import os
import json
import time
from datetime import date
from dotenv import load_dotenv
import requests

load_dotenv()

CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# 관심 있는 분야별로, 국내(네이버) 검색어와 미국(NewsAPI) 검색어를 짝지어둔 목록입니다.
SECTORS = [
    {"keyword": "AI", "us_query": "artificial intelligence"},
    {"keyword": "블록체인", "us_query": "blockchain"},
    {"keyword": "제조업", "us_query": "semiconductor manufacturing"},
    {"keyword": "기준금리", "us_query": "Federal Reserve interest rate"},
]


def clean_html(text):
    """네이버 API가 제목/설명에 섞어 보내는 HTML 태그를 사람이 읽기 좋게 정리합니다."""
    return (
        text.replace("<b>", "")
        .replace("</b>", "")
        .replace("&quot;", '"')
        .replace("&amp;", "&")
    )


def request_with_retry(url, headers=None, params=None, retries=3, delay=5):
    """네트워크 요청이 실패하면, 잠시 기다렸다가 최대 retries번까지 다시 시도합니다."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == retries:
                raise
            print(f"  ⚠️ 요청 실패 (시도 {attempt}/{retries}): {e}")
            print(f"  {delay}초 후 다시 시도할게요...")
            time.sleep(delay)


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

    response = request_with_retry(url, headers=headers, params=params)

    items = response.json()["items"]

    cleaned_items = []
    for item in items:
        cleaned_items.append(
            {
                "keyword": keyword,
                "source": "국내",
                "title": clean_html(item["title"]),
                "description": clean_html(item["description"]),
                "link": item["link"],
                "pubDate": item["pubDate"],
            }
        )
    return cleaned_items


def fetch_us_news(keyword, us_query, page_size=10):
    """NewsAPI.org에 영어 검색어로 요청해서, 미국 뉴스를 가져와 정리해서 돌려줍니다."""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": us_query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": NEWSAPI_KEY,
    }

    response = request_with_retry(url, params=params)

    articles = response.json()["articles"]

    cleaned_items = []
    for article in articles:
        cleaned_items.append(
            {
                "keyword": keyword,
                "source": "해외",
                "title": article["title"],
                "description": article["description"] or "",
                "link": article["url"],
                "pubDate": article["publishedAt"],
            }
        )
    return cleaned_items


def main():
    all_news = []

    for sector in SECTORS:
        keyword = sector["keyword"]

        print(f"'{keyword}' 국내 뉴스 수집 중...")
        news_items = fetch_news(keyword)
        all_news.extend(news_items)
        print(f"  -> {len(news_items)}건 수집 완료")

        print(f"'{keyword}' 미국 뉴스 수집 중...")
        us_news_items = fetch_us_news(keyword, sector["us_query"])
        all_news.extend(us_news_items)
        print(f"  -> {len(us_news_items)}건 수집 완료")

    today_str = date.today().isoformat()
    save_path = f"data/news_{today_str}.json"

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 총 {len(all_news)}건의 뉴스를 '{save_path}' 파일에 저장했어요.")


if __name__ == "__main__":
    main()
