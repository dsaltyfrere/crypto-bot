from models.base_model import BaseModel
from peewee import CharField

class WhalepoolTransaction(BaseModel):
    id = CharField(unique=True)
    symbol = CharField()
    type = CharField()
    blockchain = CharField()
    amount = CharField()
    amount_usd = CharField()
    hash = CharField()
    from_owner = CharField()
    to_owner = CharField()

    class Meta:
        table_name ="whalepool_transactions"

    @property
    def to_string(self):
        return "{} {}\n{} ({}) from {} to {}".format(
            self.type,
            self.blockchain,
            self.amount,
            self.amount_usd,
            self.from_owner,
            self.to_owner
        )