import json, sys, os
TASK_ID = "H_01"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_PATH = os.path.join(BASE, "results", "result.json")
GRADING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grading_result.json")
BOTH_FILES = ["doc_003_security.txt", "doc_004_security.txt", "doc_007_security.txt", "doc_008_cloud.txt", "doc_010_security.txt"]
EXCLUDED_FILES = ["doc_001_cloud.txt", "doc_002_cloud.txt", "doc_005_kubernetes.txt", "doc_006_kubernetes.txt", "doc_009_database.txt"]

def grade():
    if not os.path.exists(RESULT_PATH):
        return {"task_id": TASK_ID, "status": "fail", "outcome_status": "failed", "passed": 0, "total": 10, "must_pass_satisfied": False, "results": [{"rubric_id": "R1", "passed": False, "score": 0, "reason": "result.json not found", "evidence": {}}]}
    with open(RESULT_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            return {"task_id": TASK_ID, "status": "fail", "outcome_status": "failed", "passed": 0, "total": 10, "must_pass_satisfied": False, "results": [{"rubric_id": "R2", "passed": False, "score": 0, "reason": f"Invalid JSON: {e}", "evidence": {}}]}

    results = []
    p = 0
    must = {"R1": False, "R2": False, "R3": False, "R4": False, "R5": False, "R7": False}

    r1 = os.path.exists(RESULT_PATH)
    results.append({"rubric_id": "R1", "passed": r1, "score": 1 if r1 else 0, "reason": "OK" if r1 else "missing", "evidence": {}})
    if r1: p += 1; must["R1"] = r1

    r2 = all(k in data for k in ["query", "ranked_results", "total_criteria_matched_files"])
    results.append({"rubric_id": "R2", "passed": r2, "score": 1 if r2 else 0, "reason": "OK" if r2 else "missing keys", "evidence": {"keys": list(data.keys())}})
    if r2: p += 1; must["R2"] = r2

    r3 = isinstance(data.get("query"), dict) and "keywords" in data["query"] and "mode" in data["query"]
    results.append({"rubric_id": "R3", "passed": r3, "score": 1 if r3 else 0, "reason": "OK" if r3 else "bad query", "evidence": {"query": data.get("query")}})
    if r3: p += 1; must["R3"] = r3

    ranked = data.get("ranked_results", [])
    rfiles = [r.get("file", "") for r in ranked]
    r4 = all(f in rfiles for f in BOTH_FILES)
    results.append({"rubric_id": "R4", "passed": r4, "score": 1 if r4 else 0, "reason": "OK" if r4 else f"missing files: {set(BOTH_FILES)-set(rfiles)}", "evidence": {"matched": rfiles}})
    if r4: p += 1; must["R4"] = r4

    total = data.get("total_criteria_matched_files", 0)
    r5 = total == 5
    results.append({"rubric_id": "R5", "passed": r5, "score": 1 if r5 else 0, "reason": f"total={total}" if r5 else f"expected 5", "evidence": {"total": total}})
    if r5: p += 1; must["R5"] = r5

    r6 = all(isinstance(r, dict) and "file" in r and "cloud_count" in r and "security_count" in r and "lines" in r for r in ranked) if ranked else False
    results.append({"rubric_id": "R6", "passed": r6, "score": 1 if r6 else 0, "reason": "OK" if r6 else "bad entry format", "evidence": {}})
    if r6: p += 1

    sec_counts = {r["file"]: r["security_count"] for r in ranked}
    r7 = sec_counts.get("doc_007_security.txt", 0) >= 2
    results.append({"rubric_id": "R7", "passed": r7, "score": 1 if r7 else 0, "reason": f"doc_007_security_count={sec_counts.get('doc_007_security.txt')}" if r7 else "security_count too low", "evidence": {"counts": sec_counts}})
    if r7: p += 1; must["R7"] = r7

    r8 = all(f not in rfiles for f in EXCLUDED_FILES)
    results.append({"rubric_id": "R8", "passed": r8, "score": 1 if r8 else 0, "reason": "OK" if r8 else "excluded files found", "evidence": {}})
    if r8: p += 1

    WS_FILES = BOTH_FILES + EXCLUDED_FILES
    r9 = all(f in WS_FILES for f in rfiles)
    results.append({"rubric_id": "R9", "passed": r9, "score": 1 if r9 else 0, "reason": "OK" if r9 else "invalid files", "evidence": {}})
    if r9: p += 1

    r10 = all(len(r.get("lines", [])) > 0 for r in ranked) if ranked else False
    results.append({"rubric_id": "R10", "passed": r10, "score": 1 if r10 else 0, "reason": "OK" if r10 else "missing lines", "evidence": {}})
    if r10: p += 1

    all_must = all(must.values())
    status = "pass" if p >= 8 and all_must else ("partial" if p >= 5 else "fail")
    outcome = "satisfied" if status == "pass" else ("needs_revision" if status == "partial" else "failed")
    gr = {"task_id": TASK_ID, "status": status, "outcome_status": outcome, "passed": p, "total": 10, "must_pass_satisfied": all_must, "results": results}
    os.makedirs(os.path.dirname(GRADING_PATH), exist_ok=True)
    with open(GRADING_PATH, "w") as f:
        json.dump(gr, f, indent=2)
    return gr

if __name__ == "__main__":
    r = grade()
    print(json.dumps(r))
    sys.exit(0 if r["status"] == "pass" else 1)
