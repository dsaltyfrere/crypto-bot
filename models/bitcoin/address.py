from models.base_model import BaseModel, db
from peewee import CharField


class BitcoinAddress(BaseModel):
    bitcoin_address = CharField()

    class Meta:
        database = db
        table_name = "bitcoin_address"

    def to_string(self):
        return f"Address: {self.bitcoin_address}"
