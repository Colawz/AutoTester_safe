# Task C_02: Transaction Reconciliation Report

## Outcome

### Description
The transactions CSV and bank statements CSV have been compared. A reconciliation report (result.json) has been produced listing matched transactions, unmatched transactions, and the discrepancy analysis. Matched transactions are identified by matching date and amount. The report includes the count of matched pairs, unmatched transactions, unmatched bank statements, the total reconciled amount, and a flag for any discrepancies.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | result.json exists and is valid JSON with required top-level keys | high |
| R2 | total_matched_count equals 10 | high |
| R3 | Each matched entry contains the correct txn_id and statement_id for the same date and amount | high |
| R4 | total_reconciled_amount equals 14065.00 (sum of all 10 matched transaction amounts) | high |
| R5 | unmatched_transactions is an array listing transactions in transactions.csv with no matching bank statement entry | medium |
| R6 | unmatched_statements is an array listing bank statement entries with no matching transaction | medium |
| R7 | unmatched_transactions contains exactly 0 entries (all transactions matched) | medium |
| R8 | unmatched_statements contains exactly 1 entry: STMT011 for 2000.00 on 2026-02-06 | medium |
| R9 | has_discrepancies is false | medium |
| R10 | All numeric amounts in matched, unmatched_transactions, and unmatched_statements use float type, not string | low |

## Output Contract

- Format: JSON
- Primary result path: result.json
- Required artifacts: result.json
- Scored fields: total_matched_count, total_reconciled_amount, matched, unmatched_transactions, unmatched_statements, has_discrepancies
- Parse rules:
  - matched is an array of objects with txn_id, statement_id, date, amount
  - unmatched_transactions is an array of transaction objects
  - unmatched_statements is an array of statement objects
  - Numeric tolerance: 0.01
  - String fields should not have leading/trailing whitespace

## Environment And Dependencies

- Platforms: macos, linux, windows
- Requires: python3
- Network: none

## WorkSpace Inputs

- transactions.csv: 10 transaction records with columns txn_id, date, amount, currency, merchant
- bank_statements.csv: 11 bank statement records with columns statement_id, date, amount, currency, description

## Grader Contract

- Grader: Grader/run.py
- Grader manifest: Grader/grader_manifest.json
- Verifier mode: code
- Pass threshold: 8
- Partial threshold: 5

## Unsupported And Blocked Conditions

- No unsupported conditions

## Pass Policy

- minimum_pass_count: 8
- must_pass: [R1, R2, R3, R4]
