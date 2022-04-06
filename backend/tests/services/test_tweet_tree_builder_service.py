from backend.services.tweet_tree_builder_service import TweetTreeMetrics, TweetTree, TweetTreeBuilder


class TestTweetTreeMetrics:
    """
    Test class that tests the TweetTreeMetrics class which is responsible for aggregated general metrics about
    the tweet tree.
    """

    def test_set_root_tweet_sentiment(self):
        """
        Tests the set_root_tweet_sentiment function that sets the sentiment of the root tweet in the metric object.
        """
        metrics = TweetTreeMetrics()
        metrics.set_root_tweet_sentiment("positive")

        root_tweet_sentiment = metrics.get_metrics()["root_tweet_sentiment"]
        expected_root_tweet_sentiment = "positive"

        assert expected_root_tweet_sentiment == root_tweet_sentiment

    def test_set_root_tweet_argument_strength(self):
        """
        Tests the set_root_tweet_argument_strength function that sets the argument strength of the root tweet in
        the metric object.
        """
        metrics = TweetTreeMetrics()
        metrics.set_root_tweet_argument_strength(10)

        root_tweet_sentiment = metrics.get_metrics()["root_tweet_argument_strength"]
        expected_root_tweet_sentiment = 10

        assert expected_root_tweet_sentiment == root_tweet_sentiment

    def test_set_strongest_argument_id(self):
        """
        Tests the set_strongest_argument_id function which sets the strongest argument ID in the metric object.
        """
        metrics = TweetTreeMetrics()

        # Add several arguments, with ID = 1 the strongest
        metrics.set_strongest_argument_id(0, 1)
        metrics.set_strongest_argument_id(1, 10)
        metrics.set_strongest_argument_id(2, 5)

        # Get the strongest argument
        strongest_argument_id = metrics.get_metrics()["strongest_argument_id"]
        expected_strongest_argument_id = 1

        assert strongest_argument_id == expected_strongest_argument_id

    def test_max_min_public_metrics(self):
        """
        Tests the max min public metrics logic which handles the maximum and minimum public metrics of a tweet in
        the tree.
        """
        metrics = TweetTreeMetrics()

        # Make 2 tweets, one popular one unpopular
        popular_tweet = {"like_count": 100, "retweet_count": 50}
        unpopular_tweet = {"like_count": 2, "retweet_count": 1}

        # Set the max and min in the metrics object
        metrics.set_max_min_public_metrics(popular_tweet)
        metrics.set_max_min_public_metrics(unpopular_tweet)

        max_public_metrics = metrics.get_max_public_metrics()
        min_public_metrics = metrics.get_min_public_metrics()

        expected_max_public_metrics = 150
        expected_min_public_metrics = 3

        assert max_public_metrics == expected_max_public_metrics
        assert min_public_metrics == expected_min_public_metrics

    def test_general_sentiment(self):
        """
        Tests the general sentiment logic which manages the general sentiment of a tree.
        """
        metrics = TweetTreeMetrics()

        metrics.increment_general_sentiment("positive")
        metrics.increment_general_sentiment("positive")
        metrics.increment_general_sentiment("negative")
        metrics.increment_general_sentiment("neutral")

        general_sentiment = metrics.get_metrics()["general_sentiment"]
        expected_general_sentiment = "positive"

        assert general_sentiment == expected_general_sentiment

    def test_sentiment_towards_root(self):
        """
        Tests the sentiment towards the root tweet logic.
        """
        metrics = TweetTreeMetrics()

        metrics.increment_root_sentiment("positive")
        metrics.increment_root_sentiment("positive")
        metrics.increment_root_sentiment("negative")
        metrics.increment_root_sentiment("neutral")
        metrics.compute_sentiment_towards_root()

        general_sentiment = metrics.get_metrics()["sentiment_towards_root"]
        expected_general_sentiment = "positive"

        assert general_sentiment == expected_general_sentiment


class TestTweetTree:
    """
    Tests the TweetTree class which holds the tweets in a tweet data structure.
    """

    def test_tweet_tree(self):
        """
        Tests the entire logic of the TweetTree class, handling all branches in the logic based on the
        mock data given to it.
        """
        # The shapes of mock data ensure all logic is tested

        # Mock tweet
        root_tweet = {"id": "0",
                      "text": "Python is a superb programming language",
                      "retweet_count": 1,
                      "reply_count": 2,
                      "like_count": 3,
                      "quote_count": 4,
                      "referenced_tweets": [],
                      "sentiment": "positive"
                      }

        # Mock conversation thread
        conversation_thread = [{"id": "1",
                                "text": "I agree! it is amazing for AI and ML as well",
                                "retweet_count": 1,
                                "reply_count": 0,
                                "like_count": 1,
                                "quote_count": 0,
                                "referenced_tweets": [{"id": "0", "text": "Python is a superb programming language"}],
                                "sentiment": "positive"
                                },
                               {"id": "2",
                                "text": "This is a reply to a deleted tweet",
                                "retweet_count": 0,
                                "reply_count": 0,
                                "like_count": 0,
                                "quote_count": 0,
                                "referenced_tweets": [{"id": "150", "text": "deleted"}],
                                "sentiment": "neutral"
                                },
                               {"id": "3",
                                "text": "This is a reply to reply. I agree, its amazing!",
                                "retweet_count": 0,
                                "reply_count": 0,
                                "like_count": 1,
                                "quote_count": 0,
                                "referenced_tweets": [
                                    {"id": "1", "text": "I agree! it is amazing for AI and ML as well"}],
                                "sentiment": "positive"
                                },
                               ]
        metrics = TweetTreeMetrics()

        tweet_tree = TweetTree(root_tweet, conversation_thread, metrics)
        tweet_tree_json = tweet_tree.get_json()

        # This is what the JSON data should look like, if it is the same, all logic is correct
        expected_tweet_tree_json = {'tweet_tree': {'attributes': {'id': '0', 'text': 'Python is a superb programming '
                                                                                     'language', 'retweet_count': 1,
                                                                  'reply_count': 2, 'like_count': 3, 'quote_count':
                                                                      4, 'referenced_tweets': [], 'sentiment':
                                                                      'positive'}, 'name': '0', 'children': [{
            'attributes': {'id': '1', 'text': 'I agree! it is amazing for AI and ML as well', 'retweet_count': 1,
                           'reply_count': 0, 'like_count': 1, 'quote_count': 0, 'sentiment': 'positive',
                           'argumentative_type': 'support'}, 'name': '1', 'children': [{'attributes': {'id': '3',
                                                                                                       'text': 'This '
                                                                                                               'is a '
                                                                                                               'reply '
                                                                                                               'to '
                                                                                                               'reply. I agree, its amazing!',
                                                                                                       'retweet_count': 0,
                                                                                                       'reply_count': 0,
                                                                                                       'like_count': 1,
                                                                                                       'quote_count': 0,
                                                                                                       'sentiment': 'positive',
                                                                                                       'argumentative_type': 'support'},
                                                                                        'name': '3'}]}]},
                                    'metrics': {'root_tweet_sentiment': '', 'root_tweet_argument_strength': '',
                                                'strongest_argument_id': '', 'sentiment_towards_root': '',
                                                'general_sentiment': 'positive'}}

        assert tweet_tree_json == expected_tweet_tree_json


class TestTweetTreeBuilder:
    """
    Test class that tests the class TweetTreeBuilder that builds tweet trees.
    """

    def test_tweet_tree_builder(self, mocker):
        """
        Tests the tweet building logic.
        """
        # Mock tweet
        root_tweet = {"id": "0",
                      "text": "I love Pizza",
                      "retweet_count": 25,
                      "reply_count": 0,
                      "like_count": 29,
                      "quote_count": 0,
                      "sentiment": "positive"}

        # Mock the API calls to prevent querying Twitter
        mocker.patch("backend.services.twitter_api_service.TwitterAPIService.get_tweet", return_value=root_tweet)
        mocker.patch("backend.services.twitter_api_service.TwitterAPIService.get_conversation_thread", return_value=[])
        mocker.patch("backend.services.twitter_api_service.TwitterAPIService.get_tweets_from_keyword", return_value=[])

        # Build the tweet tree
        builder = TweetTreeBuilder("0")

        tweet_tree_json = builder.get_tweet_tree().get_json()

        # The expected tree shape
        expected_tweet_tree_json = {'tweet_tree': {'attributes': {
            'id': '0',
            'text': 'I love Pizza',
            'retweet_count': 25,
            'reply_count': 0,
            'like_count': 29,
            'quote_count': 0,
            'sentiment': 'positive',
            'argumentative_type': 'none'
        }, 'name': '0', 'children': []},
            'metrics': {
                'root_tweet_sentiment': 'positive',
                'root_tweet_argument_strength': '',
                'strongest_argument_id': '',
                'sentiment_towards_root': 'positive',
                'general_sentiment': 'positive'
            }
        }

        assert tweet_tree_json == expected_tweet_tree_json
