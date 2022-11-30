from .base_model import BaseModel
from peewee import CharField, BooleanField, IntegerField

class Feed(BaseModel):
    feed_name = CharField()
    feed_preview = BooleanField(default=True)
    feed_url = CharField()
    feed_fetch_attempts = IntegerField(default = 0)
    feed_enabled = BooleanField(default = True)
    feed_datetime_regex = CharField(null=True)

    class Meta:
        table_name = "feeds"

    def to_string(self):
        return f"{self.feed_name}: {self.feed_url} | Preview: {self.feed_preview} | Fetch attempts: {self.feed_fetch_attempts} | Enabled: {'Yes' if self.feed_enabled else 'No'}"
