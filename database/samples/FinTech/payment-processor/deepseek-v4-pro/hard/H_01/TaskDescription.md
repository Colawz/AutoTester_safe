# Task H_01: Multi-Currency Settlement Analysis

## Outcome

### Description
The multi-currency transactions.csv has been processed using exchange_rates.csv for currency conversion. All 10 transactions have been converted to a USD equivalent using the provided exchange rates. The result.json contains: per-transaction breakdown with original and USD-converted values, total USD equivalent by merchant, total USD equivalent by currency, the overall settlement total in USD, the average USD equivalent, and a cross-rate validation check that each transaction's converted amount rounds to 2 decimal places.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | result.json exists and is valid JSON | high |
| R2 | transactions array has 10 entries, one per transaction | high |
| R3 | Each transaction entry has original_amount, original_currency, usd_equivalent, exchange_rate_used fields | high |
| R4 | H001 (5000 USD) has usd_equivalent = 5000.00 (rate 1.0) | high |
| R5 | H002 (3500 EUR) usd_equivalent computed using EUR→USD rate (1.09): 3500 * 1.09 = 3815.00 | high |
| R6 | H003 (100000 JPY) usd_equivalent computed using JPY→USD rate (0.0066): 100000 * 0.0066 = 660.00 | high |
| R7 | by_merchant has GlobalMerchant and EuroShop with correct aggregated USD totals | medium |
| R8 | by_currency has entries for USD, EUR, JPY, GBP, CHF with correct aggregated USD totals | medium |
| R9 | overall.total_usd, overall.count=10, overall.average_usd are correct | medium |
| R10 | All usd_equivalent values are rounded to 2 decimal places | low |

## Output Contract

- Format: JSON
- Primary result path: result.json
- Required artifacts: result.json
- Scored fields: transactions, by_merchant, by_currency, overall
- Parse rules:
  - transactions is array of objects with txn_id, original_amount, original_currency, usd_equivalent, exchange_rate_used
  - by_merchant maps merchant name to {count, total_usd}
  - by_currency maps currency code to {count, total_original, total_usd}
  - overall contains count, total_usd, average_usd
  - Numeric tolerance: 0.01 for all USD amounts

## Environment And Dependencies

- Platforms: macos, linux, windows
- Requires: python3
- Network: none

## WorkSpace Inputs

- transactions.csv: 10 multi-currency transactions with columns txn_id, date, amount, currency, merchant, card_type
- exchange_rates.csv: 20 exchange rate pairs with columns base_currency, target_currency, rate

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
- must_pass: [R1, R2, R4, R5, R6]
