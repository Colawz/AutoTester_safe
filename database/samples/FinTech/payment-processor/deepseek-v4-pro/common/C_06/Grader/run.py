#!/usr/bin/env python3
import json, sys
from pathlib import Path

TASK_ID = "C_06"
RESULT_DIR = Path("results") / TASK_ID / "results"
RESULT_FILE = RESULT_DIR / "result.json"

TRANSACTIONS = [
    {"date":"2026-04-01","amount":250.00,"merchant":"MerchantA","card_type":"Visa","status":"completed"},
    {"date":"2026-04-01","amount":1800.00,"merchant":"MerchantB","card_type":"Mastercard","status":"completed"},
    {"date":"2026-04-01","amount":95.00,"merchant":"MerchantA","card_type":"Amex","status":"completed"},
    {"date":"2026-04-02","amount":3200.00,"merchant":"MerchantC","card_type":"Visa","status":"completed"},
    {"date":"2026-04-02","amount":150.00,"merchant":"MerchantB","card_type":"Mastercard","status":"pending"},
    {"date":"2026-04-02","amount":780.00,"merchant":"MerchantA","card_type":"Visa","status":"completed"},
    {"date":"2026-04-03","amount":4500.00,"merchant":"MerchantC","card_type":"Amex","status":"completed"},
    {"date":"2026-04-03","amount":299.99,"merchant":"MerchantB","card_type":"Mastercard","status":"completed"},
    {"date":"2026-04-03","amount":1250.00,"merchant":"MerchantA","card_type":"Visa","status":"failed"},
    {"date":"2026-04-04","amount":675.00,"merchant":"MerchantC","card_type":"Mastercard","status":"completed"},
    {"date":"2026-04-04","amount":4300.00,"merchant":"MerchantB","card_type":"Visa","status":"completed"},
    {"date":"2026-04-04","amount":89.99,"merchant":"MerchantA","card_type":"Amex","status":"pending"},
]

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

    overall = data.get("overall", {})
    r2_pass = overall.get("count") == 12
    check("R2", r2_pass, f"overall.count = {overall.get('count')}" if r2_pass else f"Expected 12, got {overall.get('count')}")

    expected_total = sum(t["amount"] for t in TRANSACTIONS)
    r3_pass = isinstance(overall.get("total_amount"), (int,float)) and abs(overall["total_amount"] - expected_total) < 0.01
    check("R3", r3_pass, f"overall.total_amount = {overall.get('total_amount')}" if r3_pass else f"Expected {expected_total:.2f}, got {overall.get('total_amount')}")

    # R4: by_date
    by_date = data.get("by_date", {})
    date_groups = {}
    for t in TRANSACTIONS:
        date_groups.setdefault(t["date"], []).append(t["amount"])
    r4_pass = True
    for d, amounts in date_groups.items():
        entry = by_date.get(d, {})
        exp_total = sum(amounts)
        exp_count = len(amounts)
        if entry.get("count") != exp_count or abs(entry.get("total_amount", 0) - exp_total) >= 0.01:
            r4_pass = False
    r4_pass = r4_pass and len(by_date) == 4
    check("R4", r4_pass, "by_date correct with 4 date entries" if r4_pass else "by_date incorrect")

    # R5: by_merchant
    by_merchant = data.get("by_merchant", {})
    merchant_groups = {}
    for t in TRANSACTIONS:
        merchant_groups.setdefault(t["merchant"], []).append(t["amount"])
    r5_pass = True
    for m, amounts in merchant_groups.items():
        entry = by_merchant.get(m, {})
        if entry.get("count") != len(amounts) or abs(entry.get("total_amount", 0) - sum(amounts)) >= 0.01:
            r5_pass = False
    r5_pass = r5_pass and len(by_merchant) == 3
    check("R5", r5_pass, "by_merchant correct with 3 merchant entries" if r5_pass else "by_merchant incorrect")

    # R6: by_card_type
    by_card_type = data.get("by_card_type", {})
    ct_groups = {}
    for t in TRANSACTIONS:
        ct_groups.setdefault(t["card_type"], []).append(t["amount"])
    r6_pass = True
    for ct, amounts in ct_groups.items():
        entry = by_card_type.get(ct, {})
        if entry.get("count") != len(amounts) or abs(entry.get("total_amount", 0) - sum(amounts)) >= 0.01:
            r6_pass = False
    r6_pass = r6_pass and len(by_card_type) == 3
    check("R6", r6_pass, "by_card_type correct" if r6_pass else f"by_card_type incorrect: {by_card_type}")

    # R7: by_status
    by_status = data.get("by_status", {})
    r7_pass = by_status.get("completed") == 8 and by_status.get("pending") == 2 and by_status.get("failed") == 1
    check("R7", r7_pass, f"by_status: completed=8, pending=2, failed=1" if r7_pass else f"by_status incorrect: {by_status}")

    # R8: each group has all required fields
    r8_pass = True
    for group_key in ["overall", "by_date", "by_merchant", "by_card_type"]:
        obj = data.get(group_key, {})
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, dict):
                    if not all(f in v for f in ["count", "total_amount", "average_amount"]):
                        r8_pass = False
    check("R8", r8_pass, "All groups have count, total_amount, average_amount" if r8_pass else "Missing fields in some groups")

    # R9: average_amount values correct
    r9_pass = True
    avg_expected = round(expected_total / 12, 2)
    if abs(overall.get("average_amount", 0) - avg_expected) >= 0.01:
        r9_pass = False
    for d, amounts in date_groups.items():
        entry = by_date.get(d, {})
        exp_avg = round(sum(amounts) / len(amounts), 2)
        if abs(entry.get("average_amount", 0) - exp_avg) >= 0.01:
            r9_pass = False
    check("R9", r9_pass, "All average_amount values correct" if r9_pass else "Some average_amount values incorrect")

    # R10: no unexpected status values
    valid_statuses = {"completed", "pending", "failed"}
    actual_statuses = set(by_status.keys())
    r10_pass = actual_statuses.issubset(valid_statuses)
    check("R10", r10_pass, f"Status keys: {actual_statuses}" if r10_pass else f"Unexpected status keys: {actual_statuses - valid_statuses}")

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
