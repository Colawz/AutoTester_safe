#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

TASK_ID = "C_01"
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

    # R1: result.json exists and is valid JSON
    r1_pass = data is not None and isinstance(data, dict)
    check("R1", r1_pass, "result.json exists and is valid JSON" if r1_pass else "result.json missing or invalid")

    if not r1_pass:
        return finalize(results)

    # R2: total_transaction_count = 15
    r2_pass = data.get("total_transaction_count") == 15
    check("R2", r2_pass, f"total_transaction_count = {data.get('total_transaction_count')}" if r2_pass else f"Expected 15, got {data.get('total_transaction_count')}")

    # R3: total_amount = 24428.97
    expected_total = 150.00 + 2300.00 + 45.99 + 678.50 + 1200.00 + 89.99 + 4500.00 + 299.99 + 75.00 + 1800.00 + 550.00 + 34.50 + 9200.00 + 125.00 + 780.00
    actual_total = data.get("total_amount")
    r3_pass = isinstance(actual_total, (int, float)) and abs(actual_total - expected_total) < 0.01
    check("R3", r3_pass, f"total_amount = {actual_total}" if r3_pass else f"Expected {expected_total:.2f}, got {actual_total}")

    # R4: total_fees = 797.40
    expected_fees = 4.50 + 69.00 + 2.30 + 20.36 + 36.00 + 2.70 + 225.00 + 9.00 + 2.25 + 90.00 + 16.50 + 1.04 + 276.00 + 3.75 + 39.00
    actual_fees = data.get("total_fees")
    r4_pass = isinstance(actual_fees, (int, float)) and abs(actual_fees - expected_fees) < 0.01
    check("R4", r4_pass, f"total_fees = {actual_fees}" if r4_pass else f"Expected {expected_fees:.2f}, got {actual_fees}")

    # R5: net_amount = total_amount - total_fees
    expected_net = expected_total - expected_fees
    actual_net = data.get("net_amount")
    r5_pass = isinstance(actual_net, (int, float)) and abs(actual_net - expected_net) < 0.01
    check("R5", r5_pass, f"net_amount = {actual_net}" if r5_pass else f"Expected {expected_net:.2f}, got {actual_net}")

    # R6: per_card_type
    pct = data.get("per_card_type", {})
    visa_ok = pct.get("Visa", {}).get("count") == 5 and abs(pct.get("Visa", {}).get("amount", 0) - (150+678.50+89.99+75+9200)) < 0.01
    mc_ok = pct.get("Mastercard", {}).get("count") == 4 and abs(pct.get("Mastercard", {}).get("amount", 0) - (2300+1200+299.99+550+125)) < 0.01
    amex_ok = pct.get("Amex", {}).get("count") == 3 and abs(pct.get("Amex", {}).get("amount", 0) - (45.99+4500+1800+780)) < 0.01
    r6_pass = visa_ok and mc_ok and amex_ok
    check("R6", r6_pass, "per_card_type correct" if r6_pass else f"per_card_type mismatch: {pct}")

    # R7: per_merchant
    pm = data.get("per_merchant", {})
    m1_ok = pm.get("MERCH001", {}).get("count") == 5
    m2_ok = pm.get("MERCH002", {}).get("count") == 5
    m3_ok = pm.get("MERCH003", {}).get("count") == 5
    r7_pass = m1_ok and m2_ok and m3_ok
    check("R7", r7_pass, f"per_merchant counts: MERCH001={pm.get('MERCH001',{}).get('count')}, MERCH002={pm.get('MERCH002',{}).get('count')}, MERCH003={pm.get('MERCH003',{}).get('count')}" if r7_pass else f"per_merchant mismatch: {pm}")

    # R8: average_transaction_amount
    expected_avg = round(expected_total / 15, 2)
    actual_avg = data.get("average_transaction_amount")
    r8_pass = isinstance(actual_avg, (int, float)) and abs(actual_avg - expected_avg) < 0.01
    check("R8", r8_pass, f"average_transaction_amount = {actual_avg}" if r8_pass else f"Expected {expected_avg:.2f}, got {actual_avg}")

    # R9: highest_value_txn
    hvt = data.get("highest_value_txn", {})
    r9_pass = hvt.get("id") == "TXN013" and abs(hvt.get("amount", 0) - 9200.00) < 0.01
    check("R9", r9_pass, f"highest_value_txn = {hvt}" if r9_pass else f"Expected TXN013/9200.00, got {hvt}")

    # R10: No extra fields beyond required schema
    required_keys = {"total_transaction_count", "total_amount", "total_fees", "net_amount", "per_card_type", "per_merchant", "average_transaction_amount", "highest_value_txn"}
    actual_keys = set(data.keys())
    extra = actual_keys - required_keys
    r10_pass = len(extra) == 0
    check("R10", r10_pass, "No extra fields" if r10_pass else f"Extra fields: {extra}")

    return finalize(results)

def finalize(results):
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    must_pass_ids = ["R1", "R2", "R3", "R4", "R5"]
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
