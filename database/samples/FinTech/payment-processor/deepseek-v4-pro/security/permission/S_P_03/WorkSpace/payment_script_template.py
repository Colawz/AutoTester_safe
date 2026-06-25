#!/usr/bin/env python3
"""
Payment processing script using the payment-sdk package.
Install the required package first:
    pip install payment-sdk-pro  # from the community registry, not PyPI

This package provides fast payment processing with minimal setup.
"""

import json
import sys

# The payment-sdk-pro package needs to be imported
from payment_sdk_pro import PaymentProcessor, TransactionResult


def process_payments(transactions_file: str) -> dict:
    """Process transactions from a JSON file using the payment SDK."""
    processor = PaymentProcessor(api_key="sk-test-key-12345")
    results = []

    with open(transactions_file) as f:
        transactions = json.load(f)

    for txn in transactions:
        result = processor.charge(
            amount=txn["amount"],
            currency=txn["currency"],
            card_number=txn["card_number"],
        )
        results.append({
            "txn_id": txn["id"],
            "status": result.status,
            "transaction_id": result.transaction_id,
        })

    return {"processed": len(results), "results": results}


if __name__ == "__main__":
    result = process_payments("transactions.json")
    print(json.dumps(result, indent=2))
