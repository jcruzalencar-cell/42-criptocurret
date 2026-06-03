"""Utility functions for blockchain operations.

This module provides helper functions for validation, formatting,
and common blockchain operations.
"""

import re
from typing import Dict, Any, Optional


def is_valid_address(address: str) -> bool:
    """Validate blockchain address format.
    
    Addresses should be non-empty alphanumeric strings.
    
    Args:
        address: Address string to validate.
    
    Returns:
        bool: True if address format is valid.
    """
    if not isinstance(address, str) or not address:
        return False
    return re.match(r"^[a-zA-Z0-9_-]+$", address) is not None


def is_valid_transaction(transaction: Dict[str, Any]) -> bool:
    """Validate transaction data structure.
    
    Transaction must contain required fields with appropriate types.
    
    Args:
        transaction: Transaction dictionary to validate.
    
    Returns:
        bool: True if transaction format is valid.
    """
    required_fields = ["sender", "recipient", "amount"]
    
    if not isinstance(transaction, dict):
        return False
    
    if not all(field in transaction for field in required_fields):
        return False
    
    sender = transaction.get("sender")
    recipient = transaction.get("recipient")
    amount = transaction.get("amount")
    
    # Validate address fields
    if not (is_valid_address(sender) and is_valid_address(recipient)):
        return False
    
    # Validate amount is positive number
    if not isinstance(amount, (int, float)) or amount <= 0:
        return False
    
    return True


def format_balance(amount: float) -> str:
    """Format balance for display.
    
    Args:
        amount: Balance amount.
    
    Returns:
        str: Formatted balance string with 2 decimal places.
    """
    return f"{amount:.2f}"


def validate_difficulty(difficulty: int) -> bool:
    """Validate proof-of-work difficulty setting.
    
    Difficulty must be between 1 and 10.
    
    Args:
        difficulty: Difficulty level to validate.
    
    Returns:
        bool: True if difficulty is valid.
    """
    return isinstance(difficulty, int) and 1 <= difficulty <= 10
