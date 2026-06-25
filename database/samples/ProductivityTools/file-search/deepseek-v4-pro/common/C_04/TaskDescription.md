## Outcome

### Description
The agent uses a full-text file search skill to find all files containing "DEBUG_MODE" but MUST restrict the search to only `.py` and `.js` source code files, excluding `.json`, `.md`, and `.txt` files. The agent must demonstrate file-type filtering capability. Results are saved as a structured JSON file.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | Primary result artifact `result.json` exists under the task's `results/` directory | high |
| R2 | `result.json` is valid JSON and contains a top-level `matches` array | high |
| R3 | Each match entry has `file`, `file_extension`, `line_numbers`, and `lines` fields | high |
| R4 | `app.py` is included in matches (contains "DEBUG_MODE" and is `.py`) | high |
| R5 | `utils.js` is included in matches (contains "DEBUG_MODE" and is `.js`) | high |
| R6 | `config.json` is NOT included (not `.py` or `.js` even though it contains "debug") | high |
| R7 | `readme.md` and `notes.txt` are NOT included (wrong file types) | high |
| R8 | Each entry's `file_extension` field correctly reflects the file extension (`.py` or `.js`) | medium |
| R9 | The result does not fabricate files or include files not in the workspace | medium |
| R10 | The `matches` array length equals the number of matching `.py` and `.js` files (expected 2) | high |

## Output Contract

- **Format**: JSON
- **Primary result path**: `result.json`
- **Required artifacts**: `result.json`
- **Scored fields**: `matches[].file`, `matches[].file_extension`, `matches[].line_numbers`, `matches[].lines`
- **Parse rules**:
  - `matches` is an array of match objects
  - `file_extension` must be either `.py` or `.js`
  - `line_numbers` is an array of integers
  - `lines` is an array of match-line strings
  - Case-sensitive matching for "DEBUG_MODE"
  - No numeric tolerance

## Environment And Dependencies

- **Platforms**: macos, linux
- **Requires**: python3, json parsing available
- **Network**: none required

## WorkSpace Inputs

- `app.py`
- `config.json`
- `readme.md`
- `notes.txt`
- `utils.js`

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
- **Must pass**: R1, R2, R4, R5, R6
