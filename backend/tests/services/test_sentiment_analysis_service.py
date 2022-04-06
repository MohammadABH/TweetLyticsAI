from backend.services.sentiment_analysis_service import VaderSentimentAnalysis, BertweetSentimentAnalysis, SentimentAnalysis


class TestVaderSentimentAnalysis:
    """
    Test class that tests VaderSentimentAnalysis, which extracts sentiment from a text/tweet using VADER.
    """
    vader = VaderSentimentAnalysis()  # Store as class variable to prevent re-constructing it each time

    def test_predict_sentiment_negative(self):
        """
        Tests the case in which VADER classifies a tweet as negative sentiment.
        """
        tweet = "I hate this random topic, its super annoying and frustrating"
        sentiment = TestVaderSentimentAnalysis.vader.predict_sentiment(tweet)
        expected_sentiment = "negative"

        assert sentiment == expected_sentiment

    def test_predict_sentiment_positive(self):
        """
        Tests the case in which VADER classifies a tweet as positive sentiment.
        """
        tweet = "I love this random topic, its super interesting and lovely"
        sentiment = TestVaderSentimentAnalysis.vader.predict_sentiment(tweet)
        expected_sentiment = "positive"

        assert sentiment == expected_sentiment

    def test_predict_sentiment_neutral(self):
        """
        Tests the case in which VADER classifies a tweet as neutral sentiment.
        """
        tweet = "This is a neutral tweet"
        sentiment = TestVaderSentimentAnalysis.vader.predict_sentiment(tweet)
        expected_sentiment = "neutral"

        assert sentiment == expected_sentiment


class TestBertSentimentAnalysis:
    """
    Test class that tests BertSentimentAnalysis, which extracts sentiment from a text/tweet using BERTweet.
    """
    bert = BertweetSentimentAnalysis()

    def test_predict_sentiment_negative(self):
        """
        Tests the case in which VADER classifies a tweet as negative sentiment.
        """
        tweet = "I hate this random topic, its super annoying and frustrating"
        sentiment = TestBertSentimentAnalysis.bert.predict_sentiment(tweet)
        expected_sentiment = "negative"

        assert sentiment == expected_sentiment

    def test_predict_sentiment_positive(self):
        """
        Tests the case in which VADER classifies a tweet as positive sentiment.
        """
        tweet = "I love this random topic, its super interesting and lovely"
        sentiment = TestBertSentimentAnalysis.bert.predict_sentiment(tweet)
        expected_sentiment = "positive"

        assert sentiment == expected_sentiment

    def test_predict_sentiment_neutral(self):
        """
        Tests the case in which VADER classifies a tweet as neutral sentiment.
        """
        tweet = "This is a neutral tweet"
        sentiment = TestBertSentimentAnalysis.bert.predict_sentiment(tweet)
        expected_sentiment = "neutral"

        assert sentiment == expected_sentiment


class TestSentimentAnalysis:
    """
    Test class that tests SentimentAnalysis, which extracts sentiment from a text/tweet using BERTweet, and falls
    back on VADER if it fails.
    """
    sentiment_analyzer = SentimentAnalysis()

    def test_predict_sentiment_vader(self, mocker):
        """
        Tests the case BERT throws an error and is unable to classify the input.
        """
        # Mock BERT to throw an error to test the appropriate case, and spy on the function calls
        mocker.patch("backend.services.sentiment_analysis_service.BertweetSentimentAnalysis.predict_sentiment",
                     side_effect=Exception("Bert didn't work"))
        mocker.patch("backend.services.sentiment_analysis_service.VaderSentimentAnalysis.predict_sentiment")

        tweet = "Some random test tweet, sentiment not important for this test"

        TestSentimentAnalysis.sentiment_analyzer.predict_sentiment(tweet)

        # Vader should have been called as BERT threw an exception
        SentimentAnalysis.vaderSentimentAnalysis.predict_sentiment.assert_called_once_with(tweet)

    def test_predict_sentiment_bert(self, mocker):
        """
        Tests the case BERT does not throw an error and is able to classify the input.
        """
        # Mock and spy on the function calls
        mocker.patch("backend.services.sentiment_analysis_service.BertweetSentimentAnalysis.predict_sentiment")
        mocker.patch("backend.services.sentiment_analysis_service.VaderSentimentAnalysis.predict_sentiment")

        tweet = "Some random test tweet, sentiment not important for this test"

        TestSentimentAnalysis.sentiment_analyzer.predict_sentiment(tweet)

        SentimentAnalysis.bertSentimentAnalysis.predict_sentiment.assert_called_once_with(tweet)
        # Vader should NOT have been called as BERT threw an exception
        SentimentAnalysis.vaderSentimentAnalysis.predict_sentiment.assert_not_called()
