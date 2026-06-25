import json, sys, os
TASK_ID = "H_03"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_PATH = os.path.join(BASE, "results", "result.json")
GRADING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grading_result.json")

ALL_FILES = ["animal_mammals.txt", "animal_birds.txt", "animal_reptiles.txt", "animal_aquatic.txt", "animal_domestic.txt", "animal_wildlife.txt", "animal_prehistoric.txt"]

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
    must = {"R1": False, "R2": False, "R3": False, "R4": False, "R6": False}

    r1 = os.path.exists(RESULT_PATH)
    results.append({"rubric_id": "R1", "passed": r1, "score": 1 if r1 else 0, "reason": "OK" if r1 else "missing", "evidence": {}})
    if r1: p += 1; must["R1"] = r1

    r2 = all(k in data for k in ["query", "file_count", "files_matching", "matches"])
    results.append({"rubric_id": "R2", "passed": r2, "score": 1 if r2 else 0, "reason": "OK" if r2 else "missing keys", "evidence": {"keys": list(data.keys())}})
    if r2: p += 1; must["R2"] = r2

    query = data.get("query", {})
    r3 = isinstance(query, dict) and any(k in query for k in ["include_any", "require_all", "exclude"])
    results.append({"rubric_id": "R3", "passed": r3, "score": 1 if r3 else 0, "reason": "OK" if r3 else "bad query", "evidence": {"query": query}})
    if r3: p += 1; must["R3"] = r3

    fmatches = data.get("files_matching", [])
    r4 = "animal_mammals.txt" in fmatches
    results.append({"rubric_id": "R4", "passed": r4, "score": 1 if r4 else 0, "reason": "OK" if r4 else "mammals missing", "evidence": {"files": fmatches}})
    if r4: p += 1; must["R4"] = r4

    r5 = "animal_domestic.txt" in fmatches
    results.append({"rubric_id": "R5", "passed": r5, "score": 1 if r5 else 0, "reason": "OK" if r5 else "domestic missing", "evidence": {}})
    if r5: p += 1

    r6 = "animal_prehistoric.txt" not in fmatches
    results.append({"rubric_id": "R6", "passed": r6, "score": 1 if r6 else 0, "reason": "OK" if r6 else "prehistoric should be excluded", "evidence": {}})
    if r6: p += 1; must["R6"] = r6

    r7 = all(f in ALL_FILES for f in fmatches)
    results.append({"rubric_id": "R7", "passed": r7, "score": 1 if r7 else 0, "reason": "OK" if r7 else "invalid file names", "evidence": {}})
    if r7: p += 1

    matches = data.get("matches", [])
    r8 = all(isinstance(m, dict) and "file" in m and "matched_terms" in m and "lines" in m for m in matches) if matches else False
    results.append({"rubric_id": "R8", "passed": r8, "score": 1 if r8 else 0, "reason": "OK" if r8 else "bad format", "evidence": {}})
    if r8: p += 1

    r9 = all(f in ALL_FILES for f in fmatches) and len(fmatches) >= 1
    results.append({"rubric_id": "R9", "passed": r9, "score": 1 if r9 else 0, "reason": "OK" if r9 else "bad entries", "evidence": {}})
    if r9: p += 1

    fc = data.get("file_count", 0)
    r10 = fc == len(fmatches) and fc >= 1
    results.append({"rubric_id": "R10", "passed": r10, "score": 1 if r10 else 0, "reason": f"file_count={fc}" if r10 else "mismatch", "evidence": {"file_count": fc, "actual": len(fmatches)}})
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
