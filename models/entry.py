import datetime

from .base_model import BaseModel, db
from .feed import Feed
from peewee import ForeignKeyField, CharField, BooleanField, DateTimeField


class FeedEntry(BaseModel):
    feed = ForeignKeyField(Feed, to_field='id')
    entry_title = CharField(null=True)
    entry_link = CharField()
    entry_published_at = CharField()
    send = BooleanField()

    class Meta:
        table_name = "entries"
        database = db

    def to_string(self):
        ...