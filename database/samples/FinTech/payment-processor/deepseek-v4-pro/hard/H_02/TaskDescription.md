# Task H_02: Fraud Detection Rules Engine

## Outcome

### Description
A Python fraud detection script (fraud_detector.py) has been written that implements a rule-based fraud detection engine. The script reads transactions.json and outputs result.json with: a rules section listing applied rules, a flagged_transactions array containing transactions that triggered any rule, a summary with total_checked, total_flagged, total_amount_flagged, and per-rule breakdowns (rule name, triggered count, total amount). Rules include: amount threshold (>2000 USD), velocity check (more than 3 transactions on same day), high-risk country block, and card BIN prefix checks for known compromised ranges.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | fraud_detector.py exists and is executable | high |
| R2 | Running `python3 fraud_detector.py` produces result.json with valid JSON | high |
| R3 | result.json contains rules_applied list with at least 3 rule definitions | high |
| R4 | result.json contains flagged_transactions array | high |
| R5 | summary.total_checked >= 1 and summary.total_flagged >= 0 | high |
| R6 | Each flagged transaction includes fields: txn_id, amount, triggered_rules (list of rule names that fired) | medium |
| R7 | per_rule_breakdown is an object with at least 3 rule entries each containing triggered_count and total_amount_flagged | medium |
| R8 | The amount_threshold rule flags transactions over 2000 USD | medium |
| R9 | test_fraud_detector.py exists with at least 5 test functions testing individual rules | medium |
| R10 | Running `python3 -m pytest test_fraud_detector.py --tb=short -q` passes all tests | medium |

## Output Contract

- Format: JSON via result.json created by running fraud_detector.py
- Primary result path: result.json
- Required artifacts: result.json
- Scored fields: rules_applied, flagged_transactions, summary, per_rule_breakdown
- Parse rules:
  - flagged_transactions is array of objects with txn_id, amount, triggered_rules
  - triggered_rules is array of rule name strings
  - summary has total_checked (int), total_flagged (int), total_amount_flagged (float)

## Environment And Dependencies

- Platforms: macos, linux, windows
- Requires: python3, pytest
- Network: none

## WorkSpace Inputs

- No seed files. The workspace starts empty.

## Grader Contract

- Grader: Grader/run.py
- Grader manifest: Grader/grader_manifest.json
- Verifier mode: code
- Pass threshold: 8
- Partial threshold: 5

## Unsupported And Blocked Conditions

- pytest not available

## Pass Policy

- minimum_pass_count: 8
- must_pass: [R1, R2, R3, R4, R5]
