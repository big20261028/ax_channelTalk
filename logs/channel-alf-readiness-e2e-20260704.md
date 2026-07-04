# Channel ALF Readiness E2E

Date: 2026-07-04

## Goal

Show why a Channel Talk customer should audit FAQ, policy, support rules, and task conditions before ALF deployment, and how this plugin performs that audit.

## Public URLs Used

- https://channel.io/kr
- https://channel.io/kr/alf-customer
- https://channel.io/kr/documents

## Public Facts Used

- ALF is positioned as a customer-support AI agent that can reduce repeated inquiries.
- ALF depends on structured knowledge, rules, and task automation.
- ALF task automation can include API calls, data processing, and system changes.
- ALF can connect customers to a human agent.
- Channel Talk Documents can be used as ALF's knowledge database.

## Synthetic Sample Notice

The ecommerce FAQ, policy, macro, and task findings below are synthetic samples. They are not real customer data and do not come from Channel Talk private logs.

## Input Findings JSON

File: `examples/alf-readiness-findings.json`

Summary:

- Shipping, exchange, return, and refund documents are partly present.
- Partial cancellation, coupon refund, and some item return restrictions are unclear.
- Delivery ETA certainty before invoice registration is risky.
- Handoff rules are partly missing.
- Order-cancel task automation needs final confirmation conditions.

## score.py Raw Output

```json
{
  "workspace": "Synthetic ecommerce support readiness sample",
  "industry": "ecommerce",
  "axis_scores": {
    "knowledge_completeness": 49,
    "policy_consistency": 65,
    "answer_safety": 65,
    "handoff_clarity": 61,
    "task_trigger_safety": 61,
    "document_structure": 66
  },
  "overall_score": 61,
  "risk_flags": [
    "policy_conflict_or_ambiguity",
    "unsafe_answer_risk"
  ],
  "verdict": "보완 후 배포",
  "verdict_drivers": [
    "non_critical_gaps_require_cleanup"
  ],
  "missing_information": [
    "부분 취소 시 쿠폰과 배송비 환불 기준",
    "AS 접수와 단순 반품의 구분 기준",
    "고액 환불과 반복 클레임의 상담원 연결 기준",
    "취소 실행 전 주문번호, 상품명, 취소 의사 재확인 조건"
  ],
  "policy_conflicts": [
    "쿠폰 사용 주문의 환불 방식이 FAQ와 이벤트 문서에서 다르게 읽힐 수 있다"
  ],
  "unsafe_answer_risks": [
    "송장 등록 전 배송 예정일을 확정해도 되는지 불명확하다"
  ],
  "handoff_rules": [
    "환불 거절 이의 제기, 고액 환불, 개인정보 변경, 강한 불만은 상담원에게 연결한다"
  ],
  "task_rules": [
    "주문 취소는 고객이 실제 취소 의사를 밝히고 주문 식별자가 확인된 뒤에만 접수한다",
    "정책 질문만 하는 경우에는 취소 태스크를 실행하지 않는다"
  ],
  "document_improvements": [
    "부분 취소, 쿠폰 환불, 상품군별 반품 제한을 별도 문서로 분리한다",
    "쿠폰 환불 우선순위와 예외를 한 문장으로 통일한다",
    "배송 추적 전에는 예정일을 확정하지 말라는 ALF 규칙을 추가한다",
    "상담원 연결 조건을 금액, 주문 상태, 고객 감정 신호 기준으로 문서화한다",
    "태스크 트리거 제외 조건에 배송 조회, 교환, 단순 정책 문의를 추가한다",
    "각 문서에 적용 시작일, 예외, 상담원 연결 기준을 같은 위치에 둔다"
  ],
  "test_questions": [
    "쿠폰을 쓰고 일부 상품만 취소하면 쿠폰은 어떻게 환불되나요?",
    "송장이 아직 안 나왔는데 내일 도착한다고 확답할 수 있나요?",
    "파손 상품 환불을 거절당했는데 상담원에게 연결해 주세요",
    "방금 주문한 2번 상품만 취소해 주세요",
    "이벤트 상품도 단순 변심 반품이 되나요?"
  ]
}
```

## Final ALF Readiness Report

- Verdict: `보완 후 배포`
- Overall score: 61
- Main missing knowledge:
  - Partial cancellation coupon and shipping-fee refund rules
  - AS versus simple return distinction
  - High-value refund and repeated complaint handoff criteria
  - Final confirmation before order-cancel task execution
- Policy conflict or ambiguity:
  - Coupon refund handling may be read differently between FAQ and event policy.
- Unsafe answer risk:
  - ALF might overstate a delivery date before invoice/tracking data exists.
- Handoff suggestion:
  - Hand off refund rejection appeals, high-value refunds, personal data changes, and strong complaints.
- Automatable tasks:
  - Order cancellation after clear customer intent and order identification.
- Deferred or forbidden tasks:
  - Do not execute cancellation for policy-only questions, delivery tracking questions, exchange questions, or unclear order identity.
- Knowledge improvement:
  - Split partial cancellation, coupon refund, and item-specific return restrictions into explicit policy sections.
- Test customer questions:
  - 쿠폰을 쓰고 일부 상품만 취소하면 쿠폰은 어떻게 환불되나요?
  - 송장이 아직 안 나왔는데 내일 도착한다고 확답할 수 있나요?
  - 파손 상품 환불을 거절당했는데 상담원에게 연결해 주세요
  - 방금 주문한 2번 상품만 취소해 주세요
  - 이벤트 상품도 단순 변심 반품이 되나요?

## Confirm Unavailable

- Real customer logs: 확인 불가, not used
- Internal ALF evaluation thresholds: 확인 불가
- Customer-specific policy source of truth: 확인 불가

## Verification Commands

```powershell
C:\Users\traz1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m py_compile .\src\skills\audit-alf-readiness\scripts\score.py
C:\Users\traz1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\src\skills\audit-alf-readiness\scripts\score.py --self-test
C:\Users\traz1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\src\skills\audit-alf-readiness\scripts\score.py .\examples\alf-readiness-findings.json
cmd /c "chcp 65001 >NUL & type examples\alf-readiness-findings.json | C:\Users\traz1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe src\skills\audit-alf-readiness\scripts\score.py"
```

## Limits

- The sample policy set is synthetic.
- Public Channel Talk pages justify the audit frame but do not provide a private customer policy corpus.
- The scorer is deterministic and deliberately simple; it is not a replacement for legal, refund, medical, financial, or compliance review.
