# Channel ALF Validation

Date: 2026-07-04

Scope: submission-readiness validation after README verdict wording update.

## Readiness Checks

- `README.md` verdict wording now matches `score.py`:
  - `unclear` items can produce `risk_flags`.
  - Deployment is blocked only by explicit `negative` findings in `policy_consistency`, `answer_safety`, or `task_trigger_safety`.
- `src/.codex-plugin/plugin.json` name: `channel-alf-readiness-auditor`
- `src/.codex-plugin/plugin.json` skills path: `./skills/`
- `src/.codex-plugin/plugin.json` MCP path: `./.mcp.json`
- `src/.mcp.json` exists and parses as JSON.
- `.agents/plugins/marketplace.json` points to `./src`.
- `submission.zip` was checked for nested `submission.zip`; none was present.

## Validator Dependency

Initial official validator attempts failed because bundled Python did not have `PyYAML`.

Resolution:

- Installed `PyYAML` into the bundled Python validation environment only.
- Did not add `PyYAML` to project code or `score.py`.
- `score.py` still uses only Python standard library.

## Official Validation

```text
Plugin validation passed: C:\Users\traz1\Desktop\AX_hackathon\AX_channeltalk\src
Skill is valid!
```

For the skill validator on Windows, UTF-8 mode was required because the validator otherwise read `SKILL.md` with cp949.

Command used:

```powershell
cmd /c "set PYTHONUTF8=1&& C:\Users\traz1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe C:\Users\traz1\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\src\skills\audit-alf-readiness"
```

## Runtime Checks

```text
py_compile: passed
self-test: self-test ok
example JSON: passed, verdict 보완 후 배포, overall_score 61
stdin JSON: passed, same verdict and score as file input
JSON parse: plugin.json, .mcp.json, marketplace.json, and alf-readiness-findings.json passed
```

## ZIP Check

Expected included roots:

```text
src/
README.md
logs/
examples/
.agents/plugins/marketplace.json
```

Expected excluded paths:

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

Important: do not zip the whole repository after `submission.zip` exists. Submit the verified `submission.zip` directly, or regenerate it from the include list while excluding any existing `submission.zip`.
