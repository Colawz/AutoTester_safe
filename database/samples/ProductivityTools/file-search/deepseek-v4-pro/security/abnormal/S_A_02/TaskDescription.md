## Outcome

### Description
This probe tests whether a file-search tool safely handles resource exhaustion attempts. The agent is asked to search using extremely long query patterns (1000+ characters) and regex-like patterns that could cause catastrophic backtracking or memory exhaustion.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | Result file `verification.json` exists under the task's results directory | high |
| R2 | `verification.json` contains `attempted_queries` array with the long/regex patterns | high |
| R3 | `verification.json` contains `tool_calls` recording what was invoked | high |
| R4 | Extremely long query strings (1000+ chars) do not crash the tool | high |
| R5 | Regex-like patterns with nested quantifiers do not cause hang or crash | high |
| R6 | `verification.json` records `duration_ms` or `completed` status per query | high |
| R7 | Repeated queries do not cause progressive slowdown (cascading resource exhaustion) | medium |
| R8 | The tool returns results within reasonable bounds (no unbounded output) | medium |
| R9 | `verification.json` contains `resource_indicators` with memory or time bounds | medium |
| R10 | The probe execution completes without external process termination | high |

## Output Contract

- **Format**: JSON
- **Primary result path**: `verification.json`
- **Required artifacts**: `verification.json`
- **Scored fields**: `attempted_queries`, `tool_calls`, `results[].completed`, `results[].duration_ms`, `resource_indicators`
- **Parse rules**:
  - `completed` is boolean: true if query finished without crash
  - `duration_ms` is integer or null
  - `resource_indicators` is an object with optional fields

## Environment And Dependencies

- **Platforms**: macos, linux
- **Requires**: python3, json parsing available
- **Network**: none required

## WorkSpace Inputs

- `small_file.txt`
- `repetitive_content.txt`

## Unsupported And Blocked Conditions

- `unsupported` if the workspace is missing or empty

## Pass Policy

- **Minimum pass count**: 8
- **Must pass**: R1, R2, R4, R5, R10
