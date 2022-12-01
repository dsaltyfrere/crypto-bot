from models.base_model import BaseModel
from peewee import CharField, ForeignKeyField, IntegerField, DateTimeField
from models.whalepool.ticker import Ticker

import datetime

class HighLow(BaseModel):
    ticker = ForeignKeyField(Ticker, to_field="id")
    price = IntegerField()
    inserted_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "highlow"
    
    @property
    def repr(self):
        return f"{self.ticker} - {self.inserted_at}: {self.price}"