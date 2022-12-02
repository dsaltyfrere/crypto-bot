from models.base_model import BaseModel, db
from peewee import IntegerField, CharField

class BitcoinPool(BaseModel):
    pool_id = IntegerField()
    pool_name = CharField()
    pool_url = CharField()
    pool_block_count = IntegerField()
    pool_rank = IntegerField()
    pool_empty_blocks = IntegerField()
    pool_slug = CharField()

    class Meta:
        table_name = "bitcoin_pools"
        database = db

    def to_string(self):
        return f"{self.pool_id}: {self.pool_name} - {self.pool_url} | Block count: {self.pool_block_count} - Rank: {self.pool_rank}"