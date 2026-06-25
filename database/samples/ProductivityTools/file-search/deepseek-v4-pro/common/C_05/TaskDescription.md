## Outcome

### Description
The agent uses a full-text file search skill to find all occurrences of the keyword "machine learning" (case-insensitive) across all text files in the workspace and compute the total occurrence count and per-file counts. The agent must produce a structured JSON summary with file-level breakdown and an aggregate total.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | Primary result artifact `result.json` exists under the task's `results/` directory | high |
| R2 | `result.json` is valid JSON and contains top-level `total_occurrences`, `files`, and `search_term` keys | high |
| R3 | `search_term` is `"machine learning"` | high |
| R4 | `files` is an array of objects each with `file`, `occurrence_count`, and `lines` fields | high |
| R5 | `paper1.txt` occurrence count is 3 (lines 1, 3, 6 use lowercase "machine learning"; line 5 uses "Machine learning") | high |
| R6 | `paper2.txt` occurrence count is 2 (lines 2 and 4) and `paper3.txt` occurrence count is 3 (lines 1, 2, 4) | high |
| R7 | `paper4.txt` is either absent from files or has occurrence_count 0 (does not contain "machine learning") | medium |
| R8 | `total_occurrences` equals the sum of all per-file occurrence counts | high |
| R9 | The result does not contain placeholder counts (e.g. all zeros, all same number, or fabricated data) | medium |
| R10 | Each line in `lines` contains the phrase "machine learning" (case-insensitive) | high |

## Output Contract

- **Format**: JSON
- **Primary result path**: `result.json`
- **Required artifacts**: `result.json`
- **Scored fields**: `total_occurrences`, `files[].file`, `files[].occurrence_count`, `files[].lines`, `search_term`
- **Parse rules**:
  - `total_occurrences` is an integer, the sum of all per-file counts
  - `occurrence_count` is an integer counting occurrences per file
  - Case-insensitive matching for "machine learning"
  - Lines that contain "Machine learning" (capitalized) must also be counted
  - No numeric tolerance
  - The `files` array is unordered

## Environment And Dependencies

- **Platforms**: macos, linux
- **Requires**: python3, json parsing available
- **Network**: none required

## WorkSpace Inputs

- `paper1.txt`
- `paper2.txt`
- `paper3.txt`
- `paper4.txt`

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
- **Must pass**: R1, R2, R3, R5, R8
