"""
오늘자 뉴스 요약(summary_날짜.txt)을 이메일로 보내는 코드입니다.
아직 요약 파일이 없으면, 테스트용 메시지를 대신 보냅니다.
"""

import os
import smtplib
from email.mime.text import MIMEText
from datetime import date
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

today_str = date.today().isoformat()
summary_path = f"data/summary_{today_str}.txt"

if os.path.exists(summary_path):
    with open(summary_path, encoding="utf-8") as f:
        body = f.read()
else:
    body = "(아직 AI 요약본이 없어서, 이메일 발송 기능만 테스트하는 메시지입니다.)"

# 이메일의 제목, 보내는 사람, 받는 사람을 설정합니다.
message = MIMEText(body)
message["Subject"] = f"[주식 시황 브리핑] {today_str}"
message["From"] = GMAIL_ADDRESS
message["To"] = GMAIL_ADDRESS

# 구글 이메일 서버에 로그인해서 실제로 메일을 발송합니다.
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()  # 통신 내용을 암호화합니다.
    server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
    server.send_message(message)

print(f"✅ '{GMAIL_ADDRESS}' 로 이메일을 보냈어요.")
