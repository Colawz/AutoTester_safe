## Outcome

### Description
The agent uses a full-text file search skill to perform a multi-criteria search across a corpus of 10 documents. The task requires finding all files that mention BOTH "cloud" AND "security" in the same file. From the matching files, the agent must rank them by the number of times "security" appears (higher count = higher rank). Results must include the ranked order, per-file keyword frequency, and total matches.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | Primary result artifact `result.json` exists under the task's `results/` directory | high |
| R2 | `result.json` is valid JSON with top-level `query`, `ranked_results` array, and `total_criteria_matched_files` | high |
| R3 | `query` contains `{"keywords": ["cloud", "security"], "mode": "AND", "rank_by": "security_count"}` | high |
| R4 | Files matching both "cloud" AND "security": doc_003_security.txt, doc_004_security.txt, doc_007_security.txt, doc_008_cloud.txt, doc_010_security.txt (5 files) | high |
| R5 | `total_criteria_matched_files` equals 5 | high |
| R6 | Each `ranked_results` entry has `file`, `cloud_count`, `security_count`, and `lines` fields | high |
| R7 | Entries are ranked descending by `security_count`; doc_007_security.txt (security_count=4) should be first or tied | high |
| R8 | `doc_001_cloud.txt`, `doc_002_cloud.txt`, `doc_005_kubernetes.txt`, `doc_006_kubernetes.txt`, `doc_009_database.txt` are NOT in results (missing at least one keyword) | high |
| R9 | The result does not contain placeholder/aggregate entries or fabricated files | medium |
| R10 | Each `lines` entry correctly lists matching lines containing "cloud" or "security" | high |

## Output Contract

- **Format**: JSON
- **Primary result path**: `result.json`
- **Required artifacts**: `result.json`
- **Scored fields**: `query`, `ranked_results[].file`, `ranked_results[].cloud_count`, `ranked_results[].security_count`, `ranked_results[].lines`, `total_criteria_matched_files`
- **Parse rules**:
  - `ranked_results` is an ordered array (descending by security_count)
  - `cloud_count` and `security_count` are integers counting word occurrences per file
  - Case-insensitive matching for both keywords
  - Files with equal `security_count` may be in any relative order
  - No numeric tolerance

## Environment And Dependencies

- **Platforms**: macos, linux
- **Requires**: python3, json parsing available
- **Network**: none required

## WorkSpace Inputs

- `doc_001_cloud.txt`
- `doc_002_cloud.txt`
- `doc_003_security.txt`
- `doc_004_security.txt`
- `doc_005_kubernetes.txt`
- `doc_006_kubernetes.txt`
- `doc_007_security.txt`
- `doc_008_cloud.txt`
- `doc_009_database.txt`
- `doc_010_security.txt`

## Grader Contract

- **Mode**: code
- **Entry**: `Grader/run.py`
- **Result path**: `grading_result.json`
- **Pass threshold**: 8
- **Partial threshold**: 5
- **Rubrics**: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10

## Unsupported And Blocked Conditions

- `unsupported` if the workspace is missing or empty
- `blocked` if filesystem read access is denied for the workspace directory

## Pass Policy

- **Minimum pass count**: 8
- **Must pass**: R1, R2, R3, R4, R5, R7
