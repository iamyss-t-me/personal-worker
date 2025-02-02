import feedparser
from config import Config
from DB.video import DB


async def get_link():
    db = DB()
    titles = [video.title for video in db.get_videos()]
    feed = feedparser.parse(Config.RSS_URL)
    for entry in feed.entries:
        if entry.title not in titles:
            return entry
        continue
    return None

