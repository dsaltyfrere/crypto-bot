from peewee import CharField, IntegerField
from models.base_model import BaseModel

class Olhc(BaseModel):
    open = IntegerField()
    low = IntegerField()
    high = IntegerField()
    ticker = CharField()

    @property
    def to_string(self):
        return f"{self.ticker} | open: {self.open} - low: {self.low} - high: {self.high}"