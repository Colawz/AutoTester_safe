## Outcome

### Description
The agent uses a full-text file search skill to find all occurrences of the keyword "sundial" across all text files in the workspace. For each match, the agent must return the matching line AND one line of surrounding context (the line before and the line after). The agent must produce a structured JSON result with contextual snippets.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | Primary result artifact `result.json` exists under the task's `results/` directory | high |
| R2 | `result.json` is valid JSON and contains top-level `matches` array | high |
| R3 | Each match entry has `file`, `line_number`, `matched_line`, and `context` fields | high |
| R4 | `context` is an object with `before` (preceding line or null) and `after` (following line or null) | high |
| R5 | `chapter1.txt` contains 2 matches for "sundial" at lines 4 and 8 | high |
| R6 | `chapter2.txt` contains 2 matches for "sundial" at lines 6 and 7 | high |
| R7 | The `before` context for the first match in `chapter1.txt` (line 4) correctly shows line 3 | medium |
| R8 | The `after` context for the last match correctly shows the following line or null if at end | high |
| R9 | The result does not contain placeholder text, hardcoded snippets, or fabricated matches | medium |
| R10 | Total matches across all files equals 4 | high |

## Output Contract

- **Format**: JSON
- **Primary result path**: `result.json`
- **Required artifacts**: `result.json`
- **Scored fields**: `matches[].file`, `matches[].line_number`, `matches[].matched_line`, `matches[].context.before`, `matches[].context.after`
- **Parse rules**:
  - `matches` is an array of match objects
  - `line_number` is an integer (one-indexed)
  - `context.before` is a string or null if no preceding line
  - `context.after` is a string or null if no following line
  - Case-sensitive matching for "sundial"
  - No numeric tolerance

## Environment And Dependencies

- **Platforms**: macos, linux
- **Requires**: python3, json parsing available
- **Network**: none required

## WorkSpace Inputs

- `chapter1.txt`
- `chapter2.txt`

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
- **Must pass**: R1, R2, R3, R4, R5
