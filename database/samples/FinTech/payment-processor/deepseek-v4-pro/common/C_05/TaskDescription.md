# Task C_05: Refund Processing Pipeline

## Outcome

### Description
The refund_requests.csv has been processed. A result.json output contains: total refund requests count, total refund amount requested, total refund amount approved (only for customer_request and duplicate_charge reasons), total refund amount rejected (product_defective and wrong_amount reasons), per-reason breakdowns, a list of processed refunds with their approved/rejected status, and the net impact (total requested - total approved).

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | result.json exists and is valid JSON | high |
| R2 | total_requests equals 6 | high |
| R3 | total_requested_amount equals 4964.48 (sum of all amounts) | high |
| R4 | total_approved_amount equals 2918.49 (REF001 150 + REF002 2300 + REF004 678.50) = 3128.50 (customer_request + duplicate_charge reasons) | high |
| R5 | total_rejected_amount equals 1245.99 (REF003 45.99 + REF005 1200) | high |
| R6 | per_reason_breakdown contains keys customer_request, duplicate_charge, product_defective, wrong_amount with correct counts | medium |
| R7 | processed list has 6 entries each with refund_id, status (approved/rejected), amount, reason | medium |
| R8 | REF001 status is approved, REF003 status is rejected, REF005 status is rejected | medium |
| R9 | net_impact is computed as total_approved_amount - total_requested_amount (negative value) | medium |
| R10 | No string-type numeric values for any amount field | low |

## Output Contract

- Format: JSON
- Primary result path: result.json
- Required artifacts: result.json
- Scored fields: total_requests, total_requested_amount, total_approved_amount, total_rejected_amount, per_reason_breakdown, processed, net_impact
- Parse rules:
  - amount fields are float; tolerance 0.01
  - processed is array of objects with refund_id, status, amount, reason
  - per_reason_breakdown is object with reason keys mapping to {count, amount}

## Environment And Dependencies

- Platforms: macos, linux, windows
- Requires: python3
- Network: none

## WorkSpace Inputs

- refund_requests.csv: 6 refund requests with columns refund_id, transaction_id, amount, reason, status

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
