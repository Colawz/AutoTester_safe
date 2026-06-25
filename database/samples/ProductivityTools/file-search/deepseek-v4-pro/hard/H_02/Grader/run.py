import json, sys, os
TASK_ID = "H_02"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_PATH = os.path.join(BASE, "results", "result.json")
GRADING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grading_result.json")

ACME_FILE = "company_report.txt"
RODRIGUEZ_FILE = "project_nexus.txt"
CROSS_FILES = [ACME_FILE, RODRIGUEZ_FILE]

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
    must = {"R1": False, "R2": False, "R3": False, "R4": False, "R5": False, "R8": False}

    r1 = os.path.exists(RESULT_PATH)
    results.append({"rubric_id": "R1", "passed": r1, "score": 1 if r1 else 0, "reason": "OK" if r1 else "missing", "evidence": {}})
    if r1: p += 1; must["R1"] = r1

    r2 = all(k in data for k in ["entities", "cross_references", "summary"])
    results.append({"rubric_id": "R2", "passed": r2, "score": 1 if r2 else 0, "reason": "OK" if r2 else "missing keys", "evidence": {"keys": list(data.keys())}})
    if r2: p += 1; must["R2"] = r2

    entities = data.get("entities", [])
    r3 = isinstance(entities, list) and len(entities) == 2 and all("name" in e and "files" in e and "total_mentions" in e for e in entities)
    results.append({"rubric_id": "R3", "passed": r3, "score": 1 if r3 else 0, "reason": "OK" if r3 else "bad entities", "evidence": {}})
    if r3: p += 1; must["R3"] = r3

    cross = data.get("cross_references", [])
    r4 = all(f in cross for f in CROSS_FILES)
    results.append({"rubric_id": "R4", "passed": r4, "score": 1 if r4 else 0, "reason": "OK" if r4 else f"missing {CROSS_FILES}", "evidence": {"cross": cross}})
    if r4: p += 1; must["R4"] = r4

    acme_entity = next((e for e in entities if "Acme" in e.get("name", "")), {})
    rodriguez_entity = next((e for e in entities if "Rodriguez" in e.get("name", "") or "Maria" in e.get("name", "")), {})
    r5 = acme_entity.get("total_mentions", 0) >= 1
    results.append({"rubric_id": "R5", "passed": r5, "score": 1 if r5 else 0, "reason": f"Acme mentions: {acme_entity.get('total_mentions')}" if r5 else "no Acme mentions", "evidence": {"acme": acme_entity}})
    if r5: p += 1; must["R5"] = r5

    r6 = rodriguez_entity.get("total_mentions", 0) >= 1
    results.append({"rubric_id": "R6", "passed": r6, "score": 1 if r6 else 0, "reason": "OK" if r6 else "no Rodriguez mentions", "evidence": {"rodriguez": rodriguez_entity}})
    if r6: p += 1

    r7 = all(f not in cross for f in ["competitor_analysis.txt", "market_trends.txt"])
    results.append({"rubric_id": "R7", "passed": r7, "score": 1 if r7 else 0, "reason": "OK" if r7 else "extra files in cross", "evidence": {}})
    if r7: p += 1

    summary = data.get("summary", {})
    r8 = all(k in summary for k in ["total_entity_files", "total_cross_reference_files", "entities_searched"])
    results.append({"rubric_id": "R8", "passed": r8, "score": 1 if r8 else 0, "reason": "OK" if r8 else "bad summary", "evidence": {"summary": summary}})
    if r8: p += 1; must["R8"] = r8

    r9 = isinstance(cross, list) and len(cross) == 2
    results.append({"rubric_id": "R9", "passed": r9, "score": 1 if r9 else 0, "reason": "OK" if r9 else "bad cross refs", "evidence": {}})
    if r9: p += 1

    r10 = summary.get("total_cross_reference_files", 0) == 2
    results.append({"rubric_id": "R10", "passed": r10, "score": 1 if r10 else 0, "reason": f"cross_count={summary.get('total_cross_reference_files')}" if r10 else "expected 2", "evidence": {"cross_count": summary.get("total_cross_reference_files")}})
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
