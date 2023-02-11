from models.base_model import BaseModel, db
from peewee import CharField, IntegerField, BooleanField, ForeignKeyField, DecimalField, BigIntegerField

class BitcoinAddressUtxoStatus(BaseModel):
    confirmed = BooleanField()
    block_height = IntegerField()
    block_hash = CharField()
    block_time = IntegerField()

    class Meta:
        database = db
        table_name = "bitcoin_address_utxo_status"

    def to_string(self):
        ...