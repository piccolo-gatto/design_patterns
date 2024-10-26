from enum import Enum


class TransactionType(Enum):
    RECEIPT = "receipt"
    EXPENDITURE = "expenditure"