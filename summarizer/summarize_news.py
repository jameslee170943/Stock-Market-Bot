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
    "0. 예정된 실적 발표: 아마존, 엔비디아, 구글(알파벳), 메타, 삼성전자,\n"
    "   SK하이닉스 등 시장에 영향력이 큰 대형 기업의 실적 발표가\n"
    "   이번 주(가까운 시일 내)로 예정되어 있다는 뉴스가 있다면,\n"
    "   다른 어떤 뉴스보다도 브리핑 맨 위에 배치할 것.\n"
    "   (뒤의 [주의] 항목에 있는 '예정된 일정보다 예상 밖 이벤트를 우선하라'는\n"
    "    규칙의 예외로 취급한다 — 대형 기업 실적 발표는 예정된 일정이어도 중요하다.)\n"
    "1. 매크로: 시장 전체에 영향을 주는 뉴스\n"
    "   (미중 관계, 금리, 환율, 원자재, 지정학 이벤트 등)\n"
    "2. 섹터: 특정 산업 전체에 영향을 주는 뉴스\n"
    "   (해외 기업/기관 발표라도 국내 섹터에 파급되면 반드시 포함할 것.\n"
    "    예: 미국 반도체 기업 실적/전망 → 국내 반도체주 영향)\n"
    "3. 개별 종목: 특정 기업의 주가에 영향을 주는 뉴스\n"
    "\n"
    "[각 뉴스마다 아래 형식으로 작성]\n"
    "- 제목:\n"
    "- 분류: (예정된 실적 발표 / 매크로 / 섹터 / 개별종목)\n"
    "  · '예정된 실적 발표'로 분류한 뉴스는 아래 2가지 항목으로 나누어 작성할 것:\n"
    "    - 시장 기대감: 실적 컨센서스(시장 예상치)나 투자자들의 기대 수준.\n"
    "    - 시장 영향: 실적 결과에 따라 국내 증시·관련 섹터에 어떻게\n"
    "      작용할 수 있는지.\n"
    "- 시장 영향 분석:\n"
    "  · '매크로'로 분류한 뉴스(기준금리, 환율, 원자재, 지정학 이벤트 등)는\n"
    "    아래 3가지 항목으로 나누어 분석할 것 (해당 사항이 없으면 '해당 없음'이라고 쓸 것):\n"
    "    - 주식시장 영향:\n"
    "    - AI 섹터 영향:\n"
    "    - 로봇 섹터 영향:\n"
    "  · '섹터'/'개별종목'으로 분류한 뉴스는 위처럼 나누지 말고,\n"
    "    기존처럼 한 문장으로 작성할 것.\n"
    "- 링크:\n"
    "\n"
    "[주의]\n"
    "- 이미 다 알려진 예정된 일정보다, 예상을 벗어난 이벤트를 우선하라.\n"
    "- 단순 주가 등락 보도보다 '원인과 배경'이 담긴 뉴스를 우선하라.\n"
    "\n"
    "[제외 기준]\n"
    "아래에 해당하는 뉴스는 브리핑에서 제외하라:\n"
    "- 회사나 산업 전체가 아닌 개인의 신상/사법 처리에 그치는 뉴스\n"
    "  (예: 직원 개인의 기술 유출·횡령 등으로 인한 형사 처벌 소식 —\n"
    "   회사의 실적·전략·주가에 직접적인 영향을 준다는 근거가 없다면 제외)\n"
    "- 단순 홍보, 광고성 기사, 행사 참석/인사말 소식\n"
    "- 당장 사업화·실적과 연결되지 않는 순수 연구/기술 트렌드성 뉴스\n"
    "  (예: 학술 연구 발표, 실험실 단계의 신소재·신기술 —\n"
    "   특정 기업의 사업·매출·투자 계획과 명확히 연결되지 않으면 제외)\n"
    "- 주가나 산업 동향에 실질적인 영향을 준다고 보기 어려운 뉴스"
)

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=8000,
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
