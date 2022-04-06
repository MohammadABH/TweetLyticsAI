import os
from yake import KeywordExtractor as Yake
from transformers import AutoModel, AutoTokenizer
from textblob import TextBlob
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from backend.services.utils.preprocessor import preprocess


class IKeywordExtractor:

    def get_top_keyword(self, tweet):
        """
        Abstract function that returns the top extracted keyword from a tweet.

        :param tweet:   input tweet text to extract keyword from
        :return:        extracted keyword from text
        """
        pass


class YakeKeywordExtractor(IKeywordExtractor):
    """
    Class that extracts keywords from a tweet's text using YAKE.
    """

    def __init__(self):
        self.keyword_extractor = Yake()

    def _get_keywords(self, tweet):
        """
        Computes a list of possible keywords

        :param tweet:   input tweet text to extract keywords from
        :return:        a list of all extracted keywords
        """
        keywords_with_scores = self.keyword_extractor.extract_keywords(tweet)
        keywords = list(list(zip(*keywords_with_scores))[0]) if len(keywords_with_scores) > 0 else []

        return keywords

    def get_top_keyword(self, tweet):
        """
        Function that returns the top extracted keyword from a tweet using YAKE.

        :param tweet:   input tweet text to extract keyword from
        :return:        extracted keyword from text
        """
        keywords = self._get_keywords(tweet)
        # Handle case where there are 0 potential keywords
        top_keyword = keywords[0] if len(keywords) > 0 else None

        return top_keyword


class BertKeywordExtractor(IKeywordExtractor):
    """
    Class that extracts keywords from a tweet's text using BERTweet and cosine similarities.
    Uses the same technique used in KeyBERT, but with BERTweet instead of the default BERT.

    This classes draws on the following sources:
        https://github.com/MaartenGr/KeyBERT
        https://towardsdatascience.com/keyword-extraction-with-bert-724efca412ea

    """
    dirname = os.path.dirname(__file__)
    PATH = os.path.join(dirname, '../models/vinai/bertweet-base')

    MODEL = "vinai/bertweet-base"

    # Set tokenizer normalization to true to continue tweet preprocessing
    # (normalization) according to the model's requirements
    tokenizer = AutoTokenizer.from_pretrained(MODEL, normalization=True, cache_dir=PATH)
    tokenizer.save_pretrained(PATH)  # Save tokenizer to specified path in disk to prevent re-downloading

    # Use Pytorch model instead of tensorflow due to small performance advantage
    model = AutoModel.from_pretrained(MODEL, cache_dir=PATH)
    model.save_pretrained(PATH)  # Save model to specified path in disk to prevent re-downloading

    def _get_noun_candidates(self, text, n_grams=3):
        """
        Extracts noun phrases from a text

        :param text:        text to extract noun phrases from
        :param n_grams:     minimum n-gram length of the noun phrase
        :return:            a list of noun phrases from the text that are n-grams
        """
        # Extract noun phrases using text blob
        candidates = TextBlob(text).noun_phrases

        # Filter out noun phrases that are shorter than n-grams input
        candidates_three_grams = [sentence for sentence in candidates if len(sentence.split(' ')) < n_grams]

        return candidates_three_grams

    def _get_n_grams_candidates(self, text, n_grams=3):
        """
        Extract n_grams from a text

        :param text:            text to extract the n-grams from
        :param n_grams:         n-gram length
        :return:                n-grams from the input text
        """
        # Define the n-gram range and remove english stopwords
        ngram_range = (1, n_grams)
        stop_words = "english"

        # Use count vectorizer to extract n_grams
        vectorizer = CountVectorizer(ngram_range=ngram_range, stop_words=stop_words)
        count_matrix = vectorizer.fit([text])

        # Extract n_grams from the text
        candidates = count_matrix.get_feature_names_out().tolist()

        return candidates

    def _get_candidates(self, text):
        """
        Extracts candidate keywords from an input text using noun phrases or n_grams if noun phrases fail

        :param text:    text to extract candidate keywords from
        :return:        candidate keywords that are either noun phrases or n_grams
        """
        # Extract n_grams and noun_phrases
        n_grams = 3
        n_gram_candidates = self._get_n_grams_candidates(text, n_grams)
        noun_candidates = self._get_noun_candidates(text, n_grams)

        # Return noun phrases if there are more than 0, or return n_grams
        candidates = noun_candidates if len(noun_candidates) > 0 else n_gram_candidates

        return candidates

    def _get_embeddings_from_texts(self, text_list):
        """
        Extract BERTweet embeddings from a list of text

        :param text_list:   list of text to extract embeddings from
        :return:            BERTweet embeddings of the input text
        """
        # Extract the embeddings from the pooler output layer of BERTweet
        tokens = BertKeywordExtractor.tokenizer(text_list, padding=True, return_tensors="pt")
        embeddings = BertKeywordExtractor.model(**tokens)["pooler_output"]

        # Convert it into numpy and return it
        embeddings_np = embeddings.detach().numpy()

        return embeddings_np

    def _get_keywords_from_embeddings(self, text_embedding, candidate_embeddings, candidates, keyword_number):
        """
        Extract keywords from embeddings using cosine similarities. Keyword embeddings that are closer to the
        original text's embeddings are likely to be better keywords. 'Closer' is defined using cosine distance.

        :param text_embedding:          BERTweet embeddings of original text
        :param candidate_embeddings:    BERTweet embeddings of candidate keywords
        :param candidates:              candidate keywords
        :param keyword_number:          number of keywords to extract
        :return:                        a list of keywords
        """
        # Compute cosine distance
        cosine_distance = cosine_similarity(text_embedding, candidate_embeddings)

        # Find the keywords with the shortest cosine distance adn return it
        sorted_distance_indices = cosine_distance.argsort()[0]
        keywords = [candidates[index] for index in sorted_distance_indices[-keyword_number:]]

        return keywords

    def _get_keywords(self, tweet):
        """
        Extracts keywords from an input tweet

        :param tweet:   tweet text to extract keywords from
        :return:        a list of keywords
        """
        # Pre-process the tweet and extract candidates
        pre_processed_text = preprocess(tweet)
        candidates = self._get_candidates(pre_processed_text)
        if len(candidates) == 0:
            # No possibly meaningful keyword can be extracted from the tweet, probably a tweet that doesn't make sense
            return []

        # Get the BERTweet embeddings of the candidate keywords and the original tweet text
        candidate_embeddings = self._get_embeddings_from_texts(candidates)
        text_embedding = self._get_embeddings_from_texts([pre_processed_text])

        # Extract n (n=10) number of keywords using the cosine similarities methodology
        keywords = self._get_keywords_from_embeddings(text_embedding, candidate_embeddings, candidates, 10)

        return keywords

    def get_top_keyword(self, tweet):
        """
        Function that returns the top extracted keyword from a tweet using BERTweet and cosine similarities.

        :param tweet:   input tweet text to extract keyword from
        :return:        extracted keyword from text
        """
        if tweet == "":
            return None

        # Extract potential keywords and return the best one
        keywords = self._get_keywords(tweet)
        top_keyword = keywords[0] if len(keywords) > 0 else None

        return top_keyword


class KeywordExtractor(IKeywordExtractor):
    """
    Class that extracts keywords from a tweet's text using BERTweet and cosine similarities, and falls
    back on YAKE if it fails.
    """
    bertKeywordExtractor = BertKeywordExtractor()
    yakeKeywordExtractor = YakeKeywordExtractor()

    def get_top_keyword(self, tweet):
        """
        Function that returns the top extracted keyword from a tweet using BERTweet and cosine similarities, and
        falls back on YAKE if it fails.

        :param tweet:   input tweet text to extract keyword from
        :return:        extracted keyword from text
        """
        try:
            # Extract keywords using BERTweet
            return KeywordExtractor.bertKeywordExtractor.get_top_keyword(tweet)
        except:
            # Extract keywords using YAKE if BERTweet throws an error
            return KeywordExtractor.yakeKeywordExtractor.get_top_keyword(tweet)


if __name__ == "__main__":
    pass
