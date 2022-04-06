from backend.services.utils.preprocessor import preprocess


class TestPreprocessor:
    """
    Test class that tests the text pre-processor used throughout the application
    """

    def test_pre_processing(self):
        """
        Tests that both twitter handles and links are replaced
        """
        tweet = "here is a link https://www.youtube.com/ and user @twitter"
        processed_tweet = preprocess(tweet)

        # HTTP link and twitter user handle have been removed
        expected_result = "here is a link http and user @user"


        assert expected_result == processed_tweet

    def test_http_pre_processing(self):
        """
        Tests that links are replaced from a given text
        """
        tweet = "here is a link https://www.youtube.com/"
        processed_tweet = preprocess(tweet)

        # HTTP link removed
        expected_result = "here is a link http"

        assert expected_result == processed_tweet

    def test_user_pre_processing(self):
        """
        Tests that user handles are replaced from a given text
        """
        tweet = "here is a user @twitter"
        processed_tweet = preprocess(tweet)

        # Twitter handle removed
        expected_result = "here is a user @user"

        assert expected_result == processed_tweet

