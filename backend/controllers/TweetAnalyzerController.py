from backend.services.tweet_tree_builder_service import TweetTreeBuilder
from backend.services.argumentation_service import ArgumentationAlgorithmService


class TweetAnalyzerController:

    def analyze_tweet(self, tweet_id):
        tweet_tree = TweetTreeBuilder(tweet_id).get_tweet_tree()
        root_node = tweet_tree.get_tree().nodes[tweet_tree.get_root()]

        max_score = tweet_tree.get_tweet_tree_metrics().get_max_public_metrics()

        argumentation_service = ArgumentationAlgorithmService(max_score, tweet_tree.get_tree())

        root_argument_score = argumentation_service.acceptability_degree(root_node)
        tweet_tree.metrics.set_root_tweet_argument_strength(root_argument_score)

        data = tweet_tree.get_json()

        return data
