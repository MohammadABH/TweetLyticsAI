from networkx import DiGraph
from backend.services.argumentation_service import ArgumentationAlgorithmService
from backend.services.tweet_tree_builder_service import TweetTreeMetrics


class TestArgumentationAlgorithmService:
    """
    Test class the tests the ArgumentationAlgorithmService that uses the Ebs argumentation semantics.
    """

    def test_acceptability_degree(self):
        """
        Tests the acceptability_degree function that determines the acceptability degree/strength of an argument
        """
        # Create a tweet tree with 4 nodes and metrics object
        graph = DiGraph()
        metrics = TweetTreeMetrics()

        node_0 = {
            "id": 0,
            "like_count": 0.1,
            "retweet_count": 0,
            "argumentative_type": "none"
        }

        node_1 = {
            "id": 1,
            "like_count": 0.9,
            "retweet_count": 0,
            "argumentative_type": "support"
        }

        node_2 = {
            "id": 2,
            "like_count": 0.95,
            "retweet_count": 0,
            "argumentative_type": "attack"
        }

        node_3 = {
            "id": 3,
            "like_count": 0.8,
            "retweet_count": 0,
            "argumentative_type": "attack"
        }

        # Add the nodes to the graph
        graph.add_node(0, attributes=node_0)
        graph.add_node(1, attributes=node_1)
        graph.add_node(2, attributes=node_2)
        graph.add_node(3, attributes=node_3)

        # Add edges between nodes in the graph
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(0, 3)

        # Compute the acceptability degree
        argumentation_model = ArgumentationAlgorithmService(1, 0, graph, metrics)
        acceptability_degree = argumentation_model.acceptability_degree(graph.nodes[0])

        # This is because the computation is as follows:
        # Base strength of node_0 = 0.5
        # Base strength of node_1 = 0.9
        # Base strength of node_2 = 0.95
        # Base strength of node_3 = 0.8
        # Attackers score = 0.95 + 0.8 = 1.75
        # Supporters score = 0.9
        # Strength child = 0.9 - 1.75 = -0.85
        # Final score = 1 - ((1 - 0.5^2) / (1 + (0.5 * (2 ^ -0.85)))) = 0.41286638406
        # Also allow some error for the + 0.000001 constant to avoid division by 0
        assert round(acceptability_degree, 3) == 0.413

    def test_acceptability_degree_non_argument(self):
        """
        Tests the acceptability degree of a non-argument
        """
        # A tweet that is "neutral" is a non argument
        tweet = {"attributes": {"argumentative_type": "neutral"}}
        argumentation_model = ArgumentationAlgorithmService(1, 0, None, None)
        acceptability_degree = argumentation_model.acceptability_degree(tweet)
        expected_acceptability_degree = 0.0  # Should have a strength of 0.0 as it is not an argument

        assert acceptability_degree == expected_acceptability_degree

    def test_acceptability_degree_invalid_tweet(self):
        """
        Tests the acceptability degree when a node is None (edge case)
        """
        tweet = None
        argumentation_model = ArgumentationAlgorithmService(1, 0, None, None)
        acceptability_degree = argumentation_model.acceptability_degree(tweet)
        expected_acceptability_degree = 0.0  # None should have a strength of 0.0, as it is nothing

        assert acceptability_degree == expected_acceptability_degree

