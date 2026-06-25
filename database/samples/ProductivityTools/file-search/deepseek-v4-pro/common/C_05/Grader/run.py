import json, sys, os
TASK_ID = "C_05"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_PATH = os.path.join(BASE, "results", "result.json")
GRADING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grading_result.json")

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
    must = {"R1": False, "R2": False, "R3": False, "R5": False, "R8": False}

    r1 = os.path.exists(RESULT_PATH)
    results.append({"rubric_id": "R1", "passed": r1, "score": 1 if r1 else 0, "reason": "OK" if r1 else "missing", "evidence": {}})
    if r1: p += 1; must["R1"] = r1

    r2 = all(k in data for k in ["total_occurrences", "files", "search_term"])
    results.append({"rubric_id": "R2", "passed": r2, "score": 1 if r2 else 0, "reason": "OK" if r2 else "missing keys", "evidence": {"keys": list(data.keys())}})
    if r2: p += 1; must["R2"] = r2

    r3 = data.get("search_term") == "machine learning"
    results.append({"rubric_id": "R3", "passed": r3, "score": 1 if r3 else 0, "reason": f"OK: {data.get('search_term')}" if r3 else f"wrong: {data.get('search_term')}", "evidence": {"search_term": data.get("search_term")}})
    if r3: p += 1; must["R3"] = r3

    files = data.get("files", [])
    r4 = all(isinstance(f, dict) and "file" in f and "occurrence_count" in f and "lines" in f for f in files) if files else False
    results.append({"rubric_id": "R4", "passed": r4, "score": 1 if r4 else 0, "reason": "OK" if r4 else "bad format", "evidence": {}})
    if r4: p += 1

    paper1_count = 0
    paper2_count = 0
    paper3_count = 0
    for f in files:
        if f["file"] == "paper1.txt": paper1_count = f["occurrence_count"]
        if f["file"] == "paper2.txt": paper2_count = f["occurrence_count"]
        if f["file"] == "paper3.txt": paper3_count = f["occurrence_count"]
    r5 = paper1_count == 3
    results.append({"rubric_id": "R5", "passed": r5, "score": 1 if r5 else 0, "reason": f"paper1: {paper1_count}" if r5 else f"expected 3, got {paper1_count}", "evidence": {"paper1_count": paper1_count}})
    if r5: p += 1; must["R5"] = r5

    r6 = paper2_count == 2 and paper3_count == 3
    results.append({"rubric_id": "R6", "passed": r6, "score": 1 if r6 else 0, "reason": f"paper2={paper2_count}, paper3={paper3_count}" if r6 else f"expected 2,3 got {paper2_count},{paper3_count}", "evidence": {"paper2_count": paper2_count, "paper3_count": paper3_count}})
    if r6: p += 1

    paper4_entry = [f for f in files if f["file"] == "paper4.txt"]
    r7 = len(paper4_entry) == 0 or paper4_entry[0]["occurrence_count"] == 0
    results.append({"rubric_id": "R7", "passed": r7, "score": 1 if r7 else 0, "reason": "OK" if r7 else "paper4 has unexpected count", "evidence": {}})
    if r7: p += 1

    total = data.get("total_occurrences", 0)
    expected_total = paper1_count + paper2_count + paper3_count
    r8 = total == (3 + 2 + 3)
    results.append({"rubric_id": "R8", "passed": r8, "score": 1 if r8 else 0, "reason": f"total={total}" if r8 else f"expected 8, got {total}", "evidence": {"total": total}})
    if r8: p += 1; must["R8"] = r8

    r9 = all(f["occurrence_count"] > 0 for f in files if f["file"] != "paper4.txt")
    results.append({"rubric_id": "R9", "passed": r9, "score": 1 if r9 else 0, "reason": "OK" if r9 else "zero counts", "evidence": {}})
    if r9: p += 1

    r10 = all(any("machine learning" in line.lower() for line in f.get("lines", [])) for f in files if f.get("occurrence_count", 0) > 0)
    results.append({"rubric_id": "R10", "passed": r10, "score": 1 if r10 else 0, "reason": "OK" if r10 else "lines missing keyword", "evidence": {}})
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
