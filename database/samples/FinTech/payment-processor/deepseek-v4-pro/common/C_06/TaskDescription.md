# Task C_06: Payment Summary Dashboard Data

## Outcome

### Description
The transactions.json file has been processed. A result.json has been produced containing daily summaries (grouped by date), merchant summaries (grouped by merchant), currency summaries (only USD), card type summaries, total counts by status (completed/pending/failed), and the overall total amount and count. Each summary group includes count, total_amount, and average_amount.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | result.json exists and is valid JSON | high |
| R2 | overall.total_count equals 12 | high |
| R3 | overall.total_amount equals 19889.98 (sum of all 12 transaction amounts) | high |
| R4 | by_date contains entries for each date: 2026-04-01, 2026-04-02, 2026-04-03, 2026-04-04 with correct daily totals | high |
| R5 | by_merchant contains MerchantA, MerchantB, MerchantC with correct aggregated amounts | high |
| R6 | by_card_type contains Visa, Mastercard, Amex with correct per-type counts and totals | medium |
| R7 | by_status contains completed (count=8), pending (count=2), failed (count=1) | medium |
| R8 | Each group entry has count, total_amount, average_amount fields | medium |
| R9 | All average_amount values are correctly computed as total_amount / count per group (rounded to 2 decimals) | medium |
| R10 | status totals exclude any unexpected status values (only completed, pending, failed) | low |

## Output Contract

- Format: JSON
- Primary result path: result.json
- Required artifacts: result.json
- Scored fields: overall, by_date, by_merchant, by_card_type, by_status
- Parse rules:
  - overall contains count, total_amount, average_amount
  - by_date, by_merchant, by_card_type are objects with group keys mapping to {count, total_amount, average_amount}
  - by_status is object with status keys mapping to count
  - Numeric tolerance: 0.01; average_amount rounded to 2 decimals

## Environment And Dependencies

- Platforms: macos, linux, windows
- Requires: python3
- Network: none

## WorkSpace Inputs

- transactions.json: 12 payment transaction records with fields txn_id, date, amount, currency, merchant, card_type, status

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
- must_pass: [R1, R2, R3, R4, R5]
