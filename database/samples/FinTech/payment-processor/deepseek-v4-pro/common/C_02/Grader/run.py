#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

TASK_ID = "C_02"
RESULT_DIR = Path("results") / TASK_ID / "results"
RESULT_FILE = RESULT_DIR / "result.json"

TRANSACTIONS = [
    {"txn_id":"T101","date":"2026-02-01","amount":500.00},
    {"txn_id":"T102","date":"2026-02-01","amount":1200.00},
    {"txn_id":"T103","date":"2026-02-02","amount":350.00},
    {"txn_id":"T104","date":"2026-02-02","amount":2800.00},
    {"txn_id":"T105","date":"2026-02-03","amount":150.00},
    {"txn_id":"T106","date":"2026-02-03","amount":890.00},
    {"txn_id":"T107","date":"2026-02-04","amount":2200.00},
    {"txn_id":"T108","date":"2026-02-04","amount":675.00},
    {"txn_id":"T109","date":"2026-02-05","amount":4300.00},
    {"txn_id":"T110","date":"2026-02-05","amount":950.00},
]

STATEMENTS = [
    {"st_id":"STMT001","date":"2026-02-01","amount":500.00},
    {"st_id":"STMT002","date":"2026-02-01","amount":1200.00},
    {"st_id":"STMT003","date":"2026-02-02","amount":350.00},
    {"st_id":"STMT004","date":"2026-02-02","amount":2800.00},
    {"st_id":"STMT005","date":"2026-02-03","amount":150.00},
    {"st_id":"STMT006","date":"2026-02-03","amount":890.00},
    {"st_id":"STMT007","date":"2026-02-04","amount":2200.00},
    {"st_id":"STMT008","date":"2026-02-04","amount":675.00},
    {"st_id":"STMT009","date":"2026-02-05","amount":4300.00},
    {"st_id":"STMT010","date":"2026-02-05","amount":950.00},
    {"st_id":"STMT011","date":"2026-02-06","amount":2000.00},
]

MATCHED_PAIRS = [
    ("T101","STMT001"),("T102","STMT002"),("T103","STMT003"),("T104","STMT004"),
    ("T105","STMT005"),("T106","STMT006"),("T107","STMT007"),("T108","STMT008"),
    ("T109","STMT009"),("T110","STMT010"),
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

    # R2: total_matched_count = 10
    r2_pass = data.get("total_matched_count") == 10
    check("R2", r2_pass, f"total_matched_count = {data.get('total_matched_count')}" if r2_pass else f"Expected 10, got {data.get('total_matched_count')}")

    # R3: matched entries
    matched = data.get("matched", [])
    r3_ok = True
    for txn_id, stmt_id in MATCHED_PAIRS:
        found = any(m.get("txn_id") == txn_id and m.get("statement_id") == stmt_id for m in matched)
        if not found:
            r3_ok = False
            break
    r3_pass = r3_ok and len(matched) == 10
    check("R3", r3_pass, "All 10 matched pairs correct" if r3_pass else "Matched pairs incorrect or incomplete")

    # R4: total_reconciled_amount = 14065.00
    expected_reconciled = sum(t["amount"] for t in TRANSACTIONS)
    actual_reconciled = data.get("total_reconciled_amount")
    r4_pass = isinstance(actual_reconciled, (int,float)) and abs(actual_reconciled - expected_reconciled) < 0.01
    check("R4", r4_pass, f"total_reconciled_amount = {actual_reconciled}" if r4_pass else f"Expected {expected_reconciled:.2f}, got {actual_reconciled}")

    # R5: unmatched_transactions is an array
    um_txns = data.get("unmatched_transactions", [])
    r5_pass = isinstance(um_txns, list)
    check("R5", r5_pass, "unmatched_transactions is a list" if r5_pass else "unmatched_transactions not a list")

    # R6: unmatched_statements is an array
    um_stmts = data.get("unmatched_statements", [])
    r6_pass = isinstance(um_stmts, list)
    check("R6", r6_pass, "unmatched_statements is a list" if r6_pass else "unmatched_statements not a list")

    # R7: unmatched_transactions empty (0)
    r7_pass = len(um_txns) == 0
    check("R7", r7_pass, f"unmatched_transactions empty (count={len(um_txns)})" if r7_pass else f"Expected empty, got {len(um_txns)} entries")

    # R8: unmatched_statements has STMT011
    r8_pass = len(um_stmts) == 1
    if r8_pass:
        entry = um_stmts[0]
        r8_pass = entry.get("statement_id") == "STMT011" and isinstance(entry.get("amount"), (int,float)) and abs(entry["amount"] - 2000.00) < 0.01
    check("R8", r8_pass, "unmatched_statements contains STMT011/2000.00" if r8_pass else f"unmatched_statements incorrect: {um_stmts}")

    # R9: has_discrepancies = false
    r9_pass = data.get("has_discrepancies") is False
    check("R9", r9_pass, f"has_discrepancies = {data.get('has_discrepancies')}" if r9_pass else f"Expected False, got {data.get('has_discrepancies')}")

    # R10: amounts are floats not strings
    r10_pass = True
    for entry in matched + um_txns + um_stmts:
        if isinstance(entry, dict) and "amount" in entry:
            if isinstance(entry["amount"], str):
                r10_pass = False
                break
    check("R10", r10_pass, "All amounts are numeric" if r10_pass else "Some amounts are strings")

    return finalize(results)

def finalize(results):
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    must_pass_ids = ["R1","R2","R3","R4"]
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
