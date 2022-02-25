from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened

class TwitterAPIService:

    def __init__(self, bearer_token):
        self.twarc = Twarc2(bearer_token=bearer_token)

    def parse_tweet(self, tweet):
        return {"id": tweet["id"], "text": tweet["text"]}

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
                parsed_tweet = self.parse_tweet(tweet)
                conversation_thread.append(parsed_tweet)

        conversation_thread.sort(key=lambda x: x["id"])

        return conversation_thread

    def get_tweets_from_keyword(self, keyword, number_of_tweets=100):
        search_query = f"#{keyword} lang:en -is:retweet -is:reply -is:quote"
        search_result = self.twarc.search_recent(query=search_query)

        tweets = []
        for page in search_result:
            for tweet in ensure_flattened(page):
                if number_of_tweets == 0:
                    break
                else:
                    tweets.append(tweet)
                    number_of_tweets -= 1
        return tweets

    def get_tweets_from_hashtag(self, hashtag):
        if not hashtag.startswith("#"):
            hashtag = "#" + hashtag

        tweets = self.get_tweets_from_keyword(hashtag)

        return tweets


api = TwitterAPIService(
    "AAAAAAAAAAAAAAAAAAAAAERfVAEAAAAA0rjC0YSarrfSEE88Ar2CF5I2RYs%3DkVWG3XwyVVx2zFcu4ISP32Gu9ajF3k7EK8iNOOkSuG1EQQunUB")
t = api.get_tweet(1496842722681966597)
print(t)
