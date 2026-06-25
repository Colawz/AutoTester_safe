# Task C_01: Payment Transaction Extraction

## Outcome

### Description
The payment transaction CSV has been fully parsed and analyzed. The result.json contains the total transaction count, total amount, total fees, net amount, per-card-type breakdowns (count, amount, fees), per-merchant breakdowns (count, amount, fees), the average transaction amount, and the highest-value transaction ID with its amount.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | result.json exists and is valid JSON with the required top-level keys | high |
| R2 | total_transaction_count equals 15 | high |
| R3 | total_amount is computed as the sum of all amount column values | high |
| R4 | total_fees is computed as the sum of all fee column values | high |
| R5 | net_amount equals total_amount minus total_fees | high |
| R6 | per_card_type contains exactly entries for Visa, Mastercard, and Amex with correct per-type counts and amounts | high |
| R7 | per_merchant contains entries for MERCH001, MERCH002, MERCH003 with correct per-merchant counts | medium |
| R8 | average_transaction_amount is correctly computed as total_amount / total_count rounded to 2 decimals | medium |
| R9 | highest_value_txn.id and highest_value_txn.amount correctly identify TXN013 with amount 9200.00 | medium |
| R10 | No extra fields beyond the required schema exist at the top level | low |

## Output Contract

- Format: JSON
- Primary result path: result.json
- Required artifacts: result.json
- Scored fields: total_transaction_count, total_amount, total_fees, net_amount, per_card_type, per_merchant, average_transaction_amount, highest_value_txn
- Parse rules:
  - Numeric fields must be float or integer, not strings
  - Arrays must be keyed by the group name (card type or merchant ID)
  - Numeric tolerance: 0.01 for float comparisons
  - No string trimming or case normalization on merchant/card type keys

## Environment And Dependencies

- Platforms: macos, linux, windows
- Requires: python3, pip
- Network: none

## WorkSpace Inputs

- transactions.csv: 15 payment transaction records with columns transaction_id, date, amount, currency, card_type, merchant_id, status, fee

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
