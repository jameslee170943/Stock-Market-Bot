"""
"뉴스 수집 -> AI 요약 -> 이메일 발송"을 순서대로 한 번에 실행하는 파일입니다.
이 파일 하나만 실행하면 전체 과정이 자동으로 진행됩니다.
"""

import subprocess
import sys

steps = [
    ("뉴스 수집", ["python3", "news_collector/collect_news.py"]),
    ("AI 요약", ["python3", "summarizer/summarize_news.py"]),
    ("이메일 발송", ["python3", "notifier/send_email.py"]),
]

for step_name, command in steps:
    print(f"\n===== {step_name} 시작 =====")
    result = subprocess.run(command)

    # 이전 단계가 실패하면(에러가 나면), 다음 단계로 넘어가지 않고 여기서 멈춥니다.
    if result.returncode != 0:
        print(f"\n❌ '{step_name}' 단계에서 문제가 생겨서 멈췄어요.")
        sys.exit(1)

print("\n✅ 모든 단계가 끝났어요!")
