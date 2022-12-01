from models.base_model import BaseModel
from peewee import CharField

class WhalepoolTransactionSymbol(BaseModel):
    symbol = CharField()

    class Meta:
        table_name = "whalepool_transaction_symbol"

    def to_string(self):
        return f"{self.symbol}"