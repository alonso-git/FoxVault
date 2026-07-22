from decimal import Decimal, InvalidOperation
import re

def get_transaction_amount(raw: str) -> Decimal:
    """
    Matches money formats:  
    $1    $10    $100.    $100.1    $100.10  
    $ symbol, one or more integers, dot or not, zero to two decimals  
    $ 1    $.10    100.10  
    Will fail    
    """
    money = r'\$(\d+\.?\d{0,2})'

    amount_str = re.search(money, raw)

    if not amount_str:
        raise ValueError(f"No money format found in the text: {raw}")
    
    try:
        return Decimal(amount_str.group(1))
    except InvalidOperation as e:
        raise InvalidOperation(f"Could not convert '{amount_str.group(1)}' to Decimal") from e  