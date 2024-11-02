from src.abstract_models.abstract_process import AbstractProcess
from src.models.warehouse_turnover_model import WarehouseTurnoverModel
from src.models.transaction_type import TransactionType

class WarehouseTurnoverProcess(AbstractProcess):
    def process(self, transactions: list) -> list:
        turnovers = {}
        for transaction in transactions:
            key = (transaction.warehouse.unique_code, transaction.nomenclature.unique_code, transaction.measurement.unique_code)

            if key not in turnovers:
                turnovers[key] = WarehouseTurnoverModel()
                turnovers[key].turnover = 0
                turnovers[key].warehouse = transaction.warehouse
                turnovers[key].nomenclature = transaction.nomenclature
                turnovers[key].measurement = transaction.measurement

            if transaction.type == TransactionType.RECEIPT:
                turnovers[key].turnover += transaction.count
            else:
                turnovers[key].turnover -= transaction.count

        return list(turnovers.values())