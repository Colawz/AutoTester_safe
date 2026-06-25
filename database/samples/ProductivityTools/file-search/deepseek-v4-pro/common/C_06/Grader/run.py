import json, sys, os
TASK_ID = "C_06"
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
    must = {"R1": False, "R2": False, "R3": False, "R4": False, "R5": False}
    matches = data.get("matches", [])

    r1 = os.path.exists(RESULT_PATH)
    results.append({"rubric_id": "R1", "passed": r1, "score": 1 if r1 else 0, "reason": "OK" if r1 else "missing", "evidence": {}})
    if r1: p += 1; must["R1"] = r1

    r2 = "matches" in data and isinstance(matches, list)
    results.append({"rubric_id": "R2", "passed": r2, "score": 1 if r2 else 0, "reason": "OK" if r2 else "bad", "evidence": {}})
    if r2: p += 1; must["R2"] = r2

    r3 = all(isinstance(m, dict) and "file" in m and "line_number" in m and "matched_line" in m and "context" in m for m in matches) if matches else False
    results.append({"rubric_id": "R3", "passed": r3, "score": 1 if r3 else 0, "reason": "OK" if r3 else "missing fields", "evidence": {}})
    if r3: p += 1; must["R3"] = r3

    r4 = all(isinstance(m.get("context"), dict) and ("before" in m["context"]) and ("after" in m["context"]) for m in matches) if matches else False
    results.append({"rubric_id": "R4", "passed": r4, "score": 1 if r4 else 0, "reason": "OK" if r4 else "bad context", "evidence": {}})
    if r4: p += 1; must["R4"] = r4

    ch1_matches = [m for m in matches if m.get("file") == "chapter1.txt"]
    r5 = len(ch1_matches) == 2
    results.append({"rubric_id": "R5", "passed": r5, "score": 1 if r5 else 0, "reason": f"chapter1: {len(ch1_matches)}" if r5 else f"expected 2, got {len(ch1_matches)}", "evidence": {"chapter1_count": len(ch1_matches)}})
    if r5: p += 1; must["R5"] = r5

    ch2_matches = [m for m in matches if m.get("file") == "chapter2.txt"]
    r6 = len(ch2_matches) == 2
    results.append({"rubric_id": "R6", "passed": r6, "score": 1 if r6 else 0, "reason": f"chapter2: {len(ch2_matches)}" if r6 else f"expected 2, got {len(ch2_matches)}", "evidence": {"chapter2_count": len(ch2_matches)}})
    if r6: p += 1

    r7 = any(m.get("line_number") == 4 and m.get("context", {}).get("before") is not None for m in ch1_matches)
    results.append({"rubric_id": "R7", "passed": r7, "score": 1 if r7 else 0, "reason": "OK" if r7 else "no context for line 4", "evidence": {}})
    if r7: p += 1

    last_match = matches[-1] if matches else {}
    r8 = last_match.get("context", {}).get("after") is not None if last_match else False
    results.append({"rubric_id": "R8", "passed": r8, "score": 1 if r8 else 0, "reason": "OK" if r8 else "last match lacks after context", "evidence": {}})
    if r8: p += 1

    mfiles = [m.get("file", "") for m in matches]
    r9 = all(f in ["chapter1.txt", "chapter2.txt"] for f in mfiles) and len(matches) == 4
    results.append({"rubric_id": "R9", "passed": r9, "score": 1 if r9 else 0, "reason": "OK" if r9 else "bad matches", "evidence": {"files": mfiles}})
    if r9: p += 1

    r10 = len(matches) == 4
    results.append({"rubric_id": "R10", "passed": r10, "score": 1 if r10 else 0, "reason": f"total={len(matches)}" if r10 else f"expected 4", "evidence": {"total": len(matches)}})
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
