from models.base_model import BaseModel
from peewee import CharField

class Ticker(BaseModel):
    ticker = CharField()
    exchange = CharField()
    symbol = CharField(null=True)

    class Meta:
        table_name = "tickers"

    @property
    def to_string(self):
        return f"{self.ticker} - {self.exchange} - {self.symbol}"