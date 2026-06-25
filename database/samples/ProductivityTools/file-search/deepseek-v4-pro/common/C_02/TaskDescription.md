## Outcome

### Description
The agent uses a full-text file search skill to find all files in the workspace that contain both keywords "apple" AND "banana" simultaneously. The agent must correctly identify files containing both terms and exclude files containing only one of the keywords. Results are saved as a structured JSON file.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | Primary result artifact `result.json` exists under the task's `results/` directory | high |
| R2 | `result.json` is valid JSON and contains a top-level `matches` array | high |
| R3 | Each match entry has `file`, `matched_keywords`, `line_numbers`, and `lines` fields | high |
| R4 | `fruit_bowl_apple_banana.txt` is included in matches (contains both "apple" and "banana") | high |
| R5 | `fruits_apple.txt` is NOT included (only contains "apple", not "banana") | high |
| R6 | `tropical_banana.txt` is NOT included (only contains "banana", not "apple") | high |
| R7 | `citrus_orange.txt` and `berry_notes.txt` are NOT included (contain neither keyword) | medium |
| R8 | Each matched file's `matched_keywords` field lists both "apple" and "banana" | high |
| R9 | The result does not contain placeholder text, hardcoded entries, or fabricated files | medium |
| R10 | The `matches` array length equals the number of files containing both keywords (expected 1) | high |

## Output Contract

- **Format**: JSON
- **Primary result path**: `result.json`
- **Required artifacts**: `result.json`
- **Scored fields**: `matches[].file`, `matches[].matched_keywords`, `matches[].line_numbers`, `matches[].lines`
- **Parse rules**:
  - `matches` is an array of match objects
  - `file` is a string matching an actual workspace filename
  - `matched_keywords` is an array containing both "apple" and "banana"
  - `line_numbers` is an array of integers
  - `lines` is an array of matching line strings
  - Arrays are unordered for scoring purposes
  - Case-insensitive keyword matching is acceptable
  - No numeric tolerance

## Environment And Dependencies

- **Platforms**: macos, linux
- **Requires**: python3, json parsing available
- **Network**: none required

## WorkSpace Inputs

- `fruits_apple.txt`
- `tropical_banana.txt`
- `fruit_bowl_apple_banana.txt`
- `citrus_orange.txt`
- `berry_notes.txt`

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
- **Must pass**: R1, R2, R4, R5
