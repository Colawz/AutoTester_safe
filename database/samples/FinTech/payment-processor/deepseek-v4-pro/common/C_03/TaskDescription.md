# Task C_03: Payment Method Validation

## Outcome

### Description
A Python validation script has been written that implements the Luhn algorithm for credit card number validation. The script (validate_card.py) accepts a card number as a command-line argument and outputs a JSON object with: the card number (masked as ****-****-****-{last4}), brand detection (Visa, Mastercard, Amex, or Unknown), a valid boolean, the checksum digit, and any validation error. The script must also include at least 5 test cases in a separate test file test_validate.py.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | validate_card.py exists in WorkSpace and is executable Python | high |
| R2 | Running `python3 validate_card.py 4111111111111111` outputs valid JSON with valid=true for this Visa test number | high |
| R3 | Running `python3 validate_card.py 5500000000000004` outputs valid=true for this Mastercard test number | high |
| R4 | Running `python3 validate_card.py 340000000000009` outputs valid=true with brand=Amex | high |
| R5 | Running `python3 validate_card.py 1234567890123456` outputs valid=false | high |
| R6 | The output JSON contains keys: card_number, brand, valid, checksum, error | medium |
| R7 | card_number is masked as ****-****-****-{last4} format | medium |
| R8 | brand detection: 4111111111111111 → Visa, 5500000000000004 → Mastercard, 340000000000009 → Amex, 1234567890123456 → Unknown | medium |
| R9 | test_validate.py exists with at least 5 test functions named test_* | medium |
| R10 | Running `python3 -m pytest test_validate.py --tb=short -q` passes all tests | medium |

## Output Contract

- Format: Command stdout JSON from validate_card.py
- Primary result path: result.json (containing CLI execution results)
- Required artifacts: result.json
- Scored fields: valid, brand, card_number, checksum, error
- Parse rules:
  - valid is boolean
  - brand is string
  - card_number is string in masked format
  - checksum is integer
  - Numeric tolerance: exact

## Environment And Dependencies

- Platforms: macos, linux, windows
- Requires: python3, pytest
- Network: none

## WorkSpace Inputs

- No seed files. Workspace starts empty.

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
