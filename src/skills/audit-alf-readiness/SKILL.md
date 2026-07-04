---
name: audit-alf-readiness
description: Use before Channel Talk ALF deployment to audit FAQ, policy documents, support rules, and task drafts for missing knowledge, policy conflicts, unsafe answer risks, handoff conditions, automation risks, and document-structure improvements.
---

# Channel ALF Readiness Audit

Use this skill to produce an operations-facing ALF readiness audit, not a customer-facing answer.

## Users

- CX leads preparing Channel Talk ALF
- CS managers
- Operations teams
- ALF setup owners
- Solution consultants

## Use Cases

- First ALF deployment
- Preparing FAQ and policy documents for ALF knowledge
- Automating shipping, exchange, return, refund, and cancellation inquiries
- Drafting order-cancel, booking-change, refund-request, or similar task automation
- Checking likely unsafe AI answers
- Defining when ALF must hand off to a human agent

## Inputs

The user may provide one or more of:

- FAQ documents
- Shipping policy
- Exchange, return, and refund policy
- Order cancellation policy
- Product or service terms
- Support macros
- ALF rule drafts
- System trigger drafts
- Customer question lists
- Public policy URLs

## Evidence Policy

- Use only documents, URLs, or public materials provided by the user.
- Do not use private APIs, hidden logs, paid APIs, or non-public customer data.
- Mark unverifiable facts as `확인 불가`.
- Do not invent numbers, outcomes, or policy terms.
- Cite source URLs when available.

## Six Audit Axes

1. `knowledge_completeness`
   - Whether FAQ and policy documents cover repeated customer questions.
   - Check shipping, cancellation, exchange, return, refund, AS, product use, coupon, and payment coverage.

2. `policy_consistency`
   - Whether FAQ, terms, event pages, product pages, and support macros conflict.
   - Check return windows, refund exclusions, coupon refund handling, and similar policy details.

3. `answer_safety`
   - Whether ALF could answer with unsafe certainty.
   - Watch for unverified delivery dates, refund eligibility promises, inventory claims, legal, medical, or financial advice.

4. `handoff_clarity`
   - Whether the documents define when ALF must hand off to a human.
   - Check payment disputes, delivery accidents, refund rejection appeals, personal data changes, legal issues, and strong complaints.

5. `task_trigger_safety`
   - Whether task automation conditions are safe enough.
   - Confirm that task triggers require clear customer intent and enough identifiers before order cancellation, booking changes, or refund submission.

6. `document_structure`
   - Whether ALF can easily reference the documents.
   - Check headings, conditions, exceptions, steps, handoff criteria, freshness, and duplicate documents.

## Workflow

1. Identify supplied documents and source URLs.
2. Extract facts, policies, rules, and task conditions. Mark gaps as `확인 불가`.
3. Score each axis from 0 to 100 using the six audit axes.
4. Call `scripts/score.py` when findings JSON is available.
5. Produce the final ALF readiness report.

## Final Output

Include:

- Final verdict: `배포 가능`, `보완 후 배포`, or `배포 보류`
- Overall score
- Axis audit results
- Missing knowledge
- Policy conflicts
- Unsafe answer risks
- Handoff rule suggestions
- Automatable tasks
- Tasks to defer or forbid
- Document-structure improvements
- ALF rule suggestions
- Test customer-question set
- `확인 불가` items
- Evidence URLs
