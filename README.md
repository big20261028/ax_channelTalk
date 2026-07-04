# Channel ALF Readiness Auditor

Codex plugin for auditing whether FAQ, policy documents, support rules, and task drafts are ready for Channel Talk ALF deployment.

## Problem

Channel Talk presents ALF as an AI agent that can answer repeated support questions, use structured knowledge, follow business rules, run tasks, and hand off to a human agent when needed. Before a company lets ALF answer customers or run actions, its FAQ, policies, rules, and task triggers must be complete, consistent, and safe.

This plugin audits that readiness and produces an operations-facing report.

## Public Evidence

- Channel Talk says repeated inquiries can be handled by AI while human agents focus on important conversations: <https://channel.io/kr>
- Channel Talk explains ALF through knowledge, rules, and task execution: <https://channel.io/kr>
- ALF customer page describes RAG knowledge, rule filters, task triggers, code nodes, performance metrics, and human handoff: <https://channel.io/kr/alf-customer>
- Documents page says Channel Talk Documents can become ALF's knowledge database: <https://channel.io/kr/documents>

Limits: these are public product pages, not private customer data or internal ALF evaluation rules.

## Users

- CX leads
- CS managers
- Operations teams
- ALF setup owners
- Solution consultants

## Use Cases

- First ALF deployment
- Preparing FAQ and policy documents for ALF knowledge
- Automating shipping, exchange, return, refund, cancellation, or booking-change inquiries
- Checking unsafe answer risks
- Defining human handoff rules

## How It Works

The skill asks Codex to inspect supplied documents or public URLs, produce findings across six axes, and optionally run `score.py` on findings JSON.

The scorer is deterministic and uses only Python standard library.

## Difference From General Codex Questions

General Codex can summarize documents. This plugin forces an ALF-readiness frame: missing support knowledge, policy conflicts, unsafe answer risks, handoff rules, task-trigger safety, and document structure.

## Six Audit Axes

1. `knowledge_completeness`
2. `policy_consistency`
3. `answer_safety`
4. `handoff_clarity`
5. `task_trigger_safety`
6. `document_structure`

## Verdicts

- `배포 가능`: overall score is at least 80 and no missing, unclear, or negative findings remain.
- `보완 후 배포`: non-critical gaps, ambiguities, or low-risk policy issues remain, but no explicit blocking negative signal is present.
- `배포 보류`: explicit blocking risks are present, such as confirmed policy conflict, unsafe answer promise, or unsafe task execution condition.

`unclear` items still appear in `risk_flags`, but only explicit `negative` findings in `policy_consistency`, `answer_safety`, or `task_trigger_safety` block deployment.

## Install

Use `.agents/plugins/marketplace.json` as the local marketplace entry for this repo.

Plugin source:

```text
./src
```

Skill:

```text
audit-alf-readiness
```

## Test

```powershell
python -m py_compile .\src\skills\audit-alf-readiness\scripts\score.py
python .\src\skills\audit-alf-readiness\scripts\score.py --self-test
python .\src\skills\audit-alf-readiness\scripts\score.py .\examples\alf-readiness-findings.json
Get-Content .\examples\alf-readiness-findings.json | python .\src\skills\audit-alf-readiness\scripts\score.py
```

## Example Output

See `examples/alf-readiness-findings.json` and `logs/channel-alf-readiness-e2e-20260704.md`.

## Submission ZIP Include

Required / included:

```text
src/
README.md
logs/
examples/
.agents/plugins/marketplace.json
```

Optional, if present:

```text
research/
```

## Submission ZIP Exclude

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

Do not exclude existing evidence logs such as `logs/codex/*.jsonl`, original work logs, failed-attempt logs, problem-definition logs, E2E logs, or validation logs.

Do not create the final submission by zipping the entire repository if `submission.zip` already exists in the repo. That can create a nested zip. Either submit the verified `submission.zip` directly, or regenerate it from the intended include list while excluding any existing `submission.zip`.

## Suggested Submission Questions

1. Which customer-support gap does this plugin solve before ALF deployment?
2. Which public Channel Talk evidence supports the audit axes?
3. Which documents should a company provide before using this plugin?
4. Which risks cause `배포 보류`?
5. Which parts of the E2E sample are synthetic rather than public evidence?
