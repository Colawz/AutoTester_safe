## Outcome

### Description
The agent uses a full-text file search skill to execute a complex boolean query across 7 animal-themed document files. The query logic is: find all files that contain ("mammals" OR "birds") AND "dogs" but NOT "prehistoric". The agent must correctly apply nested boolean logic (OR within AND with NOT exclusion). Results are saved as a structured JSON file.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | Primary result artifact `result.json` exists under the task's `results/` directory | high |
| R2 | `result.json` is valid JSON with top-level `query`, `files_matching`, and `matches` | high |
| R3 | `query` contains `{"include_any": ["mammals", "birds"], "require_all": ["dogs"], "exclude": ["prehistoric"]}` | high |
| R4 | `animal_mammals.txt` is included (contains "mammals" and "Dogs") | high |
| R5 | `animal_domestic.txt` is included (contains "Dogs" and appears in animals context; "mammals" or "birds" not needed since "dogs" is the require_all) | medium |
| R6 | `animal_prehistoric.txt` is NOT included (contains "dogs" but also "prehistoric" and relates to prehistoric context) | high |
| R7 | `animal_birds.txt`, `animal_reptiles.txt`, `animal_aquatic.txt`, `animal_wildlife.txt` are evaluated correctly according to the boolean logic | high |
| R8 | Each `matches` entry has `file`, `matched_terms`, and `lines` fields | high |
| R9 | The result does not contain placeholder, hardcoded, or fabricated results | medium |
| R10 | The `file_count` equals the number of files satisfying the full boolean query | high |

## Output Contract

- **Format**: JSON
- **Primary result path**: `result.json`
- **Required artifacts**: `result.json`
- **Scored fields**: `query`, `file_count`, `files_matching`, `matches[].file`, `matches[].matched_terms`, `matches[].lines`
- **Parse rules**:
  - `query` must reflect the boolean logic described
  - `files_matching` is an array of file names satisfying the full boolean expression
  - `matched_terms` is an array identifying which query terms matched in that file
  - Case-insensitive matching
  - No numeric tolerance

## Environment And Dependencies

- **Platforms**: macos, linux
- **Requires**: python3, json parsing available
- **Network**: none required

## WorkSpace Inputs

- `animal_mammals.txt`
- `animal_birds.txt`
- `animal_reptiles.txt`
- `animal_aquatic.txt`
- `animal_domestic.txt`
- `animal_wildlife.txt`
- `animal_prehistoric.txt`

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
- **Must pass**: R1, R2, R3, R4, R6
