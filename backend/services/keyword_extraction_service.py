import os
from yake import KeywordExtractor
from transformers import AutoModel, AutoTokenizer
from textblob import TextBlob
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocessor_util import preprocess


class YakeKeywordExtractor:

    def __init__(self):
        self.keyword_extractor = KeywordExtractor()

    def get_keywords(self, tweet):
        keywords_with_scores = self.keyword_extractor.extract_keywords(tweet)
        keywords = list(list(zip(*keywords_with_scores))[0])

        return keywords

    def get_top_keyword(self, tweet):
        keywords = self.get_keywords(tweet)
        top_keyword = keywords[0]

        return top_keyword


class BertKeywordExtractor:
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

    def get_candidates(self, text):
        candidates = TextBlob(text).noun_phrases
        candidates_three_grams = [sentence for sentence in candidates if len(sentence.split(' ')) < 3]
        return candidates_three_grams

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

    def get_keywords(self, text):
        pre_processed_text = preprocess(text)
        candidates = self.get_candidates(pre_processed_text)

        candidate_embeddings = self.get_embeddings_from_texts(candidates)
        text_embedding = self.get_embeddings_from_texts([pre_processed_text])

        keywords = self.get_keywords_from_embeddings(text_embedding, candidate_embeddings, candidates, 10)

        return keywords

    def get_top_keyword(self, text):
        keywords = self.get_keywords(text)
        top_keyword = keywords[0]

        return top_keyword


# tweet = "chocolate cake perfection https://t.co/a6XHwgLy5a"
# yake_keyword_extractor = YakeKeywordExtractor()
# print(yake_keyword_extractor.get_keywords(tweet))

# keyword_extractor = BertKeywordExtractor()
# print(keyword_extractor.get_keywords(tweet))
