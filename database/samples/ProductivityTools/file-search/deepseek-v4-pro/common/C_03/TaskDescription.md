## Outcome

### Description
The agent uses a full-text file search skill to find all files containing the keyword "apple" but excluding any file that also contains "banana". The agent must apply set-difference logic (apple AND NOT banana). Results are saved as a structured JSON file.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | Primary result artifact `result.json` exists under the task's `results/` directory | high |
| R2 | `result.json` is valid JSON and contains a top-level `matches` array | high |
| R3 | Each match entry has `file`, `line_numbers`, and `lines` fields | high |
| R4 | `doc_alpha.txt` is included in matches (contains "apple" without "banana") | high |
| R5 | `doc_delta.txt` is included in matches (contains "apple" without "banana") | high |
| R6 | `doc_beta.txt` is NOT included (contains both "apple" and "banana") | high |
| R7 | `doc_gamma.txt` and `doc_epsilon.txt` are NOT included (do not contain "apple") | medium |
| R8 | Each matched entry correctly lists the line numbers and lines where "apple" appears | high |
| R9 | The result does not contain placeholder text, hardcoded entries, or fabricated content | medium |
| R10 | The `matches` array length equals the number of files matching the exclusion criteria (expected 2) | high |

## Output Contract

- **Format**: JSON
- **Primary result path**: `result.json`
- **Required artifacts**: `result.json`
- **Scored fields**: `matches[].file`, `matches[].line_numbers`, `matches[].lines`
- **Parse rules**:
  - `matches` is an array of match objects
  - `file` is a string matching an actual workspace filename
  - `line_numbers` is an array of integers (one-indexed)
  - `lines` is an array of matching line strings
  - Case-insensitive matching is acceptable
  - No numeric tolerance

## Environment And Dependencies

- **Platforms**: macos, linux
- **Requires**: python3, json parsing available
- **Network**: none required

## WorkSpace Inputs

- `doc_alpha.txt`
- `doc_beta.txt`
- `doc_gamma.txt`
- `doc_delta.txt`
- `doc_epsilon.txt`

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
- **Must pass**: R1, R2, R4, R6
