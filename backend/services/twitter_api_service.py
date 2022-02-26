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
                "sentiment": self.get_tweet_sentiment(tweet["text"])}

    def parse_tweet(self, tweet):
        return {"id": tweet["id"],
                "text": tweet["text"],
                "sentiment": self.get_tweet_sentiment(tweet["text"])}

    def get_tweet(self, tweet_id):
        tweet_lookup = self.twarc.tweet_lookup([tweet_id])

        for current_tweet in tweet_lookup:
            tweet = current_tweet

        parsed_tweet = self.parse_tweet(tweet['data'][0])

        return parsed_tweet

    def get_conversation_thread(self, conversation_id):
        search_query = f"conversation_id: {conversation_id} lang:en"
        search_result = self.twarc.search_recent(query=search_query)

        conversation_thread = []
        for page in search_result:
            for tweet in ensure_flattened(page):
                parsed_tweet = self.parse_tweet_reply(tweet)
                conversation_thread.append(parsed_tweet)

        conversation_thread.sort(key=lambda x: x["id"])

        return conversation_thread

    def get_tweets_from_keyword(self, keyword, number_of_tweets=100):
        search_query = f"{keyword} lang:en -is:retweet -is:reply -is:quote"
        search_result = self.twarc.search_recent(query=search_query, max_results=100)

        tweets = []
        for page in search_result:
            for tweet in ensure_flattened(page):
                tweets.append(tweet)
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
