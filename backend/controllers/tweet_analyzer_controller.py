from backend.services.tweet_tree_builder_service import TweetTreeBuilder
from backend.services.argumentation_service import ArgumentationAlgorithmService


class TweetAnalyzerController:
    """
    Controller class for the API to prevent business logic from leaking to the API later.
    Composes and orchestrates the services required to produce the argumentation models.
    """

    def analyze_tweet(self, tweet_id):
        """
        Given an input tweet, it will generate and return the final computed argumentation model,
        metrics and analysis

        :param tweet_id:    tweet id to analyse
        :return:            the argumentation model, metrics and analysis
        """
        # Create the tweet tree and metrics
        tweet_tree = TweetTreeBuilder(tweet_id).get_tweet_tree()
        tweet_tree_metrics = tweet_tree.get_tweet_tree_metrics()

        root_node = tweet_tree.get_tree().nodes[tweet_tree.get_root()]

        # Run the argumentation algorithm on the tweet tree
        max_score = tweet_tree.get_tweet_tree_metrics().get_max_public_metrics()
        min_score = tweet_tree.get_tweet_tree_metrics().get_min_public_metrics()

        argumentation_service = ArgumentationAlgorithmService(max_score, min_score, tweet_tree.get_tree(), tweet_tree_metrics)

        root_argument_score = argumentation_service.acceptability_degree(root_node)
        tweet_tree.metrics.set_root_tweet_argument_strength(root_argument_score)

        # Encode the output as JSON and return
        data = tweet_tree.get_json()

        return data


if __name__ == "__main__":
    pass
