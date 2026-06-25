## Outcome

### Description
The agent uses a full-text file search skill to find all files in the workspace that contain the exact keyword "Erlang". For each matching file, the agent records the filename, the line numbers where matches occur, and the matching line content. Results are saved as a structured JSON file.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | Primary result artifact `result.json` exists under the task's `results/` directory | high |
| R2 | `result.json` is valid JSON and contains a top-level `matches` array | high |
| R3 | Each match entry has `file`, `line_numbers`, and `lines` fields | high |
| R4 | `project_overview.txt` is included in matches because it contains "Erlang" on line 2 | high |
| R5 | At least one other file besides `project_overview.txt` is correctly matched | medium |
| R6 | No file that does NOT contain "Erlang" is included in matches | high |
| R7 | Each file entry's `line_numbers` field is an array of integers identifying the correct match lines | high |
| R8 | Each file entry's `lines` field contains the exact matching line text for each matched line | high |
| R9 | The result does not contain placeholder text, hardcoded templates, or fabricated entries for files not in the workspace | medium |
| R10 | The `result.json` file is parseable and contains non-empty `matches` | high |

## Output Contract

- **Format**: JSON
- **Primary result path**: `result.json`
- **Required artifacts**: `result.json`
- **Scored fields**: `matches[].file`, `matches[].line_numbers`, `matches[].lines`
- **Parse rules**:
  - `matches` is an ordered array (order does not affect scoring)
  - `file` is a string, must match an actual workspace filename
  - `line_numbers` is an array of integers, one-indexed
  - `lines` is an array of strings, each the exact matching line
  - Arrays are unordered for matching purposes
  - No numeric tolerance; exact match required for check
  - Case sensitivity follows exact match rules (keyword "Erlang")

## Environment And Dependencies

- **Platforms**: macos, linux
- **Requires**: python3, json parsing available
- **Network**: none required

## WorkSpace Inputs

- `project_overview.txt`
- `architecture_notes.md`
- `deployment_guide.txt`
- `security_policy.md`
- `roadmap.txt`

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
- **Must pass**: R1, R2, R4
