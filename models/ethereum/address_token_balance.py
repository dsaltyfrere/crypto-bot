from models.base_model import BaseModel, db
from peewee import CharField, ForeignKeyField, IntegerField

from models.ethereum.address import EthereumAddress


class EthereumAddressTokenBalance(BaseModel):
    ethereum_address = ForeignKeyField(EthereumAddress, to_field='ethereum_address')
    ethereum_token_address = CharField(null=True)
    ethereum_token_name = CharField(null=True)
    ethereum_token_symbol = CharField(null=True)
    ethereum_token_logo = CharField(null=True)
    ethereum_token_thumbnail = CharField(null=True)
    ethereum_token_decimals = IntegerField(null=True)
    ethereum_token_balance = CharField(null=True)

    class Meta:
        database = db
        table_name = "ethereum_address_token_balance"

    def to_string(self):
        if self.ethereum_token_balance is not None and self.ethereum_token_decimals is not None:
            balance = float(self.ethereum_token_balance) / self.ethereum_token_decimals
        else:
            balance = 0
        return f"Address: {self.ethereum_address} | Token address: {self.ethereum_token_address} | Token name: {self.ethereum_token_name} | Token symbol: {self.ethereum_token_symbol} | Token balance: {balance}"
