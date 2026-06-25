#!/usr/bin/env python3
import json, sys
from pathlib import Path

TASK_ID = "C_04"
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

    r2_pass = data.get("invoice_number") == "INV-2026-001"
    check("R2", r2_pass, f"invoice_number = {data.get('invoice_number')}" if r2_pass else f"Expected INV-2026-001, got {data.get('invoice_number')}")

    merchant = data.get("merchant", {})
    r3_pass = merchant.get("name") == "GlobalShop Inc."
    check("R3", r3_pass, f"merchant.name = {merchant.get('name')}" if r3_pass else f"Expected GlobalShop Inc., got {merchant.get('name')}")

    customer = data.get("customer", {})
    r4_pass = customer.get("name") == "Alice Johnson"
    check("R4", r4_pass, f"customer.name = {customer.get('name')}" if r4_pass else f"Expected Alice Johnson, got {customer.get('name')}")

    items = data.get("items", [])
    expected_descs = ["Premium Widget", "Basic Gadget", "Shipping & Handling"]
    r5_pass = len(items) == 3 and all(it.get("description") in expected_descs for it in items)
    check("R5", r5_pass, f"items count = {len(items)}" if r5_pass else f"Expected 3 items, got {len(items)}: {[it.get('description') for it in items]}")

    r6_pass = True
    expected_extended = {"Premium Widget": 99.98, "Basic Gadget": 129.99, "Shipping & Handling": 15.00}
    for it in items:
        desc = it.get("description", "")
        exp = expected_extended.get(desc)
        if exp is None or abs(it.get("extended_price", 0) - exp) >= 0.01:
            r6_pass = False
    check("R6", r6_pass, "All extended prices correct" if r6_pass else "Extended price mismatch")

    subtotal = data.get("subtotal")
    r7_pass = isinstance(subtotal, (int,float)) and abs(subtotal - 244.97) < 0.01
    check("R7", r7_pass, f"subtotal = {subtotal}" if r7_pass else f"Expected 244.97, got {subtotal}")

    tax = data.get("tax")
    # 244.97 * 0.08 = 19.5976, round to 19.60
    r8_pass = isinstance(tax, (int,float)) and abs(tax - 19.60) < 0.01
    check("R8", r8_pass, f"tax = {tax}" if r8_pass else f"Expected 19.60, got {tax}")

    total = data.get("total")
    r9_pass = isinstance(total, (int,float)) and abs(total - 264.57) < 0.01
    check("R9", r9_pass, f"total = {total}" if r9_pass else f"Expected 264.57, got {total}")

    inv_text = data.get("invoice_text", "")
    r10_pass = isinstance(inv_text, str) and len(inv_text) > 50 and "INV-2026-001" in inv_text
    check("R10", r10_pass, "invoice_text is non-empty and contains invoice number" if r10_pass else f"invoice_text invalid (len={len(inv_text) if isinstance(inv_text, str) else 'N/A'})")

    return finalize(results)

def finalize(results):
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    must_pass_ids = ["R1","R2","R5","R6","R7"]
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
