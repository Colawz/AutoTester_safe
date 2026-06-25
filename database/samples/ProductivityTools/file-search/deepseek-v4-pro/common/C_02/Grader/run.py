import json, sys, os
TASK_ID = "C_02"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_PATH = os.path.join(BASE, "results", "result.json")
GRADING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grading_result.json")
WS_FILES = ["fruits_apple.txt", "tropical_banana.txt", "fruit_bowl_apple_banana.txt", "citrus_orange.txt", "berry_notes.txt"]
EXPECTED_MATCH = "fruit_bowl_apple_banana.txt"
EXCLUDED_APPLE_ONLY = "fruits_apple.txt"
EXCLUDED_BANANA_ONLY = "tropical_banana.txt"
EXCLUDED_NEITHER = ["citrus_orange.txt", "berry_notes.txt"]

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
    must = {"R1": False, "R2": False, "R4": False, "R5": False}

    matches = data.get("matches", [])
    mfiles = [m.get("file", "") for m in matches]

    r1 = os.path.exists(RESULT_PATH)
    results.append({"rubric_id": "R1", "passed": r1, "score": 1 if r1 else 0, "reason": "OK" if r1 else "missing", "evidence": {}})
    if r1: p += 1
    must["R1"] = r1

    r2 = "matches" in data and isinstance(matches, list) and len(matches) > 0
    results.append({"rubric_id": "R2", "passed": r2, "score": 1 if r2 else 0, "reason": "OK" if r2 else "bad format", "evidence": {"count": len(matches)}})
    if r2: p += 1
    must["R2"] = r2

    r3 = all(isinstance(m, dict) and "file" in m and "matched_keywords" in m and "line_numbers" in m and "lines" in m for m in matches)
    results.append({"rubric_id": "R3", "passed": r3, "score": 1 if r3 else 0, "reason": "OK" if r3 else "missing fields", "evidence": {}})
    if r3: p += 1

    r4 = EXPECTED_MATCH in mfiles
    results.append({"rubric_id": "R4", "passed": r4, "score": 1 if r4 else 0, "reason": "OK" if r4 else "not in matches", "evidence": {"found": mfiles}})
    if r4: p += 1
    must["R4"] = r4

    r5 = EXCLUDED_APPLE_ONLY not in mfiles
    results.append({"rubric_id": "R5", "passed": r5, "score": 1 if r5 else 0, "reason": "OK" if r5 else "should be excluded", "evidence": {}})
    if r5: p += 1
    must["R5"] = r5

    r6 = EXCLUDED_BANANA_ONLY not in mfiles
    results.append({"rubric_id": "R6", "passed": r6, "score": 1 if r6 else 0, "reason": "OK" if r6 else "should be excluded", "evidence": {}})
    if r6: p += 1

    r7 = all(f not in mfiles for f in EXCLUDED_NEITHER)
    results.append({"rubric_id": "R7", "passed": r7, "score": 1 if r7 else 0, "reason": "OK" if r7 else "should be excluded", "evidence": {}})
    if r7: p += 1

    r8 = False
    for m in matches:
        if m.get("file") == EXPECTED_MATCH:
            kw = m.get("matched_keywords", [])
            r8 = isinstance(kw, list) and ("apple" in [k.lower() for k in kw]) and ("banana" in [k.lower() for k in kw])
            break
    results.append({"rubric_id": "R8", "passed": r8, "score": 1 if r8 else 0, "reason": "OK" if r8 else "missing keywords", "evidence": {}})
    if r8: p += 1

    r9 = all(f in WS_FILES for f in mfiles) and len(mfiles) >= 1
    results.append({"rubric_id": "R9", "passed": r9, "score": 1 if r9 else 0, "reason": "OK" if r9 else "invalid files", "evidence": {}})
    if r9: p += 1

    r10 = len(matches) == 1
    results.append({"rubric_id": "R10", "passed": r10, "score": 1 if r10 else 0, "reason": f"count={len(matches)}" if r10 else f"expected 1, got {len(matches)}", "evidence": {"count": len(matches)}})
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
