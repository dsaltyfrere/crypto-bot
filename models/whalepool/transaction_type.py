from models.base_model import BaseModel
from peewee import CharField

class WhalepoolTransactionType(BaseModel):
    transaction_type = CharField()

    class meta:
        table_name = "whalepool_transaction_type"

    def to_string(self):
        return f"{self.transaction_type}"