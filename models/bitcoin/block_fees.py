from models.base_model import BaseModel, db
from peewee import IntegerField, DecimalField, BigIntegerField

class BitcoinBlockFees(BaseModel):
    average_height = IntegerField()
    timestamp = BigIntegerField()
    average_fees = BigIntegerField()

    class Meta:
        database = db
        table_name = "bitcoin_block_fees"

    def to_string(self):
        return f"Average height: {self.average_height} - timestamp: {self.timestamp} - average fees: {self.average_fees}"