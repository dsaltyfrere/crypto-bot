from models.base_model import initialize_db
from models.feed import Feed
from models.entry import FeedEntry


initialize_db([Feed, FeedEntry])