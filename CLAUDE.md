# 프로젝트: 주식 시황 브리핑 봇

## 프로젝트 목표
- AI / 블록체인 / 제조업 섹터의 뉴스를 매일 수집한다.
- AI가 사용자의 관심사 기준으로 중요한 뉴스만 골라 요약한다.
- 최종적으로 이메일로 요약 결과를 받아본다.

## 사용자 정보
- 코딩 완전 초보자. 파이썬 문법이나 개발 용어를 안다고 가정하지 않는다.

## 진행 규칙 (반드시 지킬 것)
1. **한 번에 한 단계씩만 진행한다.** 각 단계가 끝나면 사용자가 확인/승인할 때까지 다음 단계로 넘어가지 않는다.
2. **코드를 작성할 때마다 그 코드가 어떤 역할을 하는지 쉬운 말로 설명한다.** 전문 용어를 쓸 경우 풀어서 설명한다.
3. 이 규칙 파일(CLAUDE.md)을 계속 참고하고, 프로젝트 진행 상황이 바뀌면 이 파일을 업데이트한다.

## 진행 상황 로그
- [x] 1단계: 파이썬 설치 확인 (Python 3.9.6 설치됨) 및 프로젝트 폴더 구조 생성 완료
  - `news_collector/`: 뉴스 수집 코드
  - `summarizer/`: AI 요약 코드
  - `notifier/`: 이메일 발송 코드
  - `data/`: 수집한 데이터 임시 저장
- [x] 2단계: 뉴스 소스 결정 (국내 뉴스 위주, 네이버 뉴스 검색 API 사용) + API 키 발급 + `.env` 설정 완료
- [x] 3단계: 네이버 뉴스 API 연결 테스트 코드 작성 및 성공 확인 (`news_collector/test_connection.py`)
- [x] 4단계: 키워드(AI/블록체인/제조업)별 뉴스 수집 후 `data/news_날짜.json`에 저장하는 코드 작성 (`news_collector/collect_news.py`)
- [x] 5단계: AI 요약 코드 작성 (`summarizer/summarize_news.py`, Claude API 사용)
- [x] 6단계: 이메일 발송 코드 작성 및 테스트 성공 (`notifier/send_email.py`, Gmail 앱 비밀번호 사용, 발신/수신 모두 jameslee170943@gmail.com)
- [x] 7단계: 전체 파이프라인 연결 (`main.py` — 뉴스 수집 → AI 요약 → 이메일 발송 순서로 실행)
- [x] 8단계: Claude API 크레딧($5) 충전 후 전체 파이프라인 실행 테스트 성공 — 29건 수집 → AI가 중요 뉴스만 섹터별로 요약(제외 사유까지 설명) → 이메일 정상 발송 확인
- [x] 9단계: 깃허브 저장소(jameslee170943/-)에 초기 커밋 및 푸시 완료 (.env, data/는 .gitignore로 제외)
- [x] 10단계: 매일 오전 8시 자동 실행 설정 완료 (macOS launchd 사용, `scheduler/com.stockbriefingbot.daily.plist` → `~/Library/LaunchAgents/`에 등록, `launchctl bootstrap`으로 활성화). 실행 로그는 `logs/stdout.log`, `logs/stderr.log`에 기록됨
- [x] 11단계: AI 요약 프롬프트를 매크로/섹터/개별종목 우선순위 기반 분석 형식으로 교체 (`summarizer/summarize_news.py`)
- [x] 12단계: NewsAPI.org 연동해 미국 시장 뉴스 수집 추가 (`news_collector/collect_news.py` — 섹터별로 국내(네이버)/미국(NewsAPI) 뉴스를 함께 수집, 각 뉴스에 `source`(국내/해외) 필드 추가)
- [x] 13단계: 자동 실행 주기를 매일 → 월/수/금 오전 8시로 변경 (`scheduler/com.stockbriefingbot.daily.plist`의 `StartCalendarInterval`을 요일별 3개 항목으로 수정 후 launchd 재등록). 참고: 7/18~7/21 사이 Claude API 키가 무효화(401 오류)되어 요약/발송이 안 되고 있었음 — 사용자가 직접 콘솔에서 조치 예정
- [x] 14단계: 기준금리(국내 한국은행 + 미국 연준) 뉴스 수집 추가 (`news_collector/collect_news.py`의 `SECTORS`에 항목 추가), AI 요약 프롬프트에서 '매크로' 뉴스는 주식시장/AI 섹터/로봇 섹터 영향으로 세분화 분석하도록 개선 (`summarizer/summarize_news.py`). 분석 분량이 늘어나 `max_tokens`를 2000 → 4000으로 상향 조정
- [x] 15단계: 7/24(금) 자동 실행이 NewsAPI.org 연결 오류(일시적 네트워크 문제)로 실패해 이메일이 안 온 것을 확인, 수동 재실행으로 정상 작동 확인. 이 과정에서 요약이 항목 4개 추가 후에도 `max_tokens=4000`으로는 여전히 중간에 잘리는 것을 발견해 `8000`으로 재상향
- [x] 16단계: 뉴스 수집 시 네트워크 요청이 실패하면 5초 대기 후 최대 3번까지 자동 재시도하는 기능 추가 (`news_collector/collect_news.py`의 `request_with_retry()` 함수, 네이버·NewsAPI 요청 모두 적용)
- [x] 17단계: AI 요약 프롬프트에 '제외 기준' 항목 추가 (개인 신상/사법 처리 뉴스, 단순 홍보성 기사 등 주가에 실질적 영향이 없는 뉴스는 브리핑에서 제외하도록 명시) (`summarizer/summarize_news.py`)
- [x] 18단계: AI 요약 프롬프트의 '제외 기준'에 "당장 사업화·실적과 연결되지 않는 순수 연구/기술 트렌드성 뉴스" 항목 추가 (예: 학술 연구 발표, 실험실 단계 신소재/신기술) (`summarizer/summarize_news.py`)
- [x] 19단계: 대형 기업(아마존/엔비디아/구글/메타/삼성전자/SK하이닉스 등) 실적 발표 뉴스를 확실히 수집하기 위해 '실적 발표' 섹터 추가 (`news_collector/collect_news.py`). AI 요약 프롬프트에 '예정된 실적 발표'를 최우선 순위(0순위)로 추가해, 다가오는 실적 발표는 예외적으로 브리핑 맨 위에 배치하고 시장 기대감/시장 영향을 별도로 분석하도록 개선 (`summarizer/summarize_news.py`)
- [x] 20단계: 뉴스 수집 범위를 "최근 3일 이내" 기사로 제한 (`news_collector/collect_news.py`의 `DAYS_RANGE` 상수 추가 — 네이버는 응답받은 뒤 `pubDate` 기준으로 직접 필터링, NewsAPI는 요청 시 `from` 파라미터로 필터링)
- [x] 21단계: 기준금리 뉴스의 국내(네이버) 수집 정확도 개선. 기존에는 "기준금리" 단어만 검색어로 보내 본문에 스치듯 언급된 무관한 기사(적금 상품 홍보 등)까지 섞여 들어왔음. 네이버 API에 검색어를 따옴표로 감싸 보내면(`"기준금리"`) 정확한 문구 매칭이 된다는 것을 테스트로 확인, 적용함. 이를 위해 `collect_news.py`의 `SECTORS`에 `kr_query`(네이버에 실제로 보낼 검색어) 필드를 새로 추가하고 `fetch_news()`가 `keyword`(AI에게 보여줄 분류 이름)와 `query`(실제 검색어)를 분리해서 받도록 수정함 (미국 뉴스의 `us_query`와 동일한 구조)
- [x] 22단계: 8/14(금) 자동 실행이 AI 요약 단계에서 Claude API 연결 오류(`Connection reset by peer`, 일시적 네트워크 문제)로 실패해 이메일이 안 온 것을 확인. 뉴스 수집 단계에만 있던 재시도 기능(16단계)이 AI 요약 단계에는 없었던 것이 원인 — `summarizer/summarize_news.py`에 동일한 방식의 재시도 기능(`create_summary_with_retry()`, 최대 3번, 5초 대기) 추가
- [x] 23단계: '매크로' 뉴스 분석에서 '로봇 섹터 영향' 항목을 'IT 섹터 영향'으로 교체 (주식시장/AI 섹터/IT 섹터 영향 3가지 분석) (`summarizer/summarize_news.py`)
- [ ] 24단계: (다음 단계 진행 시 여기에 기록)

## 기술 스택 (진행하며 채워나감)
- 언어: Python 3.9.6
- 뉴스 수집: 네이버 뉴스 검색 API (국내) + NewsAPI.org (미국, 영어 키워드 검색)
- AI 요약: Claude API (claude-opus-4-8)
- 알림 발송: 이메일 (Gmail SMTP, 앱 비밀번호 사용)

## 설치된 패키지
- requests: 외부 API(웹 서버)에 요청을 보내고 응답을 받는 데 사용
- python-dotenv: `.env` 파일에 저장된 비밀 값(API 키 등)을 코드에서 읽어오는 데 사용
- anthropic: Claude API를 파이썬 코드에서 사용하기 위한 공식 패키지
