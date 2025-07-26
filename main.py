import tweepy
from textblob import TextBlob
from pymongo import MongoClient

# --- Twitter API Bearer Token ---
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANoC3QEAAAAAtHIaSA44xrQU8QiAwJld9AeGAo0%3DKDL1Jh4j8YCgeCWoFrpr6cccfqS12ZW3Mn4tiv1gk1RbDwIW7Q"  

# --- MongoDB setup ---
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter_db"]
collection = db["tweets"]

# --- Tweepy Streaming Client ---
class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        text = tweet.text
        analysis = TextBlob(text)
        sentiment = (
            "positive" if analysis.sentiment.polarity > 0
            else "negative" if analysis.sentiment.polarity < 0
            else "neutral"
        )
        data = {
            "tweet": text,
            "sentiment": sentiment,
            "polarity": analysis.sentiment.polarity
        }
        collection.insert_one(data)
        print(f"Tweet: {text}\nSentiment: {sentiment}\n")

    def on_connection_error(self):
        self.disconnect()

# --- Start Streaming ---
stream = MyStream(BEARER_TOKEN)
stream.add_rules(tweepy.StreamRule("AI OR machine learning OR technology lang:en"))
stream.filter(tweet_fields=["created_at"])
