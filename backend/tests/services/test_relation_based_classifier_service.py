from backend.services.relation_based_classifier_service import RelationBasedClassifierServiceBert


class TestBertRelationClassification:
    """
    Test class for RelationBasedClassifierServiceBert that classifies the argumentative relation between 2 tweets.
    """
    # Store as class variable to prevent computationally re-constructing it each time
    bert = RelationBasedClassifierServiceBert()

    def test_support_argument_relation(self):
        """
        Tests the case in which BERT classifies a tweet as a support relation.
        """
        parent_tweet = "Python is probably the best programming language ever"
        child_tweet = "I have to agree! Its super simple"

        argumentative_relation_type = TestBertRelationClassification.bert.predict_argumentative_relation(parent_tweet,
                                                                                                         child_tweet)
        expected_argumentative_relation_type = "support"
        assert argumentative_relation_type == expected_argumentative_relation_type

    def test_attack_argument_relation(self):
        """
        Tests the case in which BERT classifies a tweet as an attack relation.
        """
        parent_tweet = "Python is probably the best programming language ever"
        child_tweet = "I have to disagree! Its very slow in comparison to C++"

        argumentative_relation_type = TestBertRelationClassification.bert.predict_argumentative_relation(parent_tweet,
                                                                                                         child_tweet)
        expected_argumentative_relation_type = "attack"

        assert argumentative_relation_type == expected_argumentative_relation_type

    def test_neutral_argument_relation(self):
        """
        Tests the case in which BERT classifies a tweet as a neutral relation.
        """
        parent_tweet = "Python is probably the best programming language ever"
        child_tweet = "Hmm, I'm not sure really"

        argumentative_relation_type = TestBertRelationClassification.bert.predict_argumentative_relation(parent_tweet,
                                                                                                         child_tweet)
        expected_argumentative_relation_type = "neutral"

        assert argumentative_relation_type == expected_argumentative_relation_type

