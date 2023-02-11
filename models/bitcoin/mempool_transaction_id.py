from models.base_model import BaseModel, db
from peewee import CharField

class MempoolTransactionId(BaseModel):
    mempool_transaction_id = CharField()

    class Meta:
        database = db
        table_name = "mempool_transaction_id"