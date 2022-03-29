from backend.controllers.tweet_analyzer_controller import TweetAnalyzerController
from backend.services.tweet_tree_builder_service import TweetTreeMetrics, TweetTree


class TestTweetAnalyzerController:
    """
    Test class that tests the TweetAnalyzerController which composes the services all together, used by the API.
    """

    def test_analyze_tweet(self, mocker):
        """
        Tests the analyze_tweet function from the TestTweetAnalyzerController that co-ordinates the services together.
        """
        controller = TweetAnalyzerController()

        # Create a test tweet that will be the root of the tree
        root_tweet = {
            "id": 0,
            "like_count": 0.1,
            "retweet_count": 0,
            "argumentative_type": "none",
            "sentiment": "positive"
        }

        # Create test tree and metrics
        metrics = TweetTreeMetrics()
        tweet_tree = TweetTree(root_tweet, [], metrics)

        # Mock the _build_tweet_tree to prevent querying the Twitter API
        mocker.patch("backend.services.tweet_tree_builder_service.TweetTreeBuilder._build_tweet_tree",
                     return_value=tweet_tree)

        # Analyze a test tweet
        data = controller.analyze_tweet(0)

        # The expected output consists of aggregated metrics and the argumentation model itself
        expected_data = {'tweet_tree':
                             {'attributes':
                                  {'id': 0,
                                   'like_count': 0.1,
                                   'retweet_count': 0,
                                   'argumentative_type': 'none',
                                   'sentiment': 'positive',
                                   'acceptability': 0.5
                                   },
                              'name': 0,
                              'children': []
                              },
                         'metrics': {
                             'root_tweet_sentiment': '',
                             'root_tweet_argument_strength': 0.5,
                             'strongest_argument_id': 0,
                             'sentiment_towards_root': '',
                             'general_sentiment': 'positive'
                         }
                         }

        assert data == expected_data
