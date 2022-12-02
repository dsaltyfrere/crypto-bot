from models.base_model import BaseModel, db
from models.bitcoin.pool import BitcoinPool
from peewee import IntegerField, ForeignKeyField, BigIntegerField, DecimalField

class BitcoinPoolHashrate(BaseModel):
    timestamp = IntegerField()
    average_hashrate = BigIntegerField()
    share = DecimalField()
    pool_name = ForeignKeyField(BitcoinPool, to_field='pool_name')

    class Meta:
        table_name = "bitcoin_pool_hashrates"
        database = db

    def to_string(self):
        return f"Pool: {self.pool_name} - Hash rate: {self.average_hashrate} - Share: {self.share}"