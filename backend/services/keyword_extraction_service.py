import os
from interface import implements, Interface
from yake import KeywordExtractor as Yake
from transformers import AutoModel, AutoTokenizer
from textblob import TextBlob
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from backend.services.utils.preprocessor import preprocess


class IKeywordExtractor(Interface):

    def get_keywords(self, tweet):
        pass

    def get_top_keyword(self, tweet):
        pass


class YakeKeywordExtractor(implements(IKeywordExtractor)):

    def __init__(self):
        self.keyword_extractor = Yake()

    def get_keywords(self, tweet):
        keywords_with_scores = self.keyword_extractor.extract_keywords(tweet)
        keywords = list(list(zip(*keywords_with_scores))[0]) if len(keywords_with_scores) > 0 else []

        return keywords

    def get_top_keyword(self, tweet):
        keywords = self.get_keywords(tweet)
        top_keyword = keywords[0] if len(keywords) > 0 else None

        return top_keyword


class BertKeywordExtractor(implements(IKeywordExtractor)):
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

    def get_noun_candidates(self, text, n_grams=3):
        candidates = TextBlob(text).noun_phrases
        candidates_three_grams = [sentence for sentence in candidates if len(sentence.split(' ')) < n_grams]
        return candidates_three_grams

    def get_n_grams_candidates(self, text, n_grams=3):
        ngram_range = (1, n_grams)
        stop_words = "english"

        vectorizer = CountVectorizer(ngram_range=ngram_range, stop_words=stop_words)
        count_matrix = vectorizer.fit([text])

        candidates = count_matrix.get_feature_names_out().tolist()

        return candidates

    def get_candidates(self, text):
        n_grams = 3
        n_gram_candidates = self.get_n_grams_candidates(text, n_grams)
        noun_candidates = self.get_noun_candidates(text, n_grams)

        candidates = noun_candidates if len(noun_candidates) > 0 else n_gram_candidates

        return candidates

    def get_embeddings_from_texts(self, text_list):
        tokens = BertKeywordExtractor.tokenizer(text_list, padding=True, return_tensors="pt")
        embeddings = BertKeywordExtractor.model(**tokens)["pooler_output"]
        embeddings_np = embeddings.detach().numpy()

        return embeddings_np

    def get_keywords_from_embeddings(self, text_embedding, candidate_embeddings, candidates, keyword_number):
        cosine_distance = cosine_similarity(text_embedding, candidate_embeddings)
        sorted_distance_indices = cosine_distance.argsort()[0]
        keywords = [candidates[index] for index in sorted_distance_indices[-keyword_number:]]

        return keywords

    def get_keywords(self, tweet):
        pre_processed_text = preprocess(tweet)
        candidates = self.get_candidates(pre_processed_text)
        if len(candidates) == 0:
            # No possibly meaningful keyword can be extracted from the tweet, probably a tweet that doesn't make sense
            return []

        candidate_embeddings = self.get_embeddings_from_texts(candidates)
        text_embedding = self.get_embeddings_from_texts([pre_processed_text])

        keywords = self.get_keywords_from_embeddings(text_embedding, candidate_embeddings, candidates, 10)

        return keywords

    def get_top_keyword(self, tweet):
        if tweet == "":
            return None

        keywords = self.get_keywords(tweet)
        top_keyword = keywords[0] if len(keywords) > 0 else None

        return top_keyword


class KeywordExtractor(implements(IKeywordExtractor)):
    bertKeywordExtractor = BertKeywordExtractor()
    yakeKeywordExtractor = YakeKeywordExtractor()

    def get_keywords(self, tweet):
        try:
            return KeywordExtractor.bertKeywordExtractor.get_keywords(tweet)
        except:
            return KeywordExtractor.yakeKeywordExtractor.get_keywords(tweet)

    def get_top_keyword(self, tweet):
        try:
            return KeywordExtractor.bertKeywordExtractor.get_top_keyword(tweet)
        except:
            return KeywordExtractor.yakeKeywordExtractor.get_top_keyword(tweet)

# tweet = "chocolate cake perfection https://t.co/a6XHwgLy5a"
# yake_keyword_extractor = YakeKeywordExtractor()
# print(yake_keyword_extractor.get_keywords(tweet))

# keyword_extractor = BertKeywordExtractor()
# print(keyword_extractor.get_top_keyword(tweet))
# print(keyword_extractor.get_keywords(tweet))
