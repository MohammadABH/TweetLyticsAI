import os
from dotenv import load_dotenv
import networkx as nx
from networkx.readwrite import json_graph

from backend.services.twitter_api_service import TwitterAPIService
from backend.services.keyword_extraction_service import KeywordExtractor
from backend.services.relation_based_classifier_service import RelationBasedClassifierServiceBert


class TweetTreeMetrics:
    """
    Class that computes the aggregated general metrics about a tweet tree argumentation model to give the
    user some analysis without requiring them to inspect each node.
    """

    def __init__(self):
        self.root_tweet_sentiment = ""
        self.root_tweet_argument_strength = ""

        self.strongest_argument_id = ""
        self.strongest_argument_score = 0.0

        self.general_positive_sentiment_count = 0
        self.general_negative_sentiment_count = 0
        self.general_neutral_sentiment_count = 0

        self.root_positive_sentiment_count = 0
        self.root_negative_sentiment_count = 0
        self.root_neutral_sentiment_count = 0
        self.sentiment_towards_root = ""

        self.max_public_metrics = 0
        self.min_public_metrics = 0
        self.min_public_metrics_set = False

    def set_root_tweet_sentiment(self, root_tweet_sentiment):
        self.root_tweet_sentiment = root_tweet_sentiment

    def set_root_tweet_argument_strength(self, root_tweet_argument_strength):
        self.root_tweet_argument_strength = root_tweet_argument_strength

    def set_strongest_argument_id(self, strongest_argument_id, argument_strength):
        if argument_strength > self.strongest_argument_score:
            self.strongest_argument_id = strongest_argument_id
            self.strongest_argument_score = argument_strength

    def _set_max_public_metrics(self, tweet):
        score = tweet["like_count"] + tweet["retweet_count"]

        if score > self.max_public_metrics:
            self.max_public_metrics = score

    def _set_min_public_metrics(self, tweet):
        score = tweet["like_count"] + tweet["retweet_count"]

        if score < self.min_public_metrics:
            self.min_public_metrics = score
            self.min_public_metrics_set = True

        # This is to ensure that it gets updated initially as it is initialized to 0. An alternative
        # is to initialize it to an extremely large number, but that would break the ArgumentationAlgorithmService
        # as it needs the min metric, and using a big number will break the algorithm
        if self.min_public_metrics == 0 and self.min_public_metrics_set is False:
            self.min_public_metrics = score
            self.min_public_metrics_set = True

    def set_max_min_public_metrics(self, tweet):
        self._set_max_public_metrics(tweet)
        self._set_min_public_metrics(tweet)

    def increment_general_sentiment(self, sentiment_type):
        if sentiment_type == "positive":
            self.general_positive_sentiment_count += 1
        elif sentiment_type == "negative":
            self.general_negative_sentiment_count += 1
        else:
            self.general_neutral_sentiment_count += 1

    def increment_root_sentiment(self, sentiment_type):
        if sentiment_type == "positive":
            self.root_positive_sentiment_count += 1
        elif sentiment_type == "negative":
            self.root_negative_sentiment_count += 1
        else:
            self.root_neutral_sentiment_count += 1

    def compute_general_sentiment(self):
        values = [self.general_positive_sentiment_count,
                  self.general_negative_sentiment_count,
                  self.general_neutral_sentiment_count]
        labels = ["positive", "negative", "neutral"]

        labels_with_values = zip(values, labels)
        max_label = max(labels_with_values)[1]  # Max label is the mode, as it is the max of all the sentiment counts

        return max_label

    def compute_sentiment_towards_root(self):
        values = [self.root_positive_sentiment_count,
                  self.root_negative_sentiment_count,
                  self.root_neutral_sentiment_count]
        labels = ["positive", "negative", "neutral"]

        labels_with_values = zip(values, labels)
        max_label = max(labels_with_values)[1]  # Max label is the mode, as it is the max of all the sentiment counts

        self.sentiment_towards_root = max_label

    def get_max_public_metrics(self):
        return self.max_public_metrics

    def get_min_public_metrics(self):
        return self.min_public_metrics

    def get_metrics(self):
        return {
            "root_tweet_sentiment": self.root_tweet_sentiment,
            "root_tweet_argument_strength": self.root_tweet_argument_strength,
            "strongest_argument_id": self.strongest_argument_id,
            "sentiment_towards_root": self.sentiment_towards_root,
            "general_sentiment": self.compute_general_sentiment()
        }


class TweetTree:
    """
    Tweet tree data structure that ensures O(1) operations, uses a networkx DiGraph internally.
    """

    def __init__(self, root_tweet, conversation_thread, metrics):
        self.tree = nx.DiGraph()
        self.root = None
        self.metrics = metrics
        self._create_root(root_tweet)
        self._create_children(conversation_thread)

    def _create_root(self, root_tweet):
        root_id = root_tweet["id"]
        self.root = root_id
        self.tree.add_node(root_id, attributes=root_tweet)

    def _parse_tweet(self, tweet):
        return {"id": tweet["id"],
                "text": tweet["text"],
                "retweet_count": tweet["retweet_count"],
                "reply_count": tweet["reply_count"],
                "like_count": tweet["like_count"],
                "quote_count": tweet["quote_count"],
                "sentiment": tweet["sentiment"]}

    def _create_children(self, conversation_thread):
        # Loop through conversation thread
        for tweet in conversation_thread:
            tweet_id = tweet['id']
            tweet_parent = tweet['referenced_tweets'][0]
            tweet_parent_id = tweet_parent['id']

            # If parent tweet is deleted, ignore tweet
            if tweet_parent_id in self.tree:
                # Add the tweet to the tree
                parsed_tweet = self._parse_tweet(tweet)
                parsed_tweet[
                    "argumentative_type"] = TweetTreeBuilder.argumentation_relation_service.predict_argumentative_relation(
                    tweet_parent["text"], tweet["text"])
                self.tree.add_node(tweet_id, attributes=parsed_tweet)
                self.tree.add_edge(tweet_parent_id, tweet_id, color="g", weight=3)

                # Update metrics
                self.metrics.set_max_min_public_metrics(parsed_tweet)

                if tweet_parent_id == self.root:
                    self.metrics.increment_root_sentiment(parsed_tweet["sentiment"])
                else:
                    self.metrics.increment_general_sentiment(parsed_tweet["sentiment"])

    def set_tree(self, tree):
        self.tree = tree

    def add_edge(self, parent_node, child_node):
        self.tree.add_edge(parent_node, child_node, color='r', weight=3)

    def get_tree(self):
        return self.tree

    def get_root(self):
        return self.root

    def get_json(self):
        # Encode the tweet tree and metrics in JSON
        tweet_tree_json = json_graph.tree_data(self.tree, root=self.root, ident="name")
        metrics_json = self.metrics.get_metrics()

        json_representation = {"tweet_tree": tweet_tree_json, "metrics": metrics_json}

        return json_representation

    def get_tweet_tree_metrics(self):
        return self.metrics


class TweetTreeBuilder:
    """
    Service that builds the output tweet tree argumentation model. It consists of the original tweet conversation,
    as well as relevant and argumentatively related tweet conversations that are not within the original tweet
    conversation. Each node computes the sentiment, their argumentative relation to its parent, its public metrics
    and its acceptability degree if it is an argument.
    """
    keyword_extraction_service = KeywordExtractor()
    argumentation_relation_service = RelationBasedClassifierServiceBert()

    def __init__(self, tweet_id):
        load_dotenv()
        TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
        self.twitter_api_service = TwitterAPIService(TWITTER_API_KEY)
        self.tweet_tree = self._build_tweet_tree(tweet_id)

    def _build_tweet_tree(self, tweet_id):
        # Build tweet tree
        tweet = self.twitter_api_service.get_tweet(tweet_id)
        tweet["argumentative_type"] = "none"
        tweet_text = tweet["text"]
        tweet_conversation_thread = self.twitter_api_service.get_conversation_thread(tweet_id)

        # Compute metrics on root and initial tweet tree
        metrics = TweetTreeMetrics()
        tweet_tree = TweetTree(tweet, tweet_conversation_thread, metrics)
        metrics.set_root_tweet_sentiment(tweet["sentiment"])
        metrics.compute_sentiment_towards_root()

        # Build related tweet trees and append them to main tweet tree
        related_tweets = self._get_related_tweets(tweet_text)
        # related_tweets = []
        for related_tweet in related_tweets:
            related_tweet[
                "argumentative_type"] = TweetTreeBuilder.argumentation_relation_service.predict_argumentative_relation(
                tweet_text, related_tweet["text"])
            # Only retrieve 'fresh' argumentative tweets that are not replies or are retweets tweets
            if (related_tweet["argumentative_type"] != 'neutral') and ('referenced_tweets' not in related_tweet) and (
                    related_tweet['id'] != tweet['id']):
                related_tweet_thread = self.twitter_api_service.get_conversation_thread(related_tweet['id'])
                related_tweet_tree = TweetTree(related_tweet, related_tweet_thread, metrics).get_tree()
                tweet_tree.set_tree(nx.compose(tweet_tree.get_tree(), related_tweet_tree))
                tweet_tree.add_edge(tweet['id'], related_tweet['id'])
        return tweet_tree

    def _get_related_tweets(self, tweet):
        # Extract related tweets from twitter using a keyword
        keyword = TweetTreeBuilder.keyword_extraction_service.get_top_keyword(tweet)
        if keyword == "" or keyword is None:
            # No keyword extracted, don't query the API
            return []

        # Retrieve tweets that discuss the extracted keyword
        tweets_about_keyword = self.twitter_api_service.get_tweets_from_keyword(keyword)
        related_tweets = tweets_about_keyword

        return related_tweets

    def get_tweet_tree(self):
        return self.tweet_tree


if __name__ == "__main__":
    pass
