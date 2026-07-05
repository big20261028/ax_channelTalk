---
name: audit-alf-readiness
description: 채널톡 ALF 배포 전 FAQ, 정책 문서, 상담 규칙, 시스템 초안을 운영자 관점에서 감사해 지식 누락, 정책 충돌, 위험 답변 가능성, 상담원 연결 조건, 시스템 자동화 위험, 문서 구조 개선안을 찾을 때 사용.
---

# Channel ALF Readiness Audit

## 목적

ALF 배포 전에 고객사의 FAQ, 정책 문서, 상담 규칙, 시스템 초안이 AI 상담 자동화에 적합한지 운영자 관점에서 감사한다.

이 스킬은 고객에게 직접 답변하는 용도가 아니다. 최종 결과는 고객 답변이 아니라 ALF 준비도 리포트다.

## 사용 대상

- 채널톡 도입 컨설턴트
- ALF 후보 고객 담당자
- ALF 세팅 담당자
- 고객사의 CX 리드
- CS 매니저
- 운영팀

## 사용 상황

- ALF 최초 배포 전
- FAQ와 정책 문서를 ALF 지식으로 연결하기 전
- 배송, 교환, 반품, 환불, 주문 취소 문의를 자동화하기 전
- 상담원 연결 조건을 정리할 때
- 주문 취소, 예약 변경, 환불 요청 같은 시스템 트리거 초안을 평가할 때
- 테스트 고객 질문을 만들 때

## 입력

사용자는 다음 중 하나 이상을 제공할 수 있다.

- FAQ 문서
- 배송 정책
- 교환, 반품, 환불 정책
- 주문 취소 정책
- 상품 또는 서비스 약관
- 상담 매크로
- ALF 규칙 초안
- 시스템 트리거 초안
- 고객 질문 목록
- 공개 정책 URL

## 근거 사용 원칙

- 사용자가 제공한 문서, URL, 공개 자료만 사용한다.
- private API, hidden logs, paid APIs, non-public customer data를 사용하지 않는다.
- 실제 고객 로그를 본 것처럼 가정하지 않는다.
- 채널톡 내부 ALF 평가 기준을 아는 것처럼 가정하지 않는다.
- 확인할 수 없는 내용은 `확인 불가`로 표시한다.
- 숫자, 성과, 정책 조건을 임의로 만들지 않는다.
- 출처 URL이 있으면 함께 표시한다.

## 작업 절차

1. 입력 문서와 공개 URL을 식별한다.
2. FAQ, 정책, 상담 규칙, 시스템 트리거 조건을 추출한다.
3. 확인되지 않는 내용은 `확인 불가`로 둔다.
4. 6축 감사 기준에 맞춰 findings JSON을 만든다.
5. findings JSON이 있으면 `scripts/score.py`를 실행해 축별 점수, 종합 점수, 판정, 위험 항목을 계산한다.
6. 운영자용 ALF 준비도 리포트를 작성한다.

## 6축 감사 기준

축 이름은 `score.py`의 `AXES`와 정확히 같아야 한다.

```text
knowledge_completeness
policy_consistency
answer_safety
handoff_clarity
task_trigger_safety
document_structure
```

1. `knowledge_completeness`
   - FAQ와 정책 문서가 반복 고객 질문을 충분히 커버하는지 확인한다.
   - 배송, 취소, 교환, 반품, 환불, AS, 상품 사용, 쿠폰, 결제 기준을 확인한다.

2. `policy_consistency`
   - FAQ, 약관, 이벤트 페이지, 상품 페이지, 상담 매크로가 서로 충돌하는지 확인한다.
   - 반품 가능 기간, 환불 제외 조건, 쿠폰 환불 처리, 이벤트 예외 조건을 확인한다.

3. `answer_safety`
   - ALF가 확정할 수 없는 내용을 단정적으로 답할 위험이 있는지 확인한다.
   - 배송 예정일 확답, 환불 가능성 보장, 재고 단정, 법률/의료/금융 조언을 주의한다.

4. `handoff_clarity`
   - ALF가 상담원에게 연결해야 하는 조건이 명확한지 확인한다.
   - 결제 분쟁, 배송 사고, 환불 거절 이의 제기, 개인정보 변경, 법적 이슈, 강한 불만을 확인한다.

5. `task_trigger_safety`
   - 주문 취소, 예약 변경, 환불 요청 같은 시스템 자동화 조건이 안전한지 확인한다.
   - 고객의 명확한 실행 의도, 주문 식별자, 최종 확인 조건이 있는지 확인한다.
   - 정책 질문만 하는 경우에는 실행 시스템을 트리거하지 않아야 한다.

6. `document_structure`
   - ALF가 문서를 쉽게 참조할 수 있는 구조인지 확인한다.
   - 제목, 조건, 예외, 절차, 상담원 연결 기준, 최신 수정일, 중복 문서를 확인한다.

## Findings JSON 형식

각 축에는 다음 필드를 사용할 수 있다.

```json
{
  "confidence": 0.8,
  "positive": [],
  "missing": [],
  "unclear": [],
  "negative": [],
  "sources": [],
  "recommendations": [],
  "handoff_rules": [],
  "task_rules": [],
  "test_questions": []
}
```

`missing`, `unclear`, `negative`는 점수에 반영된다. `policy_consistency`, `answer_safety`, `task_trigger_safety`의 `negative`는 배포 보류 판정의 핵심 신호다.

## score.py 출력

`scripts/score.py`는 findings JSON을 입력으로 받아 다음 항목을 JSON으로 출력한다.

- `axis_scores`
- `overall_score`
- `risk_flags`
- `verdict`
- `verdict_drivers`
- `missing_information`
- `policy_conflicts`
- `unsafe_answer_risks`
- `handoff_rules`
- `task_rules`
- `document_improvements`
- `test_questions`

## 판정 기준

- `배포 가능`: 종합 점수 80 이상이고 missing, unclear, negative findings가 없으며 handoff/task 관련 점수가 기준 이상인 경우
- `보완 후 배포`: 치명적 negative는 없지만 누락, 불명확성, 낮은 위험의 정책 이슈가 남아 있어 보완이 필요한 경우
- `배포 보류`: `policy_consistency`, `answer_safety`, `task_trigger_safety` 축에 명시적 negative가 있어 정책 충돌, 위험 답변, 위험한 시스템 실행 조건이 확인된 경우

불명확한 항목은 risk flag로 남길 수 있다. 다만 명시적 negative가 아니면 바로 `배포 보류`로 처리하지 않는다.

## 최종 출력

최종 리포트에는 다음을 포함한다.

- 최종 판정
- 종합 점수
- 축별 감사 결과
- 지식 누락 항목
- 정책 충돌 또는 불명확 항목
- 위험 답변 가능성
- 상담원 연결 조건 제안
- 자동화 가능한 시스템
- 자동화 보류 또는 금지 시스템
- 문서 구조 개선안
- ALF 규칙 제안
- 테스트 고객 질문
- `확인 불가` 항목
- 근거 URL

## 금지 사항

- 고객에게 직접 상담 답변을 제공하는 용도로 사용하지 않는다.
- ALF 배포 최종 결정을 대체하지 않는다.
- 법무, 환불, 의료, 금융, 컴플라이언스 검토를 대체하지 않는다.
- 실제 고객 데이터, 비공개 상담 로그, 내부 API, 로그에 필요한 자료를 사용하지 않는다.
- 채널톡 내부 모델 성능 기준이나 비공개 운영 기준을 알고 있는 것처럼 쓰지 않는다.
- synthetic sample을 실제 고객 사례처럼 표현하지 않는다.

## 한계

- 공개 자료는 채널톡 제품 구조를 설명하지만 실제 고객사의 비공개 정책 문서에 대한 ALF 평가 기준은 제공하지 않는다.
- synthetic sample은 실제 고객 데이터가 아니다.
- 실제 고객사의 비공개 정책 문서, 상담 로그, 시스템 실행 로그는 확인하지 않는다.
- 최종 배포 판단은 운영자와 담당자가 해야 한다.
