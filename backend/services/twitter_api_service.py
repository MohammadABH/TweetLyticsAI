from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened
from backend.services.sentiment_analysis_service import BertweetSentimentAnalysis


class TwitterAPIService:

    sentiment_analysis_service = BertweetSentimentAnalysis()

    def __init__(self, bearer_token):
        self.twarc = Twarc2(bearer_token=bearer_token)

    def get_tweet_sentiment(self, tweet):
        tweet_sentiment = TwitterAPIService.sentiment_analysis_service.predict_sentiment(tweet)
        return tweet_sentiment

    def parse_tweet_reply(self, tweet):
        return {"id": tweet["id"],
                "text": tweet["text"],
                "referenced_tweets": tweet["referenced_tweets"] if "referenced_tweets" in tweet else [],
                "retweet_count": tweet["public_metrics"]["retweet_count"],
                "reply_count": tweet["public_metrics"]["reply_count"],
                "like_count": tweet["public_metrics"]["like_count"],
                "quote_count": tweet["public_metrics"]["quote_count"],
                "sentiment": self.get_tweet_sentiment(tweet["text"])}

    def parse_tweet_keyword(self, tweet):
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
        tweet["sentiment"] = self.get_tweet_sentiment(tweet["text"])
        tweet.pop('public_metrics', None)

        return tweet

    def parse_tweet(self, tweet):
        return {"id": tweet["id"],
                "text": tweet["text"],
                "retweet_count": tweet["public_metrics"]["retweet_count"],
                "reply_count": tweet["public_metrics"]["reply_count"],
                "like_count": tweet["public_metrics"]["like_count"],
                "quote_count": tweet["public_metrics"]["quote_count"],
                "sentiment": self.get_tweet_sentiment(tweet["text"])}

    def get_tweet(self, tweet_id):
        tweet_lookup = self.twarc.tweet_lookup([tweet_id])

        for current_tweet in tweet_lookup:
            tweet = current_tweet

        parsed_tweet = self.parse_tweet(tweet['data'][0])

        return parsed_tweet

    def get_conversation_thread(self, conversation_id):
        search_query = f"conversation_id: {conversation_id} lang:en"
        tweet_fields = "in_reply_to_user_id,public_metrics"
        search_result = self.twarc.search_recent(query=search_query, tweet_fields=tweet_fields)

        conversation_thread = []
        for page in search_result:
            for tweet in ensure_flattened(page):
                parsed_tweet = self.parse_tweet_reply(tweet)
                conversation_thread.append(parsed_tweet)

        conversation_thread.sort(key=lambda x: x["id"])

        return conversation_thread

    def get_tweets_from_keyword(self, keyword, number_of_tweets=5):
        search_query = f"{keyword} lang:en -is:retweet -is:reply -is:quote"
        tweet_fields = "id,text,public_metrics"
        search_result = self.twarc.search_recent(query=search_query, tweet_fields=tweet_fields, max_results=100)

        tweets = []
        for page in search_result:
            for tweet in ensure_flattened(page):
                parsed_tweet = self.parse_tweet_keyword(tweet)
                tweets.append(parsed_tweet)
                number_of_tweets -= 1

            if number_of_tweets <= 0:
                break

        return tweets

    def get_tweets_from_hashtag(self, hashtag):
        if not hashtag.startswith("#"):
            hashtag = "#" + hashtag

        tweets = self.get_tweets_from_keyword(hashtag)

        return tweets


# api = TwitterAPIService(
#     "AAAAAAAAAAAAAAAAAAAAAERfVAEAAAAA0rjC0YSarrfSEE88Ar2CF5I2RYs%3DkVWG3XwyVVx2zFcu4ISP32Gu9ajF3k7EK8iNOOkSuG1EQQunUB")
# t = api.get_tweet(1496982622693695496)
# print(t)
