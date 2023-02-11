from models.base_model import BaseModel, db
from peewee import CharField, IntegerField, BooleanField, ForeignKeyField, DecimalField, BigIntegerField

from models.bitcoin.address_utxo_status import BitcoinAddressUtxoStatus



class BitcoinAddressUtxo(BaseModel):
    transaction_id = CharField()
    v_out = IntegerField()
    status = ForeignKeyField(BitcoinAddressUtxoStatus, to_field='id')
    value = IntegerField()

    class Meta:
        database = db
        table_name = "bitcoin_address_utxo"

    def to_string(self):
        ...
