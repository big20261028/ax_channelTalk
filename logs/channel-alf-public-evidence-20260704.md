# Channel ALF Public Evidence

Date: 2026-07-04

Scope: public Channel Talk pages only. No private APIs, customer logs, paid data, or internal Channel Talk data were used.

## Sources

- Channel Talk homepage: https://channel.io/kr
- ALF customer page: https://channel.io/kr/alf-customer
- Documents page: https://channel.io/kr/documents

## Confirmed Facts

1. Channel Talk presents ALF as an AI agent for customer support automation.
   - Source: https://channel.io/kr
   - Public page says repeated inquiries can be handled by AI while human agents focus on important conversations.

2. Channel Talk describes ALF readiness around rules, structured knowledge, executable tasks, and improvement suggestions.
   - Source: https://channel.io/kr
   - This supports auditing business rules, knowledge structure, and task safety before deployment.

3. ALF uses knowledge/RAG materials.
   - Source: https://channel.io/kr/alf-customer
   - Public page describes folder-managed knowledge, document, Excel, website, and PDF support, and filters for controlling answer scope.

4. ALF supports rules with conditions.
   - Source: https://channel.io/kr/alf-customer
   - Public page says rules can be managed in one place and applied by detailed condition filters.

5. ALF supports task automation.
   - Source: https://channel.io/kr/alf-customer
   - Public page describes trigger nodes, agent nodes, and code nodes for API calls, data processing, and system changes.

6. ALF can hand off to a human agent.
   - Source: https://channel.io/kr/alf-customer
   - Public page says ALF can connect customers to an agent when the customer wants agent connection.

7. Channel Talk Documents can serve as ALF knowledge.
   - Source: https://channel.io/kr/documents
   - Public page says customer-support documents can be managed together and used as an AI knowledge database.

## Problem Definition Supported By Public Evidence

ALF can answer, follow rules, refer to knowledge, run tasks, and hand off. Therefore, a customer company needs a readiness audit before deployment:

- Are FAQ and policy documents complete enough?
- Do policy pages, FAQ, event pages, and macros conflict?
- Could ALF answer with unsafe certainty?
- Are human handoff conditions explicit?
- Are task triggers safe enough before system-changing actions?
- Are documents structured for reliable retrieval?

## Not Confirmed

- Private customer performance data beyond public examples: 확인 불가
- Internal Channel Talk ALF scoring rules: 확인 불가
- Customer-specific policy requirements: 확인 불가
- Real customer logs or PII: not used
