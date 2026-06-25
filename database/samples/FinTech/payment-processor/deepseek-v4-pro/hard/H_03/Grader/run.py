#!/usr/bin/env python3
import json, sys
from pathlib import Path

TASK_ID = "H_03"
RESULT_DIR = Path("results") / TASK_ID / "results"
RESULT_FILE = RESULT_DIR / "result.json"

REQUIRED_GATEWAYS = ["Stripe", "PayPal", "Square", "Adyen", "Braintree"]

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

    gc = data.get("gateway_comparison", [])
    r2_pass = len(gc) == 5
    check("R2", r2_pass, f"gateway_comparison has {len(gc)} entries" if r2_pass else f"Expected 5, got {len(gc)}")

    r3_pass = True
    required_keys = {"name", "pricing", "supported_payment_methods", "security_certifications", "api_type", "key_features"}
    for gw in gc:
        if not required_keys.issubset(gw.keys()):
            r3_pass = False
    check("R3", r3_pass, "All gateway entries have required keys" if r3_pass else "Some entries missing required keys")

    gw_names = [gw.get("name") for gw in gc]
    r4_pass = all(name in gw_names for name in REQUIRED_GATEWAYS)
    check("R4", r4_pass, f"All 5 gateways present: {gw_names}" if r4_pass else f"Missing some gateways: {gw_names}")

    r5_pass = True
    for gw in gc:
        pricing = gw.get("pricing", {})
        if "transaction_fee_percent" not in pricing or "monthly_fee" not in pricing:
            r5_pass = False
    check("R5", r5_pass, "All gateways have pricing with transaction_fee_percent and monthly_fee" if r5_pass else "Some gateways missing pricing fields")

    r6_pass = all(isinstance(gw.get("supported_payment_methods"), list) and len(gw["supported_payment_methods"]) >= 3 for gw in gc)
    check("R6", r6_pass, "All gateways have >=3 supported payment methods" if r6_pass else "Some gateways have <3 methods")

    r7_pass = all(isinstance(gw.get("security_certifications"), list) and len(gw["security_certifications"]) >= 2 for gw in gc)
    check("R7", r7_pass, "All gateways have >=2 security certifications" if r7_pass else "Some gateways have <2 certs")

    summary = data.get("summary", {})
    r8_keys = {"cheapest_option", "most_secure", "best_for_international", "best_overall"}
    r8_pass = isinstance(summary, dict) and r8_keys.issubset(summary.keys())
    check("R8", r8_pass, f"summary has all required keys: {list(summary.keys())}" if r8_pass else f"summary missing keys: {r8_keys - set(summary.keys())}")

    rec = data.get("recommended_gateways", {})
    r9_pass = isinstance(rec, dict) and len(rec) >= 3
    check("R9", r9_pass, f"recommended_gateways has {len(rec)} use-case entries" if r9_pass else f"recommended_gateways has <3 entries")

    # R10: realistic pricing
    r10_pass = True
    for gw in gc:
        pct = gw.get("pricing", {}).get("transaction_fee_percent")
        if not isinstance(pct, (int,float)) or pct < 1.5 or pct > 4.0:
            r10_pass = False
    check("R10", r10_pass, "All transaction fee percentages in realistic range (1.5-4.0%)" if r10_pass else "Some fee percentages outside realistic range")

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
