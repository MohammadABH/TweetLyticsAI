from backend.services.keyword_extraction_service import YakeKeywordExtractor, BertKeywordExtractor, KeywordExtractor


class TestYakeKeywordExtractor:
    """
    Test class for YakeKeywordExtractor which extracts keywords using YAKE.
    """

    yake = YakeKeywordExtractor()

    def test_extract_top_keyword(self):
        """
        Tests the get_top_keyword function that extracts the most significant keyword from a tweet using YAKE.
        """
        tweet = "This tweet is about Machine Learning and only about Machine Learning"
        top_keyword = TestYakeKeywordExtractor.yake.get_top_keyword(tweet)
        expected_top_keyword = "Machine Learning"

        assert top_keyword == expected_top_keyword

    def test_extract_empty_top_keyword(self):
        """
        Tests the get_top_keyword function that extracts the most significant keyword from a tweet when there is
        no keyword to extract using YAKE.
        """
        tweet = ""
        top_keyword = TestYakeKeywordExtractor.yake.get_top_keyword(tweet)

        assert top_keyword is None


class TestBertKeywordExtractor:
    """
    Test class for BertKeywordExtractor which extracts keywords using BERT and cosing similarities.
    """

    bert = BertKeywordExtractor()

    def test_extract_top_keyword(self):
        """
        Tests the get_top_keyword function that extracts the most significant keyword from a tweet using BERT.
        """
        tweet = "This tweet is about Machine Learning and only about Machine Learning"
        top_keyword = TestBertKeywordExtractor.bert.get_top_keyword(tweet)
        expected_top_keyword = "machine learning"

        assert top_keyword == expected_top_keyword

    def test_extract_empty_top_keyword(self):
        """
        Tests the get_top_keyword function that extracts the most significant keyword from a tweet when there is
        no keyword to extract using BERT.
        """
        tweet = ""
        top_keyword = TestBertKeywordExtractor.bert.get_top_keyword(tweet)

        assert top_keyword is None


class TestKeywordExtractor:
    """
    Test class that tests KeywordExtractor, which extracts the top keyword from a text/tweet using BERTweet, and falls
    back on YAKE if it fails.
    """

    keyword_extractor = KeywordExtractor()

    def test_extract_keyword_yake(self, mocker):
        """
        Tests the case BERT throws an error and is unable to find a keyword.
        """
        # Mock BERT to throw an error to test the appropriate case, and spy on the function calls
        mocker.patch("backend.services.keyword_extraction_service.BertKeywordExtractor.get_top_keyword",
                     side_effect=Exception("Bert didn't work"))
        mocker.patch("backend.services.keyword_extraction_service.YakeKeywordExtractor.get_top_keyword")

        tweet = "Some random test tweet, keyword not important for this test"

        TestKeywordExtractor.keyword_extractor.get_top_keyword(tweet)

        # YAKE should have been called as BERT threw an exception
        KeywordExtractor.yakeKeywordExtractor.get_top_keyword.assert_called_once_with(tweet)

    def test_extract_keyword_bert(self, mocker):
        """
        Tests the case BERT does not throw an error and is able to find a keyword.
        """
        # Mock and spy on the function calls
        mocker.patch("backend.services.keyword_extraction_service.BertKeywordExtractor.get_top_keyword")
        mocker.patch("backend.services.keyword_extraction_service.YakeKeywordExtractor.get_top_keyword")

        tweet = "Some random test tweet, keyword not important for this test"

        TestKeywordExtractor.keyword_extractor.get_top_keyword(tweet)

        KeywordExtractor.bertKeywordExtractor.get_top_keyword.assert_called_once_with(tweet)
        # YAKE should NOT have been called as BERT threw an exception
        KeywordExtractor.yakeKeywordExtractor.get_top_keyword.assert_not_called()

