# Channel ALF Readiness Auditor

## 개요

`channel-alf-readiness-auditor`는 채널톡 ALF 배포 전에 FAQ, 정책 문서, 상담 규칙, 시스템 초안이 AI 상담 자동화에 적합한지 감사하고 점수, 판정, 위험 항목, 보완 질문, 테스트 고객 질문을 생성하는 Codex 플러그인입니다.

이 플러그인은 고객에게 직접 답변하는 챗봇이 아닙니다. ALF 배포 전 고객사의 문서와 규칙 준비도를 운영 관점에서 점검하는 감사 도구입니다.

## 해결하려는 문제

ALF는 단순 FAQ 요약기가 아니라 지식, 규칙, 시스템 실행, 상담원 연결 조건을 바탕으로 고객 상담 자동화를 수행하는 제품입니다.

고객사의 FAQ, 배송/교환/반품/환불 정책, 상담 매크로, 시스템 조건이 불완전하거나 서로 충돌하면 ALF가 위험한 답변이나 실행을 할 수 있습니다. 예를 들어 배송 예정일을 확정할 근거가 없는데 확답하거나, 환불 가능 여부를 잘못 안내하거나, 단순 정책 문의를 실제 주문 취소 요청으로 오인할 수 있습니다.

이 플러그인은 ALF 배포 전 준비도 평가를 6축 기준으로 고정해 지식 누락, 정책 충돌, 위험 답변, 상담원 연결 기준, 시스템 트리거 위험, 문서 구조 문제를 찾습니다.

## 공개 근거

사용한 공개 URL:

```text
https://channel.io/kr
https://channel.io/kr/alf-customer
https://channel.io/kr/documents
```

채널톡 공식 공개 페이지는 ALF가 반복 문의 응답, 지식 사용, 규칙 적용, 태스크 실행, 상담원 연결과 관련된 AI 에이전트임을 설명합니다. ALF 고객 페이지는 RAG 지식, rule filter, task trigger, code node, 성과 지표, human handoff 등을 설명합니다. Documents 페이지는 채널톡 Documents가 ALF의 지식 데이터베이스로 사용될 수 있음을 설명합니다.

이 공개 자료는 제품 구조를 설명하는 근거입니다. 실제 고객사의 비공개 정책 문서, 내부 ALF 평가 기준, 실제 성과 수치는 제공하지 않습니다.

## 사용자

- 채널톡 도입을 돕는 컨설턴트
- ALF 후보 고객 담당자
- ALF 세팅 담당자
- 고객사의 CX 리드
- CS 매니저
- 운영팀

## 사용 상황

- ALF 최초 배포 전
- FAQ와 정책 문서를 ALF 지식으로 연결하기 전
- 배송, 교환, 반품, 환불, 주문 취소 같은 반복 문의를 자동화하기 전
- 상담원 연결 조건을 정리할 때
- 주문 취소, 예약 변경, 환불 요청 같은 시스템 트리거 초안을 평가할 때
- 고객 질문 테스트셋을 만들 때

## 작동 방식

1. 사용자가 FAQ, 정책 문서, 상담 매크로, ALF 규칙 초안, 시스템 트리거 초안, 고객 질문 목록 또는 공개 URL을 제공합니다.
2. `audit-alf-readiness` 스킬이 운영 관점에서 문서와 규칙을 분석합니다.
3. 6축 기준으로 findings JSON을 만듭니다.
4. `src/skills/audit-alf-readiness/scripts/score.py`가 같은 입력에 대해 같은 점수와 판정을 내는 결정론적 결과를 생성합니다.
5. 최종 출력은 점수, 판정, 위험 플래그, 판정 근거, 보완 항목, 상담원 연결 규칙, 시스템 자동화 규칙, 문서 개선안, 테스트 고객 질문을 포함합니다.

## 일반 Codex 질문과의 차이

일반 Codex 질문은 문서를 요약할 수 있습니다. 이 플러그인은 ALF 배포 준비도라는 고정된 감사 프레임을 사용합니다.

단순 요약이 아니라 ALF가 답변하거나 실행하기 전에 위험한 지식 누락, 정책 충돌, 위험 답변, 상담원 연결 기준, 시스템 트리거 안전성, 문서 구조 문제를 찾습니다. 출력도 고객 답변이 아니라 운영자용 준비도 리포트입니다.

## 6축 감사 기준

축 이름은 `score.py`의 `AXES`와 일치합니다.

```text
knowledge_completeness
policy_consistency
answer_safety
handoff_clarity
task_trigger_safety
document_structure
```

1. `knowledge_completeness`
   - FAQ와 정책 문서가 반복 고객 질문을 충분히 커버하는지 확인합니다.
   - 배송, 취소, 교환, 반품, 환불, AS, 상품 사용, 쿠폰, 결제 기준을 확인합니다.

2. `policy_consistency`
   - FAQ, 약관, 이벤트 페이지, 상품 페이지, 상담 매크로 사이에 정책 충돌이 있는지 확인합니다.
   - 반품 가능 기간, 환불 제외 조건, 쿠폰 환불 처리, 이벤트 예외 조건을 확인합니다.

3. `answer_safety`
   - ALF가 확정할 수 없는 내용을 단정적으로 답할 위험이 있는지 확인합니다.
   - 배송 예정일 확답, 환불 가능성 보장, 재고 단정, 법률/의료/금융 조언을 주의합니다.

4. `handoff_clarity`
   - ALF가 상담원에게 연결해야 하는 조건이 문서화되어 있는지 확인합니다.
   - 결제 분쟁, 배송 사고, 환불 거절 이의 제기, 개인정보 변경, 법적 이슈, 강한 불만을 확인합니다.

5. `task_trigger_safety`
   - 주문 취소, 예약 변경, 환불 요청 같은 시스템 자동화 조건이 안전한지 확인합니다.
   - 고객의 명확한 실행 의도, 주문 식별자, 최종 확인 조건이 있는지 확인합니다.
   - 정책 질문만 하는 경우에는 실행 시스템을 트리거하지 않아야 합니다.

6. `document_structure`
   - ALF가 문서를 쉽게 참조할 수 있도록 제목, 조건, 예외, 절차, 상담원 연결 기준, 최신 수정일, 중복 문서가 정리되어 있는지 확인합니다.

## 판정 기준

`score.py` 로직과 일치합니다.

- `배포 가능`: 종합 점수 80 이상이고 missing, unclear, negative findings가 없으며 handoff/task 관련 점수가 기준 이상인 경우
- `보완 후 배포`: 치명적 negative는 없지만 누락, 불명확성, 낮은 위험의 정책 이슈가 남아 있어 보완이 필요한 경우
- `배포 보류`: `policy_consistency`, `answer_safety`, `task_trigger_safety` 축에 명시적 negative가 있어 정책 충돌, 위험 답변, 위험한 시스템 실행 조건이 확인된 경우

불명확한 항목은 risk flag로 남지만 명시적 negative가 아니면 바로 `배포 보류`로 처리하지 않습니다. 정보가 부족하면 추측하지 않고 `확인 불가` 또는 보완 항목으로 표시합니다.

## 출력 결과

최종 결과는 다음 항목을 포함합니다.

- 축별 점수
- 종합 점수
- 최종 판정
- 위험 플래그
- 판정 근거
- 누락된 지식
- 정책 충돌 가능성
- 위험 답변 가능성
- 상담원 연결 규칙
- 자동화 가능한 시스템
- 보류하거나 금지해야 할 시스템
- 문서 구조 개선안
- ALF 규칙 제안
- 테스트 고객 질문
- `확인 불가` 항목
- 근거 URL

## 예시 사용 흐름

`examples/alf-readiness-findings.json`은 synthetic 이커머스 고객사의 FAQ, 정책, 상담 규칙, 시스템 초안 예시입니다. 실제 고객 데이터나 채널톡 private log가 아닙니다.

예시에는 배송/교환/반품/환불 문서가 일부 있지만 부분 취소와 쿠폰 환불 기준, AS와 단순 반품 구분, 고액 환불 상담원 연결 기준, 주문 취소 전 최종 확인 조건이 부족한 상황이 들어 있습니다.

`score.py` 실행 결과는 overall score `61`, verdict `보완 후 배포`입니다. 정책 충돌 가능성과 배송 예정일 확답 위험은 risk flag로 남지만, 명시적 blocking negative가 아니므로 `배포 보류`가 아니라 `보완 후 배포`가 됩니다.

## 설치 방법

repo-local marketplace 설정은 다음 파일에 있습니다.

```text
.agents/plugins/marketplace.json
```

플러그인 소스:

```text
./src
```

스킬 이름:

```text
audit-alf-readiness
```

## 테스트 방법

`python`이 PATH에 있으면 다음 명령을 사용할 수 있습니다.

```powershell
python -m py_compile .\src\skills\audit-alf-readiness\scripts\score.py
python .\src\skills\audit-alf-readiness\scripts\score.py --self-test
python .\src\skills\audit-alf-readiness\scripts\score.py .\examples\alf-readiness-findings.json
Get-Content .\examples\alf-readiness-findings.json | python .\src\skills\audit-alf-readiness\scripts\score.py
```

현재 환경처럼 `python`이 PATH에 없으면 기존 검증에서 사용한 Codex bundled Python을 사용합니다.

## 제출 ZIP 구성

포함:

```text
src/
README.md
logs/
examples/
.agents/plugins/marketplace.json
```

선택:

```text
research/  # 실제 폴더가 있을 때만
```

제외:

```text
.git/
.codex/
__pycache__/
*.pyc
.venv/
node_modules/
cache/temp files
OS/editor temp files
submission.zip
```

`logs/` 전체 원본은 포함해야 합니다. `logs/codex/*.jsonl` 원본 로그를 제외하지 마세요. 기존 로그를 수정, 삭제, 요약본으로 대체하지 마세요. 기존 `submission.zip`이 zip 내부에 중첩 포함되지 않게 재생성해야 합니다.

## 한계

- 공개 자료 기반 감사이므로 채널톡 내부 ALF 평가 기준은 확인할 수 없습니다.
- synthetic sample은 실제 고객 데이터가 아닙니다.
- 실제 고객사의 비공개 정책 문서, 상담 로그, 시스템 실행 로그는 확인하지 않았습니다.
- 법무, 정책, 환불, 의료, 금융, 컴플라이언스 판단을 대체하지 않습니다.
- ALF 배포 여부의 최종 결정은 고객사 운영자와 담당자가 해야 합니다.
