#!/usr/bin/env python3
import json, sys
from pathlib import Path

TASK_ID = "C_05"
RESULT_DIR = Path("results") / TASK_ID / "results"
RESULT_FILE = RESULT_DIR / "result.json"

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

    r1_pass = data is not None and isinstance(data, dict)
    check("R1", r1_pass, "result.json exists and is valid JSON" if r1_pass else "result.json missing or invalid")
    if not r1_pass:
        return finalize(results)

    r2_pass = data.get("total_requests") == 6
    check("R2", r2_pass, f"total_requests = {data.get('total_requests')}" if r2_pass else f"Expected 6, got {data.get('total_requests')}")

    # total_requested = 150 + 2300 + 45.99 + 678.50 + 1200 + 89.99 = 4464.48
    expected_requested = 150.00 + 2300.00 + 45.99 + 678.50 + 1200.00 + 89.99
    actual_requested = data.get("total_requested_amount")
    r3_pass = isinstance(actual_requested, (int,float)) and abs(actual_requested - expected_requested) < 0.01
    check("R3", r3_pass, f"total_requested_amount = {actual_requested}" if r3_pass else f"Expected {expected_requested:.2f}, got {actual_requested}")

    # customer_request (150+678.50+89.99=918.49) + duplicate_charge (2300) = 3218.49 ? Wait...
    # Actually REF001=customer_request=150, REF002=duplicate_charge=2300, REF004=customer_request=678.50, REF006=customer_request=89.99
    # approved = customer_request + duplicate_charge = REF001(150,customer_request) + REF002(2300,duplicate_charge) + REF004(678.50,customer_request) + REF006(89.99,customer_request)
    # = 150+2300+678.50+89.99 = 3218.49
    # rejected = product_defective(45.99) + wrong_amount(1200) = 1245.99
    expected_approved = 150.00 + 2300.00 + 678.50 + 89.99
    actual_approved = data.get("total_approved_amount")
    r4_pass = isinstance(actual_approved, (int,float)) and abs(actual_approved - expected_approved) < 0.01
    check("R4", r4_pass, f"total_approved_amount = {actual_approved}" if r4_pass else f"Expected {expected_approved:.2f}, got {actual_approved}")

    expected_rejected = 45.99 + 1200.00
    actual_rejected = data.get("total_rejected_amount")
    r5_pass = isinstance(actual_rejected, (int,float)) and abs(actual_rejected - expected_rejected) < 0.01
    check("R5", r5_pass, f"total_rejected_amount = {actual_rejected}" if r5_pass else f"Expected {expected_rejected:.2f}, got {actual_rejected}")

    reasons = data.get("per_reason_breakdown", {})
    r6_pass = all(k in reasons for k in ["customer_request","duplicate_charge","product_defective","wrong_amount"])
    if r6_pass:
        r6_pass = reasons["customer_request"]["count"] == 3 and reasons["duplicate_charge"]["count"] == 1 and reasons["product_defective"]["count"] == 1 and reasons["wrong_amount"]["count"] == 1
    check("R6", r6_pass, f"per_reason_breakdown correct" if r6_pass else f"per_reason_breakdown incorrect: {reasons}")

    processed = data.get("processed", [])
    r7_pass = len(processed) == 6 and all("refund_id" in p and "status" in p and "amount" in p and "reason" in p for p in processed)
    check("R7", r7_pass, f"processed has {len(processed)} entries with required fields" if r7_pass else f"processed invalid: count={len(processed)}")

    ref_statuses = {p.get("refund_id"): p.get("status") for p in processed}
    r8_pass = ref_statuses.get("REF001") == "approved" and ref_statuses.get("REF003") == "rejected" and ref_statuses.get("REF005") == "rejected"
    check("R8", r8_pass, f"REF001=approved, REF003=rejected, REF005=rejected" if r8_pass else f"Status check failed: {ref_statuses}")

    net = data.get("net_impact")
    expected_net = expected_approved - expected_requested
    r9_pass = isinstance(net, (int,float)) and abs(net - expected_net) < 0.01
    check("R9", r9_pass, f"net_impact = {net}" if r9_pass else f"Expected {expected_net:.2f}, got {net}")

    # R10: all amounts are numeric
    r10_pass = not isinstance(actual_approved, str) and not isinstance(actual_requested, str)
    if r10_pass:
        for p in processed:
            if isinstance(p.get("amount"), str):
                r10_pass = False
                break
    check("R10", r10_pass, "All amounts are numeric" if r10_pass else "String amounts found")

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
