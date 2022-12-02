from models.base_model import BaseModel, db
from peewee import IntegerField, BigIntegerField, DateTimeField

class LightningNetworkStat(BaseModel):
    stat_id = IntegerField()
    added = DateTimeField()
    channel_count = IntegerField()
    node_count = IntegerField()
    total_capacity = BigIntegerField()
    tor_nodes = IntegerField()
    clearnet_nodes = IntegerField()
    unannounced_nodes = IntegerField()
    average_capacity = BigIntegerField()
    average_fee_rate = IntegerField()
    average_base_fee_mtokens = IntegerField()
    median_capacity = BigIntegerField()
    median_fee_rate = IntegerField()
    median_base_fee_mtokens = IntegerField()
    clearnet_tor_nodes = IntegerField()