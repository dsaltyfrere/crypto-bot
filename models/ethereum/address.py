from models.base_model import BaseModel, db
from peewee import CharField


class EthereumAddress(BaseModel):
    ethereum_address = CharField()
    ethereum_address_alias = CharField(null=True)

    class Meta:
        database = db
        table_name = "ethereum_address"

    def to_string(self):
        return f"Address: {self.ethereum_address}"
