# Task C_04: Invoice Generation

## Outcome

### Description
A formatted invoice has been generated from the invoice_data.json workspace file. The invoice (result.json) contains the invoice number, merchant info, customer info, itemized line items with extended prices, subtotal, tax amount, total, payment info, and a formatted text representation (invoice_text). All calculations (extended price = quantity * unit_price, subtotal, tax = subtotal * tax_rate, total = subtotal + tax) are correct.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | result.json exists and is valid JSON | high |
| R2 | invoice_number equals "INV-2026-001" | high |
| R3 | merchant.name equals "GlobalShop Inc." | high |
| R4 | customer.name equals "Alice Johnson" | high |
| R5 | items array has 3 entries with correct descriptions | high |
| R6 | Each item has extended_price = quantity * unit_price (49.99*2=99.98, 129.99*1=129.99, 15.00*1=15.00) | high |
| R7 | subtotal equals 244.97 (99.98 + 129.99 + 15.00) | medium |
| R8 | tax equals 19.60 (244.97 * 0.08 = 19.5976 rounded to 19.60) | medium |
| R9 | total equals 264.57 (subtotal + tax) | medium |
| R10 | invoice_text is a non-empty string containing the invoice number and total amount | low |

## Output Contract

- Format: JSON
- Primary result path: result.json
- Required artifacts: result.json
- Scored fields: invoice_number, merchant, customer, items, subtotal, tax, total, invoice_text
- Parse rules:
  - Numeric fields are float; tolerance 0.01
  - items is array of objects each with description, quantity, unit_price, extended_price
  - invoice_text is a string representation of the invoice

## Environment And Dependencies

- Platforms: macos, linux, windows
- Requires: python3
- Network: none

## WorkSpace Inputs

- invoice_data.json: merchant info, customer info, line items, tax rate, payment info

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
- must_pass: [R1, R2, R5, R6, R7]
