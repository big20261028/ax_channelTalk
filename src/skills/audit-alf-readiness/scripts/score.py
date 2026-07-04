#!/usr/bin/env python3
"""Score Channel Talk ALF readiness findings."""

from __future__ import annotations

import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

AXES = (
    "knowledge_completeness",
    "policy_consistency",
    "answer_safety",
    "handoff_clarity",
    "task_trigger_safety",
    "document_structure",
)

READY = "배포 가능"
FIX_THEN_DEPLOY = "보완 후 배포"
HOLD = "배포 보류"


def items(value):
    return value if isinstance(value, list) else []


def axis_score(axis, finding):
    confidence = finding.get("confidence", 0.5)
    try:
        confidence = max(0.0, min(1.0, float(confidence)))
    except (TypeError, ValueError):
        confidence = 0.5

    missing = len(items(finding.get("missing")))
    unclear = len(items(finding.get("unclear")))
    negative = len(items(finding.get("negative")))
    positive = len(items(finding.get("positive")))
    weight = 16 if axis in {"policy_consistency", "answer_safety", "task_trigger_safety"} else 12
    score = 70 + min(positive * 4, 12) - missing * 10 - unclear * 7 - negative * weight
    score -= int((1 - confidence) * 10)
    return max(0, min(100, int(round(score))))


def collect(findings, key):
    out = []
    for axis in AXES:
        for value in items(findings.get(axis, {}).get(key)):
            out.append({"axis": axis, "item": value})
    return out


def collect_plain(findings, key):
    out = []
    for axis in AXES:
        out.extend(items(findings.get(axis, {}).get(key)))
    return out


def default_questions(findings):
    questions = []
    for axis in AXES:
        finding = findings.get(axis, {})
        for value in items(finding.get("missing")) + items(finding.get("unclear")):
            questions.append(f"{axis}: {value}에 대한 정책 근거를 고객 질문 형태로 검증한다.")
    return questions[:8]


def score_payload(payload):
    findings = payload.get("findings") or {}
    axis_scores = {axis: axis_score(axis, findings.get(axis, {})) for axis in AXES}
    overall = int(round(sum(axis_scores.values()) / len(AXES)))

    missing = collect(findings, "missing")
    unclear = collect(findings, "unclear")
    negative = collect(findings, "negative")
    conflicts = items(findings.get("policy_consistency", {}).get("unclear")) + items(findings.get("policy_consistency", {}).get("negative"))
    unsafe = items(findings.get("answer_safety", {}).get("unclear")) + items(findings.get("answer_safety", {}).get("negative"))
    task_risks = items(findings.get("task_trigger_safety", {}).get("unclear")) + items(findings.get("task_trigger_safety", {}).get("negative"))
    blocking = (
        items(findings.get("policy_consistency", {}).get("negative"))
        + items(findings.get("answer_safety", {}).get("negative"))
        + items(findings.get("task_trigger_safety", {}).get("negative"))
    )

    risk_flags = []
    if conflicts:
        risk_flags.append("policy_conflict_or_ambiguity")
    if unsafe:
        risk_flags.append("unsafe_answer_risk")
    if task_risks:
        risk_flags.append("task_trigger_risk")

    if blocking:
        verdict = HOLD
    elif overall >= 80 and not missing and not unclear and not negative and axis_scores["handoff_clarity"] >= 75 and axis_scores["task_trigger_safety"] >= 75:
        verdict = READY
    else:
        verdict = FIX_THEN_DEPLOY

    drivers = []
    if verdict == HOLD:
        drivers.extend(risk_flags)
    elif verdict == READY:
        drivers.append("six_axis_scores_clear_threshold")
    else:
        drivers.append("non_critical_gaps_require_cleanup")

    handoff_rules = collect_plain(findings, "handoff_rules") or [
        f"상담원 연결 기준을 보강: {x['item']}" for x in missing + unclear if x["axis"] == "handoff_clarity"
    ]
    task_rules = collect_plain(findings, "task_rules") or [
        f"자동화 전 확인 조건 보강: {x['item']}" for x in missing + unclear if x["axis"] == "task_trigger_safety"
    ]
    test_questions = collect_plain(findings, "test_questions") or default_questions(findings)

    return {
        "workspace": payload.get("workspace", ""),
        "industry": payload.get("industry", ""),
        "axis_scores": axis_scores,
        "overall_score": overall,
        "risk_flags": risk_flags,
        "verdict": verdict,
        "verdict_drivers": drivers,
        "missing_information": [x["item"] for x in missing],
        "policy_conflicts": conflicts,
        "unsafe_answer_risks": unsafe,
        "handoff_rules": handoff_rules,
        "task_rules": task_rules,
        "document_improvements": collect_plain(findings, "recommendations"),
        "test_questions": test_questions,
    }


def load_input(path):
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        run_self_test()
        return 0

    print(json.dumps(score_payload(load_input(args.path)), ensure_ascii=False, indent=2))
    return 0


def sample():
    return {
        "workspace": "Example ecommerce support",
        "industry": "ecommerce",
        "findings": {axis: {"confidence": 1.0, "positive": ["근거 문서 있음", "예외 기준 있음", "운영 규칙 있음"], "missing": [], "unclear": [], "negative": []} for axis in AXES},
    }


def run_self_test():
    good = sample()
    assert score_payload(good)["verdict"] == READY

    partial = sample()
    partial["findings"]["knowledge_completeness"]["missing"] = ["부분 취소 환불 기준"]
    partial["findings"]["handoff_clarity"]["unclear"] = ["고액 환불 연결 기준"]
    assert score_payload(partial)["verdict"] == FIX_THEN_DEPLOY

    hold = sample()
    hold["findings"]["policy_consistency"]["negative"] = ["FAQ와 이벤트 페이지의 환불 조건 충돌"]
    hold["findings"]["answer_safety"]["negative"] = ["배송 예정일 확정 답변 위험"]
    assert score_payload(hold)["verdict"] == HOLD

    limited = sample()
    for axis in AXES:
        limited["findings"][axis]["confidence"] = 0.35
        limited["findings"][axis]["positive"] = []
        limited["findings"][axis]["missing"] = ["추가 문서 필요"]
    assert score_payload(limited)["verdict"] == FIX_THEN_DEPLOY

    print("self-test ok")


if __name__ == "__main__":
    raise SystemExit(main())
