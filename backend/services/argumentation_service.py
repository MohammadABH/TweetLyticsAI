class ArgumentationAlgorithmService:
    """
    Service that runs the EBS argumentation algorithm on a tweet tree
    """

    def __init__(self, max_score, min_score, tweet_tree, tweet_tree_metrics):
        """
        Constructor of the service

        :param max_score:           max base score of all the nodes in the tree
        :param min_score:           min base score of all the nodes in the tree
        :param tweet_tree:          the input tweet tree to compute the EBS algorithm on
        :param tweet_tree_metrics:  the metrics object of the tweet tree
        """
        self.max_score = max_score
        self.min_score = min_score
        self.tweet_tree = tweet_tree
        self.tweet_tree_metrics = tweet_tree_metrics

    def _base_strength(self, tweet):
        """
        Computes the base strength of a tweet node

        :param tweet:   input tweet node to compute base strength
        :return:        base strength of input tweet node
        """
        DEFAULT_ORIGINAL_TWEET_SCORE = 0.5
        if tweet["attributes"]["argumentative_type"] == "none":
            # If the tweet is the original input tweet node, return 0.5
            # This is because the original tweet is always the one with the highest public metrics.
            # Hence, it skews the algorithm, this logic is discussed further in the report.
            return DEFAULT_ORIGINAL_TWEET_SCORE

        # Compute and return the normalized score, add 0.000001 to denominator to prevent division by 0 error
        score = tweet["attributes"]["like_count"] + tweet["attributes"]["retweet_count"]
        normalized_score = ((score - self.min_score) / (self.max_score - self.min_score) + 0.000001)

        return normalized_score

    def acceptability_degree(self, tweet):
        """
        Computes the EBS acceptability degree of a tweet node that represents the strength of an argument

        :param tweet:   input tweet node to compute acceptability degree using EBS
        :return:        acceptability degree of input tweet node
        """
        if tweet is None or tweet["attributes"]["argumentative_type"] == "neutral":
            # The tweet is non-argumentative, hence, should not be included in the algorithm
            return 0.0

        # Run the EBS algorithm as normal, it is practically a 1:1 mapping from here
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

