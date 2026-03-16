from __future__ import annotations

from sentiment.reddit_scraper import RedditScraper
from sentiment.twitter_scraper import TwitterScraper


class SentimentModel:
    def __init__(self):
        self.twitter = TwitterScraper()
        self.reddit = RedditScraper()

    def aggregate(self, symbol: str) -> float:
        tw = self.twitter.score(symbol)
        rd = self.reddit.score(symbol)
        return (tw + rd) / 2
