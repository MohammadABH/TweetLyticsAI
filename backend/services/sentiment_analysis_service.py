import os
from interface import implements, Interface
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize, download
from backend.services.utils.preprocessor_util import preprocess
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline

download('punkt')


class ISentimentAnalysis(Interface):

    def predict_sentiment(self, tweet):
        """
        Abstract function that returns the sentiment label of an input Tweet.
        The implementation/way in which the sentiment is extracted is determined
        by the subclass.

        :param tweet:   the input tweet to predict the sentiment label for

        :return:        sentiment label (one of [positive, neutral, negative])
        """
        pass


class VaderSentimentAnalysis(implements(ISentimentAnalysis)):
    # Vader sentiment analysis object
    vader_analyzer = SentimentIntensityAnalyzer()

    def _get_sentiment_label(self, sentiment_score):
        """
        Function that gets the sentiment label [positive, neutral, negative]
        of a sentiment compound score from Vader

        :param sentiment_score: sentiment compound score of a text

        :return       sentiment label (one of [positive, neutral, negative]) based
                      on the input compound score from vader
        """
        if sentiment_score >= 0.05:
            return 'positive'
        elif sentiment_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'

    def predict_sentiment(self, tweet):
        """
        Function that predicts the sentiment label of an input tweet using Vader

        :param tweet:   the input tweet to predict the sentiment label for

        :return         sentiment label of a given tweet
        """

        preprocessed_tweet = preprocess(tweet)

        # According to the Vader documentation (https://github.com/cjhutto/vaderSentiment/blob/d8da3e21374a57201b557a4c91ac4dc411a08fed/vaderSentiment/vaderSentiment.py#L600)
        # it works best when sentiment analysis is done at a sentence level and
        # not on a whole paragraph. So the tweet sentiment is calculated as the
        # average sentiment of each sentence in the tweet

        sentences = tokenize.sent_tokenize(preprocessed_tweet)  # Break tweet up into sentences
        overall_tweet_sentiment = 0.0
        for sentence in sentences:
            sentence_sentiment = VaderSentimentAnalysis.vader_analyzer.polarity_scores(sentence)

            # Use compound score as Vader documentation says it's the most accurate
            # https://github.com/cjhutto/vaderSentiment
            overall_tweet_sentiment += sentence_sentiment['compound']

        # Get average sentiment across each sentence in the tweet
        overall_tweet_sentiment = round(overall_tweet_sentiment / len(sentences), 4)

        # return the sentiment label and not the score
        return self._get_sentiment_label(overall_tweet_sentiment)


class BertweetSentimentAnalysis(implements(ISentimentAnalysis)):
    dirname = os.path.dirname(__file__)
    PATH = os.path.join(dirname, '../models/sentiment-analysis')

    MODEL = "cardiffnlp/bertweet-base-sentiment"

    # Set tokenizer normalization to true to continue tweet preprocessing
    # (normalization) according to the model's requirements
    tokenizer = AutoTokenizer.from_pretrained(MODEL, normalization=True, cache_dir=PATH)
    tokenizer.save_pretrained(PATH)  # Save tokenizer to specified path in disk to prevent re-downloading

    # Dictionaries that map labels to model output ids and vice versa
    # to have more readable prediction outputs
    id2label = {0: "negative", 1: "neutral", 2: "positive"}
    label2id = {"negative": 0, "neutral": 1, "positive": 2}

    # Use Pytorch model instead of tensorflow due to small performance advantage
    model = AutoModelForSequenceClassification.from_pretrained(MODEL, id2label=id2label, label2id=label2id,
                                                               cache_dir=PATH)
    model.save_pretrained(PATH)  # Save model to specified path in disk to prevent re-downloading

    def predict_sentiment(self, tweet):
        """
        Function that predicts the sentiment label of an input tweet using BERTweet

        :param tweet: the input tweet to predict the sentiment label for

        :return       sentiment label of a given tweet
        """

        pipe = TextClassificationPipeline(model=BertweetSentimentAnalysis.model,
                                          tokenizer=BertweetSentimentAnalysis.tokenizer, return_all_scores=False)
        classification_output = pipe(tweet)
        best_prediction = classification_output[0]
        classification_score = best_prediction['score']
        classification_label = best_prediction['label']

        return classification_label


class SentimentAnalysis(implements(ISentimentAnalysis)):

    bertSentimentAnalysis = BertweetSentimentAnalysis()
    vaderSentimentAnalysis = VaderSentimentAnalysis()

    def predict_sentiment(self, tweet):
        """
        Function that predicts the sentiment label of an input tweet. It attempts to use BERTweet, if it fails,
        it uses VADER.

        :param tweet:   the input tweet to predict the sentiment label for

        :return         sentiment label of a given tweet
        """
        try:
            return SentimentAnalysis.bertSentimentAnalysis.predict_sentiment(tweet)
        except:
            return SentimentAnalysis.vaderSentimentAnalysis.predict_sentiment(tweet)

# text = "I love you"
# bertweet_sentiment = BertweetSentimentAnalysis()
# vader = VaderSentimentAnalysis()
# print(vader.predict_sentiment((text)))
# print(bertweet_sentiment.predict_sentiment(text))
