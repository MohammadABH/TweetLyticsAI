import networkx as nx
from networkx.readwrite import json_graph
import json
from twitter_api_service import TwitterAPIService
from keyword_extraction_service import YakeKeywordExtractor
import matplotlib.pyplot as plt


class TweetTree:

    def __init__(self, root_tweet, conversation_thread):
        self.tree = nx.DiGraph()
        self.root = None
        self._create_root(root_tweet)
        self._create_children(conversation_thread)

    def _create_root(self, root_tweet):
        root_id = root_tweet['id']
        self.root = root_id
        print(f"init root = {root_id}")
        self.tree.add_node(root_id, data=root_tweet)

    def _create_children(self, conversation_thread):
        for tweet in conversation_thread:
            tweet_id = tweet['id']
            tweet_parent_id = tweet['referenced_tweets'][0]['id']
            # If parent tweet is deleted, ignore tweet
            if tweet_parent_id in self.tree:
                self.tree.add_node(tweet_id, data=tweet)
                self.tree.add_edge(tweet_parent_id, tweet_id, color="g", weight=3)

    def set_tree(self, tree):
        self.tree = tree

    def add_edge(self, parent_node, child_node):
        self.tree.add_edge(parent_node, child_node, color='r', weight=3)

    def get_tree(self):
        return self.tree

    def get_root(self):
        return self.root

    def get_json(self):
        json_representation = json_graph.tree_data(self.tree, root=self.root)

        return json_representation


class TweetTreeBuilder:
    keyword_extraction_service = YakeKeywordExtractor()

    def __init__(self, tweet_id):
        self.twitter_api_service = TwitterAPIService(
            "AAAAAAAAAAAAAAAAAAAAAERfVAEAAAAA0rjC0YSarrfSEE88Ar2CF5I2RYs%3DkVWG3XwyVVx2zFcu4ISP32Gu9ajF3k7EK8iNOOkSuG1EQQunUB")
        self.tweet_tree = self._build_tweet_tree(tweet_id)

    def _build_tweet_tree(self, tweet_id):
        # Build tweet tree
        tweet = self.twitter_api_service.get_tweet(tweet_id)
        tweet_text = tweet["text"]
        tweet_conversation_thread = self.twitter_api_service.get_conversation_thread(tweet_id)
        tweet_tree = TweetTree(tweet, tweet_conversation_thread)

        # Build related tweet trees and append them to main tweet tree
        related_tweets = self._get_related_tweets(tweet_text)
        for related_tweet in related_tweets:
            # Only retrieve 'fresh' tweets that are not replies or are retweets tweets
            if 'referenced_tweets' not in related_tweet and related_tweet['id'] != tweet['id']:
                related_tweet_thread = self.twitter_api_service.get_conversation_thread(related_tweet['id'])
                related_tweet_tree = TweetTree(related_tweet, related_tweet_thread).get_tree()
                tweet_tree.set_tree(nx.compose(tweet_tree.get_tree(), related_tweet_tree))
                tweet_tree.add_edge(tweet['id'], related_tweet['id'])

        return tweet_tree

    def _get_related_tweets(self, tweet):
        keyword = TweetTreeBuilder.keyword_extraction_service.get_top_keyword(tweet)
        tweets_about_keyword = self.twitter_api_service.get_tweets_from_keyword(keyword)
        related_tweets = tweets_about_keyword  # TODO: check argumentative relation

        return related_tweets

    def get_tweet_tree(self):
        return self.tweet_tree


tweet_tree = TweetTreeBuilder(1496855592027275273).get_tweet_tree()
root = tweet_tree.get_root()
data = tweet_tree.get_json()
# print(f"Root = {root}")
data = json_graph.tree_data(tweet_tree.get_tree(), root=tweet_tree.get_root())
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# s = json.dumps(data)
# print(s)
# tweet_tree = tweet_tree.get_tree()
# pos = nx.spring_layout(tweet_tree, k=0.05)
# edges = tweet_tree.edges()
# colors = [tweet_tree[u][v]['color'] for u,v in edges]
# weights = [tweet_tree[u][v]['weight'] for u,v in edges]
#
# plt.figure(figsize = (20,20))
# nx.draw(tweet_tree, pos=pos, cmap=plt.cm.PiYG, edge_color=colors, width=weights, linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
# nx.draw_networkx_nodes(tweet_tree, pos=pos, node_size=300)
# plt.show()
# text = "chocolate"
# api = TwitterAPIService(
#             "AAAAAAAAAAAAAAAAAAAAAERfVAEAAAAA0rjC0YSarrfSEE88Ar2CF5I2RYs%3DkVWG3XwyVVx2zFcu4ISP32Gu9ajF3k7EK8iNOOkSuG1EQQunUB")
# print(len(api.get_tweets_from_keyword(text)))
