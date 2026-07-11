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
    "너는 국내 투자자를 위한 시황 브리핑 애널리스트다.\n"
    "수집된 뉴스 중 투자자에게 중요한 것을 아래 우선순위로 선별하라.\n"
    "\n"
    "[선별 기준 - 우선순위 순]\n"
    "1. 매크로: 시장 전체에 영향을 주는 뉴스\n"
    "   (미중 관계, 금리, 환율, 원자재, 지정학 이벤트 등)\n"
    "2. 섹터: 특정 산업 전체에 영향을 주는 뉴스\n"
    "   (해외 기업/기관 발표라도 국내 섹터에 파급되면 반드시 포함할 것.\n"
    "    예: 미국 반도체 기업 실적/전망 → 국내 반도체주 영향)\n"
    "3. 개별 종목: 특정 기업의 주가에 영향을 주는 뉴스\n"
    "\n"
    "[각 뉴스마다 아래 형식으로 작성]\n"
    "- 제목:\n"
    "- 분류: (매크로 / 섹터 / 개별종목)\n"
    "- 시장 영향 분석: 이 뉴스가 시장 또는 해당 섹터·종목에\n"
    "  어떻게 작용할 것으로 기대되는지 한 문장으로.\n"
    "- 링크:\n"
    "\n"
    "[주의]\n"
    "- 이미 다 알려진 예정된 일정보다, 예상을 벗어난 이벤트를 우선하라.\n"
    "- 단순 주가 등락 보도보다 '원인과 배경'이 담긴 뉴스를 우선하라."
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
