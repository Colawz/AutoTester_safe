#!/usr/bin/env python3
import json, sys
from pathlib import Path

TASK_ID = "H_01"
RESULT_DIR = Path("results") / TASK_ID / "results"
RESULT_FILE = RESULT_DIR / "result.json"

EXPECTED_USD = {
    "H001": 5000.00,
    "H002": 3815.00,
    "H003": 660.00,
    "H004": 3318.00,
    "H005": 750.00,
    "H006": 9120.00,
    "H007": 2725.00,
    "H008": 15000.00,
    "H009": 1980.00,
    "H010": 7620.00,
}

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

    txns = data.get("transactions", [])
    r2_pass = len(txns) == 10
    check("R2", r2_pass, f"transactions count = {len(txns)}" if r2_pass else f"Expected 10, got {len(txns)}")

    r3_pass = all("txn_id" in t and "original_amount" in t and "original_currency" in t and "usd_equivalent" in t and "exchange_rate_used" in t for t in txns)
    check("R3", r3_pass, "All transactions have required fields" if r3_pass else "Some transactions missing required fields")

    txn_map = {t.get("txn_id"): t for t in txns}
    r4_pass = "H001" in txn_map and abs(txn_map["H001"].get("usd_equivalent", 0) - EXPECTED_USD["H001"]) < 0.01
    check("R4", r4_pass, f"H001 usd_equivalent = {txn_map.get('H001',{}).get('usd_equivalent')}" if r4_pass else f"H001 expected {EXPECTED_USD['H001']:.2f}, got {txn_map.get('H001',{}).get('usd_equivalent')}")

    r5_pass = "H002" in txn_map and abs(txn_map["H002"].get("usd_equivalent", 0) - EXPECTED_USD["H002"]) < 0.01
    check("R5", r5_pass, f"H002 usd_equivalent = {txn_map.get('H002',{}).get('usd_equivalent')}" if r5_pass else f"H002 expected {EXPECTED_USD['H002']:.2f}, got {txn_map.get('H002',{}).get('usd_equivalent')}")

    r6_pass = "H003" in txn_map and abs(txn_map["H003"].get("usd_equivalent", 0) - EXPECTED_USD["H003"]) < 0.01
    check("R6", r6_pass, f"H003 usd_equivalent = {txn_map.get('H003',{}).get('usd_equivalent')}" if r6_pass else f"H003 expected {EXPECTED_USD['H003']:.2f}, got {txn_map.get('H003',{}).get('usd_equivalent')}")

    # R7: by_merchant
    by_merchant = data.get("by_merchant", {})
    # GlobalMerchant: H001(5000) + H002(3815) + H004(3318) + H005(750) + H006(9120) + H008(15000) + H010(7620) = 44623
    # EuroShop: H003(660) + H007(2725) + H009(1980) = 5365
    global_total = sum(EXPECTED_USD[h] for h in ["H001","H002","H004","H005","H006","H008","H010"])
    euro_total = sum(EXPECTED_USD[h] for h in ["H003","H007","H009"])
    gm = by_merchant.get("GlobalMerchant", {})
    es = by_merchant.get("EuroShop", {})
    r7_pass = abs(gm.get("total_usd", 0) - global_total) < 0.01 and abs(es.get("total_usd", 0) - euro_total) < 0.01
    check("R7", r7_pass, "by_merchant totals correct" if r7_pass else f"by_merchant incorrect: {by_merchant}")

    # R8: by_currency
    by_currency = data.get("by_currency", {})
    r8_pass = len(by_currency) == 5
    check("R8", r8_pass, f"by_currency has {len(by_currency)} entries" if r8_pass else f"Expected 5 currency entries, got {len(by_currency)}")

    # R9: overall
    overall = data.get("overall", {})
    total_usd = sum(EXPECTED_USD.values())
    avg_usd = round(total_usd / 10, 2)
    r9_pass = overall.get("count") == 10 and isinstance(overall.get("total_usd"), (int,float)) and abs(overall["total_usd"] - total_usd) < 0.01
    if r9_pass:
        r9_pass = isinstance(overall.get("average_usd"), (int,float)) and abs(overall["average_usd"] - avg_usd) < 0.01
    check("R9", r9_pass, f"overall: count=10, total={total_usd:.2f}, avg={avg_usd:.2f}" if r9_pass else f"overall incorrect: {overall}")

    # R10: all usd_equivalent rounded to 2 decimals
    r10_pass = all(isinstance(t.get("usd_equivalent"), (int,float)) and round(t["usd_equivalent"], 2) == t["usd_equivalent"] for t in txns)
    check("R10", r10_pass, "All usd_equivalent values rounded to 2 decimals" if r10_pass else "Some usd_equivalent not rounded to 2 decimals")

    return finalize(results)

def finalize(results):
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    must_pass_ids = ["R1","R2","R4","R5","R6"]
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
