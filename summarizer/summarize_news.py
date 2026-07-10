"""
data/ 폴더에 저장된 오늘자 뉴스를 Claude(AI)에게 보내서,
AI/블록체인/제조업 투자 관점에서 중요한 뉴스만 골라 요약받는 코드입니다.
"""

import os
import json
from datetime import date
from dotenv import load_dotenv
import anthropic

load_dotenv()

today_str = date.today().isoformat()
news_path = f"data/news_{today_str}.json"

# 오늘 수집한 뉴스 파일이 없으면, 먼저 collect_news.py를 실행하라고 안내합니다.
if not os.path.exists(news_path):
    print(f"❌ '{news_path}' 파일이 없어요. 먼저 news_collector/collect_news.py를 실행해주세요.")
    raise SystemExit(1)

with open(news_path, encoding="utf-8") as f:
    news_items = json.load(f)

# 뉴스 목록을 AI가 읽기 좋은 하나의 긴 텍스트로 정리합니다.
news_text = ""
for item in news_items:
    news_text += f"[{item['keyword']}] {item['title']}\n{item['description']}\n{item['link']}\n\n"

client = anthropic.Anthropic()  # .env의 ANTHROPIC_API_KEY를 자동으로 읽어옵니다.

# AI에게 역할과 판단 기준을 알려주는 지침입니다.
system_prompt = (
    "당신은 개인 투자자를 위한 주식 시황 브리핑 어시스턴트입니다. "
    "사용자는 AI, 블록체인, 제조업 3개 섹터의 국내 뉴스에 관심이 있습니다. "
    "아래 뉴스 목록 중에서 주가나 산업 동향에 실질적인 영향을 줄 만큼 "
    "중요한 뉴스만 골라, 섹터별로 나누어 한국어로 간결하게 요약해주세요. "
    "중요하지 않은 뉴스(단순 홍보, 광고성 기사 등)는 제외하세요. "
    "각 항목은 '- 제목 요약: 왜 중요한지 한 줄' 형식으로 작성하고, 끝에 링크를 붙여주세요."
)

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=2000,
    system=system_prompt,
    messages=[{"role": "user", "content": news_text}],
)

summary_text = next(block.text for block in response.content if block.type == "text")

print(summary_text)

# 나중에 텔레그램/이메일로 보낼 수 있도록 요약 결과도 파일로 저장해둡니다.
summary_path = f"data/summary_{today_str}.txt"
with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary_text)

print(f"\n✅ 요약 결과를 '{summary_path}' 파일에도 저장했어요.")
