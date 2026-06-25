#!/usr/bin/env python3
import json, os, sys, subprocess
from pathlib import Path

TASK_ID = "C_03"
RESULT_DIR = Path("results") / TASK_ID / "results"
RESULT_FILE = RESULT_DIR / "result.json"
WORKSPACE_DIR = Path("results") / TASK_ID / "WorkSpace"

def run_card_cli(num):
    script = WORKSPACE_DIR / "validate_card.py"
    if not script.exists():
        return None
    try:
        r = subprocess.run(["python3", str(script), num], capture_output=True, text=True, timeout=15, cwd=WORKSPACE_DIR)
        if r.returncode != 0:
            return {"error": r.stderr}
        return json.loads(r.stdout)
    except Exception as e:
        return {"error": str(e)}

def run_pytest():
    script = WORKSPACE_DIR / "test_validate.py"
    if not script.exists():
        return None, "test_validate.py not found"
    try:
        r = subprocess.run(["python3", "-m", "pytest", "test_validate.py", "--tb=short", "-q"], capture_output=True, text=True, timeout=30, cwd=WORKSPACE_DIR)
        return r.returncode, r.stdout + r.stderr
    except Exception as e:
        return -1, str(e)

def load_result():
    if not RESULT_FILE.exists():
        return None
    with open(RESULT_FILE) as f:
        return json.load(f)

def grade():
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

    # R1: validate_card.py exists
    script_path = WORKSPACE_DIR / "validate_card.py"
    r1_pass = script_path.exists()
    check("R1", r1_pass, "validate_card.py exists" if r1_pass else "validate_card.py not found")

    if not r1_pass:
        return finalize(results)

    # R2: Visa test
    r2_result = run_card_cli("4111111111111111")
    r2_pass = r2_result is not None and r2_result.get("valid") is True
    check("R2", r2_pass, f"Visa 4111111111111111 valid=true: {r2_result}" if r2_pass else f"Visa test failed: {r2_result}")

    # R3: Mastercard test
    r3_result = run_card_cli("5500000000000004")
    r3_pass = r3_result is not None and r3_result.get("valid") is True
    check("R3", r3_pass, f"Mastercard 5500000000000004 valid=true: {r3_result}" if r3_pass else f"Mastercard test failed: {r3_result}")

    # R4: Amex test
    r4_result = run_card_cli("340000000000009")
    r4_pass = r4_result is not None and r4_result.get("valid") is True and r4_result.get("brand") == "Amex"
    check("R4", r4_pass, f"Amex 340000000000009 valid=true, brand=Amex: {r4_result}" if r4_pass else f"Amex test failed: {r4_result}")

    # R5: Invalid card
    r5_result = run_card_cli("1234567890123456")
    r5_pass = r5_result is not None and r5_result.get("valid") is False
    check("R5", r5_pass, f"Invalid card valid=false: {r5_result}" if r5_pass else f"Invalid card test failed: {r5_result}")

    # R6: Output JSON keys
    sample = r2_result if r2_result else {}
    required_keys = {"card_number", "brand", "valid", "checksum", "error"}
    keys_present = set(sample.keys())
    r6_pass = required_keys.issubset(keys_present)
    check("R6", r6_pass, f"All required keys present: {keys_present}" if r6_pass else f"Missing keys: {required_keys - keys_present}")

    # R7: card_number masked
    r7_pass = isinstance(sample.get("card_number"), str) and "****-****-****-" in sample["card_number"]
    check("R7", r7_pass, f"card_number masked: {sample.get('card_number')}" if r7_pass else f"card_number not masked: {sample.get('card_number')}")

    # R8: brand detection
    r8_visa = run_card_cli("4111111111111111")
    r8_mc = run_card_cli("5500000000000004")
    r8_amex = run_card_cli("340000000000009")
    r8_inv = run_card_cli("1234567890123456")
    r8_pass = (r8_visa.get("brand") == "Visa" if r8_visa else False) and \
              (r8_mc.get("brand") == "Mastercard" if r8_mc else False) and \
              (r8_amex.get("brand") == "Amex" if r8_amex else False) and \
              (r8_inv.get("brand") == "Unknown" if r8_inv else False)
    check("R8", r8_pass, "Brand detection correct" if r8_pass else "Brand detection incorrect")

    # R9: test_validate.py with 5 test functions
    test_file = WORKSPACE_DIR / "test_validate.py"
    if test_file.exists():
        content = test_file.read_text()
        test_funcs = [line for line in content.split("\n") if line.strip().startswith("def test_")]
        r9_pass = len(test_funcs) >= 5
    else:
        r9_pass = False
    check("R9", r9_pass, f"test_validate.py has {len(test_funcs) if test_file.exists() else 0} test functions" if r9_pass else "test_validate.py missing or has <5 test functions")

    # R10: pytest passes
    rc, output = run_pytest()
    r10_pass = rc == 0
    check("R10", r10_pass, "pytest passes" if r10_pass else f"pytest failed (exit={rc}): {output[:200] if output else 'no output'}")

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
