# Task H_03: Payment Gateway Integration Report

## Outcome

### Description
A research report has been produced comparing 5 major payment gateway APIs (Stripe, PayPal, Square, Adyen, Braintree). The result.json contains: a gateway_comparison array with entries for each gateway containing at least name, pricing (transaction_fee_percent, monthly_fee), supported_payment_methods (list), security_certifications (list), api_type (REST/graphQL/etc), and key_features (list); a summary section with the cheapest option for small business, most secure option, best for international, and best overall recommendation; and a recommended_gateways section listing top 3 picks for different use cases.

### Rubric

| ID | Criterion | Priority |
|----|-----------|----------|
| R1 | result.json exists and is valid JSON | high |
| R2 | gateway_comparison array has exactly 5 entries | high |
| R3 | Each gateway entry contains at least: name, pricing, supported_payment_methods, security_certifications, api_type, key_features | high |
| R4 | All 5 well-known gateway names present: Stripe, PayPal, Square, Adyen, Braintree | high |
| R5 | pricing object has transaction_fee_percent and monthly_fee fields | medium |
| R6 | Each gateway has at least 3 supported_payment_methods as an array of strings | medium |
| R7 | Each gateway has at least 2 security_certifications (e.g., "PCI DSS Level 1") | medium |
| R8 | summary section contains cheapest_option, most_secure, best_for_international, best_overall | medium |
| R9 | recommended_gateways is an object with at least 3 use-case keys (e.g., startup, enterprise, international) each mapping to a gateway name | medium |
| R10 | All entries are grounded in realistic pricing data (transaction_fee_percent between 1.5 and 4.0) | low |

## Output Contract

- Format: JSON
- Primary result path: result.json
- Required artifacts: result.json
- Scored fields: gateway_comparison, summary, recommended_gateways
- Parse rules:
  - gateway_comparison is array of objects
  - supported_payment_methods is array of strings
  - security_certifications is array of strings
  - pricing.transaction_fee_percent is float
  - No null values in required string fields

## Environment And Dependencies

- Platforms: macos, linux, windows
- Requires: python3
- Network: optional (information retrieval may benefit from web access)

## WorkSpace Inputs

- No seed files. The workspace starts empty.

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
