class ArgumentationAlgorithmService:

    def __init__(self, max_score, min_score, tweet_tree, tweet_tree_metrics):
        self.max_score = max_score
        self.min_score = min_score
        self.tweet_tree = tweet_tree
        self.tweet_tree_metrics = tweet_tree_metrics

    def _base_strength(self, tweet):
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
        degree = 1 - ((1 - self._base_strength(tweet) ** 2) / (1 + (self._base_strength(tweet) * (2 ** strength_child))))
        tweet["attributes"]["acceptability"] = degree

        self.tweet_tree_metrics.set_strongest_argument_id(tweet["attributes"]["id"], degree)

        return degree

