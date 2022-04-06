from twarc.client2 import Twarc2

from backend.services.twitter_api_service import TwitterAPIService


class TestTwitterAPIService:
    """
    Test class to test the TwitterAPI service, which is the API layer that interacts with Twitter.
    """

    def test_get_tweet(self, mocker):
        """
        Tests the get_tweet function from the TwitterAPIService which retrieves a tweet.
        """
        # The following variable represents a result from querying Twarc for a specific tweet.
        # The general shape of this data is guaranteed. No need to deal with malformed data or different
        # shapes as it is guaranteed by Twarc.
        original_tweet = [{"data": [{"id": "0",
                                     "text": "Hello world, its a great day today!",
                                     "public_metrics": {
                                         "retweet_count": 1,
                                         "reply_count": 2,
                                         "like_count": 3,
                                         "quote_count": 4},
                                     "fake_attribute": "fake value"}]}]

        # Mock the Twarc API call to prevent querying Twitter
        mocker.patch.object(Twarc2, "tweet_lookup", return_value=original_tweet)

        # Fetch a tweet using the TwitterAPIService
        api = TwitterAPIService("fake_token")
        api_result = api.get_tweet("0")

        # The expected result is a parsed tweet containing only the needed attributes
        expected_result = {"id": "0",
                           "text": "Hello world, its a great day today!",
                           "retweet_count": 1,
                           "reply_count": 2,
                           "like_count": 3,
                           "quote_count": 4,
                           "sentiment": "positive"
                           }

        assert api_result == expected_result

    def test_get_conversation_thread(self, mocker):
        """
        Tests the get_conversation_thread function from the TwitterAPIService which retrieves a conversation thread.
        """
        # The following variable represents a result from querying Twarc for a specific conversation thread.
        # The results are purposefully in non-temporal order to showcase the TwitterAPIService handles this.
        # Again, The general shape of this data is guaranteed by Twarc.
        original_conversation_thread = [{"data": [{"id": "1",
                                                   "text": "I know right! The weather is beautiful",
                                                   "public_metrics": {
                                                       "retweet_count": 1,
                                                       "reply_count": 0,
                                                       "like_count": 1,
                                                       "quote_count": 0},
                                                   "referenced_tweets": [{"id": 0}],
                                                   "fake_attribute": "fake value"}]},
                                        {"data": [{"id": "0",
                                                   "text": "Hello world, its a great day today!",
                                                   "public_metrics": {
                                                       "retweet_count": 1,
                                                       "reply_count": 2,
                                                       "like_count": 3,
                                                       "quote_count": 4},
                                                   "fake_attribute": "fake value"}]}
                                        ]
        # Twarc returns results paginated by pages, so a list of lists
        page_result = [original_conversation_thread]

        # Mock the necessary Twarc calls
        mocker.patch.object(Twarc2, "search_recent", return_value=page_result)
        mocker.patch("twarc.expansions.ensure_flattened", return_value=iter(page_result))

        # Fetch a conversation thread using the TwitterAPIService
        api = TwitterAPIService("fake_token")
        parsed_conversation_thread = api.get_conversation_thread("0")

        # The expected parsed and sorted conversation thread
        expected_conversation_thread = [{"id": "0",
                                         "text": "Hello world, its a great day today!",
                                         "retweet_count": 1,
                                         "reply_count": 2,
                                         "like_count": 3,
                                         "quote_count": 4,
                                         "referenced_tweets": [],
                                         "sentiment": "positive"
                                         },
                                        {"id": "1",
                                         "text": "I know right! The weather is beautiful",
                                         "retweet_count": 1,
                                         "reply_count": 0,
                                         "like_count": 1,
                                         "quote_count": 0,
                                         "referenced_tweets": [{"id": 0}],
                                         "sentiment": "positive"
                                         },
                                        ]

        assert parsed_conversation_thread == expected_conversation_thread

    def test_get_tweets_from_keyword(self, mocker):
        """
        Tests the get_tweets_from_keyword function from the TwitterAPIService which retrieves tweets based on a
        keyword.
        """
        # The following variable represents a result from querying Twarc for a specific keyword using the
        # recent search API. The result is a list of tweets discussing the same topic. Once again, Twarc ensures
        # the integrity and shape of the data.
        keyword_search_tweets = [{"data": [{"id": "0",
                                            "text": "Python is really good",
                                            "public_metrics": {
                                                "retweet_count": 1,
                                                "reply_count": 0,
                                                "like_count": 1,
                                                "quote_count": 0},
                                            "attachments": {},
                                            "author": "Alice",
                                            "__twarc": {},
                                            "author_id": "123",
                                            "entities": [],
                                            "geo": "The moon"}]},
                                 {"data": [{"id": "1",
                                            "text": "There's an amazing new Python update, check it out!",
                                            "public_metrics": {
                                                "retweet_count": 1,
                                                "reply_count": 2,
                                                "like_count": 3,
                                                "quote_count": 4},
                                            "attachments": {},
                                            "author": "Bob",
                                            "__twarc": {},
                                            "author_id": "321",
                                            "entities": [],
                                            "geo": "The ocean"}]}
                                 ]

        # Twarc returns results paginated by pages, so a list of lists
        page_result = [keyword_search_tweets]

        # Mock the necessary Twarc calls
        mocker.patch.object(Twarc2, "search_recent", return_value=page_result)
        mocker.patch("twarc.expansions.ensure_flattened", return_value=iter(page_result))

        # Fetch tweets discussing the topic "Python" using TwitterAPIService (the API call is mocked, not real)
        api = TwitterAPIService("fake_token")
        parsed_tweets = api.get_tweets_from_keyword("Python", 1)  # Only retrieve 1 tweet discussing the topic

        # The expected parsed tweet discussing the topic "Python"
        expected_parsed_tweets = [{"id": "0",
                                   "text": "Python is really good",
                                   "retweet_count": 1,
                                   "reply_count": 0,
                                   "like_count": 1,
                                   "quote_count": 0,
                                   "sentiment": "positive"},
                                  ]

        assert parsed_tweets == expected_parsed_tweets
