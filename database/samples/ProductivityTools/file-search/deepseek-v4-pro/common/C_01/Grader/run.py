import json
import sys
import os

TASK_ID = "C_01"
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")
RESULT_PATH = os.path.join(RESULTS_DIR, "result.json")
GRADING_RESULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grading_result.json")

EXPECTED_KEYWORD = "Erlang"
EXPECTED_FILE = "project_overview.txt"
WORKSPACE_FILES = [
    "project_overview.txt",
    "architecture_notes.md",
    "deployment_guide.txt",
    "security_policy.md",
    "roadmap.txt"
]

def grade():
    if not os.path.exists(RESULT_PATH):
        return {
            "task_id": TASK_ID,
            "status": "fail",
            "outcome_status": "failed",
            "passed": 0,
            "total": 10,
            "must_pass_satisfied": False,
            "results": [
                {"rubric_id": "R1", "passed": False, "score": 0, "reason": "result.json not found", "evidence": {"path": RESULT_PATH}}
            ]
        }

    with open(RESULT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            return {
                "task_id": TASK_ID,
                "status": "fail",
                "outcome_status": "failed",
                "passed": 0,
                "total": 10,
                "must_pass_satisfied": False,
                "results": [
                    {"rubric_id": "R2", "passed": False, "score": 0, "reason": f"Invalid JSON: {e}", "evidence": {}}
                ]
            }

    results = []
    passed_count = 0
    must_pass = {"R1": False, "R2": False, "R4": False}
    must_pass_satisfied = True

    matches = data.get("matches", [])
    match_files = [m.get("file", "") for m in matches]

    # R1: result.json exists
    r1_pass = os.path.exists(RESULT_PATH)
    results.append({"rubric_id": "R1", "passed": r1_pass, "score": 1 if r1_pass else 0, "reason": "Exists" if r1_pass else "result.json not found", "evidence": {"path": RESULT_PATH}})
    if r1_pass: passed_count += 1
    if "R1" in must_pass: must_pass["R1"] = r1_pass

    # R2: valid JSON with matches array
    r2_pass = "matches" in data and isinstance(matches, list)
    results.append({"rubric_id": "R2", "passed": r2_pass, "score": 1 if r2_pass else 0, "reason": "Valid format" if r2_pass else "Missing matches array", "evidence": {"has_matches": "matches" in data, "is_list": isinstance(matches, list)}})
    if r2_pass: passed_count += 1
    if "R2" in must_pass: must_pass["R2"] = r2_pass

    # R3: each match has required fields
    r3_pass = all(isinstance(m, dict) and "file" in m and "line_numbers" in m and "lines" in m for m in matches) if matches else False
    results.append({"rubric_id": "R3", "passed": r3_pass, "score": 1 if r3_pass else 0, "reason": "All fields present" if r3_pass else "Missing required fields", "evidence": {"match_count": len(matches)}})
    if r3_pass: passed_count += 1

    # R4: project_overview.txt is included
    r4_pass = EXPECTED_FILE in match_files
    results.append({"rubric_id": "R4", "passed": r4_pass, "score": 1 if r4_pass else 0, "reason": "Found" if r4_pass else "project_overview.txt not in matches", "evidence": {"matched_files": match_files}})
    if r4_pass: passed_count += 1
    if "R4" in must_pass: must_pass["R4"] = r4_pass

    # R5: at least one other file besides project_overview.txt
    other_files = [f for f in match_files if f != EXPECTED_FILE]
    r5_pass = len(other_files) >= 1
    results.append({"rubric_id": "R5", "passed": r5_pass, "score": 1 if r5_pass else 0, "reason": f"{len(other_files)} other files" if r5_pass else "No other files matched", "evidence": {"other_files": other_files}})
    if r5_pass: passed_count += 1

    # R6: no file without "Erlang" in matches
    r6_pass = all(f in WORKSPACE_FILES for f in match_files)
    results.append({"rubric_id": "R6", "passed": r6_pass, "score": 1 if r6_pass else 0, "reason": "All valid" if r6_pass else "Unknown files in matches", "evidence": {"matched_files": match_files, "workspace_files": WORKSPACE_FILES}})
    if r6_pass: passed_count += 1

    # R7: line_numbers is array of ints
    r7_pass = all(isinstance(m.get("line_numbers"), list) and all(isinstance(ln, int) for ln in m["line_numbers"]) for m in matches) if matches else False
    results.append({"rubric_id": "R7", "passed": r7_pass, "score": 1 if r7_pass else 0, "reason": "Valid line numbers" if r7_pass else "Invalid line_numbers format", "evidence": {}})
    if r7_pass: passed_count += 1

    # R8: lines contain matching content
    r8_pass = all(isinstance(m.get("lines"), list) and len(m["lines"]) > 0 for m in matches) if matches else False
    results.append({"rubric_id": "R8", "passed": r8_pass, "score": 1 if r8_pass else 0, "reason": "Lines present" if r8_pass else "Missing line content", "evidence": {}})
    if r8_pass: passed_count += 1

    # R9: no placeholder/template content
    r9_pass = len(matches) > 0 and all(f in WORKSPACE_FILES for f in match_files)
    results.append({"rubric_id": "R9", "passed": r9_pass, "score": 1 if r9_pass else 0, "reason": "Valid content" if r9_pass else "Suspicious entries", "evidence": {"file_count": len(match_files)}})
    if r9_pass: passed_count += 1

    # R10: non-empty matches
    r10_pass = len(matches) > 0
    results.append({"rubric_id": "R10", "passed": r10_pass, "score": 1 if r10_pass else 0, "reason": f"{len(matches)} matches" if r10_pass else "Empty matches", "evidence": {"match_count": len(matches)}})
    if r10_pass: passed_count += 1

    all_must_pass = all(must_pass.values())
    if passed_count >= 8 and all_must_pass:
        status = "pass"
        outcome = "satisfied"
    elif passed_count >= 5:
        status = "partial"
        outcome = "needs_revision"
    else:
        status = "fail"
        outcome = "failed"

    grading_result = {
        "task_id": TASK_ID,
        "status": status,
        "outcome_status": outcome,
        "passed": passed_count,
        "total": 10,
        "must_pass_satisfied": all_must_pass,
        "results": results
    }

    os.makedirs(os.path.dirname(GRADING_RESULT_PATH), exist_ok=True)
    with open(GRADING_RESULT_PATH, "w") as f:
        json.dump(grading_result, f, indent=2)

    return grading_result

if __name__ == "__main__":
    result = grade()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "pass" else 1)
