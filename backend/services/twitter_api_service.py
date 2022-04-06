from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened

from backend.services.sentiment_analysis_service import SentimentAnalysis


class TwitterAPIService:
    """
    Service that acts as a wrapper around the Twitter API to provide the rest of the application simple access to
    the API. Provides high level functions to accessing information and data from the Twitter API.
    """

    sentiment_analysis_service = SentimentAnalysis()

    def __init__(self, bearer_token):
        self.twarc = Twarc2(bearer_token=bearer_token)

    def _get_tweet_sentiment(self, tweet):
        tweet_sentiment = TwitterAPIService.sentiment_analysis_service.predict_sentiment(tweet)
        return tweet_sentiment

    def _parse_tweet_reply(self, tweet):
        return {"id": tweet["id"],
                "text": tweet["text"],
                "referenced_tweets": tweet["referenced_tweets"] if "referenced_tweets" in tweet else [],
                "retweet_count": tweet["public_metrics"]["retweet_count"],
                "reply_count": tweet["public_metrics"]["reply_count"],
                "like_count": tweet["public_metrics"]["like_count"],
                "quote_count": tweet["public_metrics"]["quote_count"],
                "sentiment": self._get_tweet_sentiment(tweet["text"])}

    def _parse_tweet_keyword(self, tweet):
        tweet.pop('attachments', None)
        tweet.pop('author', None)
        tweet.pop('__twarc', None)
        tweet.pop('author_id', None)
        tweet.pop('entities', None)
        tweet.pop('geo', None)
        tweet["retweet_count"] = tweet["public_metrics"]["retweet_count"]
        tweet["reply_count"] = tweet["public_metrics"]["reply_count"]
        tweet["like_count"] = tweet["public_metrics"]["like_count"]
        tweet["quote_count"] = tweet["public_metrics"]["quote_count"]
        tweet["sentiment"] = self._get_tweet_sentiment(tweet["text"])
        tweet.pop('public_metrics', None)

        return tweet

    def _parse_tweet(self, tweet):
        return {"id": tweet["id"],
                "text": tweet["text"],
                "retweet_count": tweet["public_metrics"]["retweet_count"],
                "reply_count": tweet["public_metrics"]["reply_count"],
                "like_count": tweet["public_metrics"]["like_count"],
                "quote_count": tweet["public_metrics"]["quote_count"],
                "sentiment": self._get_tweet_sentiment(tweet["text"])}

    def get_tweet(self, tweet_id):
        # Fetch tweet from Twitter API
        tweet_lookup = self.twarc.tweet_lookup([tweet_id])

        for current_tweet in tweet_lookup:
            tweet = current_tweet

        # Parse the tweet
        parsed_tweet = self._parse_tweet(tweet['data'][0])

        return parsed_tweet

    def get_conversation_thread(self, conversation_id):
        # Query Twitter API for the conversation thread using conversation_id, only allow English resukts
        search_query = f"conversation_id: {conversation_id} lang:en"
        tweet_fields = "in_reply_to_user_id,public_metrics"
        search_result = self.twarc.search_recent(query=search_query, tweet_fields=tweet_fields)

        # Parse the output to a list
        conversation_thread = []
        for page in search_result:
            for tweet in ensure_flattened(page):
                parsed_tweet = self._parse_tweet_reply(tweet)
                conversation_thread.append(parsed_tweet)

        conversation_thread.sort(key=lambda x: x["id"])

        return conversation_thread

    def get_tweets_from_keyword(self, keyword, number_of_tweets=15):
        # Query the Twitter API for (default 15) tweets that discuss a certain keyword
        # The tweet must be original, not a retweet, a reply or quote
        search_query = f"{keyword} lang:en -is:retweet -is:reply -is:quote"
        tweet_fields = "id,text,public_metrics"
        search_result = self.twarc.search_recent(query=search_query, tweet_fields=tweet_fields, max_results=number_of_tweets)

        # Parse the tweets
        tweets = []
        for page in search_result:
            for tweet in ensure_flattened(page):
                parsed_tweet = self._parse_tweet_keyword(tweet)
                tweets.append(parsed_tweet)
                number_of_tweets -= 1

                if number_of_tweets <= 0:
                    return tweets

        return tweets


if __name__ == "__main__":
    pass
