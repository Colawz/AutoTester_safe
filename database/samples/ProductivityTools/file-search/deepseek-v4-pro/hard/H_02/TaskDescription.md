## Outcome

### Description
The agent uses a full-text file search skill to perform a cross-reference search across multiple business documents. The agent must find all files mentioning the name "Maria Rodriguez" and all files mentioning "Acme Corporation", then cross-reference to identify which files mention BOTH. The agent must also extract the context around each mention. Results must include a merged cross-reference report.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | Primary result artifact `result.json` exists under the task's `results/` directory | high |
| R2 | `result.json` is valid JSON with top-level `entities`, `cross_references`, and `summary` | high |
| R3 | `entities` is an array with objects for "Acme Corporation" and "Maria Rodriguez" each having `files` and `total_mentions` | high |
| R4 | `cross_references` identifies files mentioning BOTH entities: `company_report.txt` and `project_nexus.txt` | high |
| R5 | `company_report.txt` mentions "Acme Corporation" (line 1) and "Maria Rodriguez" (line 22) | high |
| R6 | `project_nexus.txt` mentions "Maria Rodriguez" (line 2) and "Acme Corporation" implicitly via context (the parent company context) | medium |
| R7 | `competitor_analysis.txt` and `market_trends.txt` mention neither entity | high |
| R8 | `summary` contains `total_entity_files`, `total_cross_reference_files`, and `entities_searched` | high |
| R9 | The result does not contain placeholder data or fabricated files | medium |
| R10 | `total_cross_reference_files` equals 2 (files mentioning both entities) | high |

## Output Contract

- **Format**: JSON
- **Primary result path**: `result.json`
- **Required artifacts**: `result.json`
- **Scored fields**: `entities[].name`, `entities[].files[].file`, `entities[].files[].line_numbers`, `entities[].total_mentions`, `cross_references`, `summary`
- **Parse rules**:
  - `cross_references` is an array of file names mentioning both entities
  - `total_mentions` is an integer count per entity
  - Case-insensitive matching for entity names
  - No numeric tolerance

## Environment And Dependencies

- **Platforms**: macos, linux
- **Requires**: python3, json parsing available
- **Network**: none required

## WorkSpace Inputs

- `company_report.txt`
- `competitor_analysis.txt`
- `market_trends.txt`
- `project_nexus.txt`

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
- **Must pass**: R1, R2, R3, R4, R5, R8
