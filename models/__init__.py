from models.base_model import initialize_db
from models.feeds.feed import Feed
from models.feeds.entry import FeedEntry


initialize_db([Feed, FeedEntry])