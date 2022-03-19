class ArgumentationAlgorithmService:

    def __init__(self, max_score, min_score, tweet_tree, tweet_tree_metrics):
        self.max_score = max_score
        self.min_score = min_score
        self.tweet_tree = tweet_tree
        self.tweet_tree_metrics = tweet_tree_metrics

    def base_strength(self, tweet):
        if tweet["attributes"]["argumentative_type"] == "none":
            return 0.5  # TODO MAKE CONSTANT

        score = tweet["attributes"]["like_count"] + tweet["attributes"]["retweet_count"]
        normalized_score = ((score - self.min_score) / (self.max_score - self.min_score) + 0.000001)

        return normalized_score

    def acceptability_degree(self, tweet):
        if tweet is None or tweet["attributes"]["argumentative_type"] == "neutral":
            return 0.0

        supporters_score = 0.0
        attackers_score = 0.0

        for child_tweet_id in self.tweet_tree.successors(tweet["attributes"]["id"]):
            child_tweet = self.tweet_tree.nodes[child_tweet_id]
            score = self.acceptability_degree(child_tweet)

            if child_tweet["attributes"]["argumentative_type"] == "support":
                supporters_score += score
            else:
                attackers_score += score

        strength_child = supporters_score - attackers_score
        degree = 1 - ((1 - self.base_strength(tweet)**2) / (1 + (self.base_strength(tweet) * (2 ** strength_child))))
        tweet["attributes"]["acceptability"] = degree

        self.tweet_tree_metrics.set_strongest_argument_id(tweet["attributes"]["id"], degree)

        return degree


# g = DiGraph()
#
# node_0 = {
#     "id": 0,
#     "public_metrics": {
#         "like_count": 0.1,
#         "retweet_count": 0
#     },
#     "argumentative_type": "none"
# }
#
# node_1 = {
#     "id": 1,
#     "public_metrics": {
#         "like_count": 0.9,
#         "retweet_count": 0
#     },
#     "argumentative_type": "support"
# }
#
# node_2 = {
#     "id": 2,
#     "public_metrics": {
#         "like_count": 0.95,
#         "retweet_count": 0
#     },
#     "argumentative_type": "attack"
# }
#
# node_3 = {
#     "id": 3,
#     "public_metrics": {
#         "like_count": 0.8,
#         "retweet_count": 0
#     },
#     "argumentative_type": "attack"
# }
#
# g.add_node(0, attributes=node_0)
# g.add_node(1, attributes=node_1)
# g.add_node(2, attributes=node_2)
# g.add_node(3, attributes=node_3)
#
# g.add_edge(0, 1)
# g.add_edge(0, 2)
# g.add_edge(0, 3)
#
# arg = ArgumentationAlgorithmService(1, g)
# print(arg.acceptability_degree(g.nodes[0]))
