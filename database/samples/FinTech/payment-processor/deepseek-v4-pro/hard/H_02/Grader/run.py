#!/usr/bin/env python3
import json, os, sys, subprocess
from pathlib import Path

TASK_ID = "H_02"
RESULT_DIR = Path("results") / TASK_ID / "results"
RESULT_FILE = RESULT_DIR / "result.json"
WORKSPACE_DIR = Path("results") / TASK_ID / "WorkSpace"

def run_detector():
    script = WORKSPACE_DIR / "fraud_detector.py"
    if not script.exists():
        return None, "fraud_detector.py not found"
    try:
        r = subprocess.run(["python3", str(script)], capture_output=True, text=True, timeout=30, cwd=WORKSPACE_DIR)
        if r.returncode != 0:
            return None, r.stderr
        return True, r.stdout
    except Exception as e:
        return None, str(e)

def run_pytest():
    test_file = WORKSPACE_DIR / "test_fraud_detector.py"
    if not test_file.exists():
        return -1, "test_fraud_detector.py not found"
    try:
        r = subprocess.run(["python3", "-m", "pytest", "test_fraud_detector.py", "--tb=short", "-q"], capture_output=True, text=True, timeout=30, cwd=WORKSPACE_DIR)
        return r.returncode, r.stdout + r.stderr
    except Exception as e:
        return -1, str(e)

def load_result():
    if not RESULT_FILE.exists():
        return None
    with open(RESULT_FILE) as f:
        return json.load(f)

def grade():
    # Run the detector first if result doesn't exist
    if not RESULT_FILE.exists():
        success, msg = run_detector()
        if not success:
            # Still try to load
            pass

    data = load_result()
    results = []

    def check(rid, passed, reason):
        results.append({
            "rubric_id": rid,
            "passed": passed,
            "score": 1.0 if passed else 0.0,
            "reason": reason,
            "evidence": {}
        })

    script_path = WORKSPACE_DIR / "fraud_detector.py"
    r1_pass = script_path.exists()
    check("R1", r1_pass, "fraud_detector.py exists" if r1_pass else "fraud_detector.py not found")

    if not r1_pass:
        return finalize(results)

    r2_pass = data is not None and isinstance(data, dict)
    check("R2", r2_pass, "result.json is valid JSON" if r2_pass else "result.json missing or invalid")
    if not r2_pass:
        return finalize(results)

    rules = data.get("rules_applied", [])
    r3_pass = len(rules) >= 3
    check("R3", r3_pass, f"rules_applied has {len(rules)} entries" if r3_pass else f"Expected >=3 rules, got {len(rules)}")

    flagged = data.get("flagged_transactions", [])
    r4_pass = isinstance(flagged, list)
    check("R4", r4_pass, f"flagged_transactions is a list (len={len(flagged)})" if r4_pass else "flagged_transactions not a list")

    summary = data.get("summary", {})
    r5_pass = summary.get("total_checked", 0) >= 1 and isinstance(summary.get("total_flagged"), int)
    check("R5", r5_pass, f"summary: checked={summary.get('total_checked')}, flagged={summary.get('total_flagged')}" if r5_pass else f"summary missing fields: {summary}")

    r6_pass = True
    for ft in flagged:
        if not all(k in ft for k in ["txn_id", "amount", "triggered_rules"]):
            r6_pass = False
        if not isinstance(ft.get("triggered_rules"), list):
            r6_pass = False
    check("R6", r6_pass, f"All flagged entries have txn_id, amount, triggered_rules" if r6_pass else "Some flagged entries missing fields")

    per_rule = data.get("per_rule_breakdown", {})
    r7_pass = isinstance(per_rule, dict) and len(per_rule) >= 3
    if r7_pass:
        for rule_name, rule_data in per_rule.items():
            if not all(k in rule_data for k in ["triggered_count", "total_amount_flagged"]):
                r7_pass = False
    check("R7", r7_pass, f"per_rule_breakdown has {len(per_rule)} entries with required fields" if r7_pass else f"per_rule_breakdown invalid: {per_rule}")

    # R8: amount_threshold rule fires for >2000
    r8_pass = any(
        ft.get("amount", 0) > 2000 and "amount_threshold" in ft.get("triggered_rules", [])
        for ft in flagged
    ) if flagged else True
    check("R8", r8_pass, "amount_threshold rule flags high-value transactions" if r8_pass else "amount_threshold rule not triggered correctly")

    test_file = WORKSPACE_DIR / "test_fraud_detector.py"
    if test_file.exists():
        content = test_file.read_text()
        test_funcs = [line for line in content.split("\n") if line.strip().startswith("def test_")]
        r9_pass = len(test_funcs) >= 5
    else:
        r9_pass = False
    check("R9", r9_pass, f"test_fraud_detector.py has {len(test_funcs) if test_file.exists() else 0} test functions" if r9_pass else "test_fraud_detector.py missing or <5 tests")

    rc, output = run_pytest()
    r10_pass = rc == 0
    check("R10", r10_pass, "pytest passes" if r10_pass else f"pytest failed (exit={rc})")

    return finalize(results)

def finalize(results):
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    must_pass_ids = ["R1","R2","R3","R4","R5"]
    must_pass_satisfied = all(r["passed"] for r in results if r["rubric_id"] in must_pass_ids)

    if passed >= 8 and must_pass_satisfied:
        status = "pass"
    elif passed >= 5:
        status = "partial"
    else:
        status = "fail"

    outcome = {
        "task_id": TASK_ID,
        "status": status,
        "outcome_status": "satisfied" if status == "pass" else "needs_revision",
        "passed": passed,
        "total": total,
        "must_pass_satisfied": must_pass_satisfied,
        "results": results
    }
    out_dir = Path("grading_results")
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "grading_result.json", "w") as f:
        json.dump(outcome, f, indent=2)
    print(json.dumps(outcome, indent=2))
    return 0 if status == "pass" else 1

if __name__ == "__main__":
    sys.exit(grade())
