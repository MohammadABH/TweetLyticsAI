from backend.services.tweet_tree_builder_service import TweetTreeBuilder
from backend.services.argumentation_service import ArgumentationAlgorithmService
import dill


class TweetAnalyzerController:

    def analyze_tweet(self, tweet_id):
        # tweet_tree = TweetTreeBuilder(tweet_id).get_tweet_tree()
        # tweet_tree_metrics = tweet_tree.get_tweet_tree_metrics()
        # # with open('tweet_tree.pkl', 'wb') as f:
        # #     dill.dump(tweet_tree, f)
        # # with open('tweet_tree.pkl', 'rb') as f:
        # #     tweet_tree = dill.load(f)
        #
        # root_node = tweet_tree.get_tree().nodes[tweet_tree.get_root()]
        #
        # max_score = tweet_tree.get_tweet_tree_metrics().get_max_public_metrics()
        # min_score = tweet_tree.get_tweet_tree_metrics().get_min_public_metrics()
        #
        # argumentation_service = ArgumentationAlgorithmService(max_score, min_score, tweet_tree.get_tree(), tweet_tree_metrics)
        #
        # root_argument_score = argumentation_service.acceptability_degree(root_node)
        # tweet_tree.metrics.set_root_tweet_argument_strength(root_argument_score)
        #
        # data = tweet_tree.get_json()
        # with open('data.pkl', 'wb') as f:
        #     dill.dump(data, f)
        with open('data.pkl', 'rb') as f:
            data = dill.load(f)

        return data
