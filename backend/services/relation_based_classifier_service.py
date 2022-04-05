import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline


class IRelationBasedClassifierService:

    def predict_argumentative_relation(self, text_a, text_b):
        """
        Abstract function that predicts the argumentative relationship between a tweet and its parent as one
        of {support, attack, neutral}.

        :param text_a:      parent node tweet
        :param text_b:      child node tweet
        :return:            argumentative relation between child and parent tweets
        """
        pass


class RelationBasedClassifierServiceBert(IRelationBasedClassifierService):
    """
    Service that extracts the argumentative relation between a tweet and its parent as one of
    {support, attack, neutral}. It uses a custom fine-tuned Twitter RoBERTa model.
    """
    dirname = os.path.dirname(__file__)
    PATH = os.path.join(dirname, "../models/rbam_twitter")

    MODEL = "MohammadABH/twitter-roberta-base-dec2021_rbam_fine_tuned"

    # Set tokenizer normalization to true to continue tweet preprocessing
    # (normalization) according to the model's requirements
    tokenizer = AutoTokenizer.from_pretrained(MODEL, normalization=True, cache_dir=PATH)
    tokenizer.save_pretrained(PATH)  # Save tokenizer to specified path in disk to prevent re-downloading

    # Use Pytorch model instead of tensorflow due to small performance advantage
    model = AutoModelForSequenceClassification.from_pretrained(MODEL, cache_dir=PATH)
    model.save_pretrained(PATH)  # Save model to specified path in disk to prevent re-downloading

    SEPARATOR_TOKEN = "</s> </s>"  # BERT special separator token

    def predict_argumentative_relation(self, text_a, text_b):
        """
        Function that predicts the argumentative relationship between a tweet and its parent as one
        of {support, attack, neutral} using a custom fine-tuned Twitter RoBERTa model.

        :param text_a:      parent node tweet
        :param text_b:      child node tweet
        :return:            argumentative relation between child and parent tweets
        """
        # Tokenizing parameters, truncate, apdd and max length of 512
        tokenizer_kwargs = {'padding': True, 'truncation': True, 'max_length': 512}

        # Use a pipeline to simplify classification
        pipe = TextClassificationPipeline(model=RelationBasedClassifierServiceBert.model,
                                          tokenizer=RelationBasedClassifierServiceBert.tokenizer,
                                          return_all_scores=False)

        # Classify the relation between the two tweets, add a BERT special seperator token between the texts
        classification_output = pipe(f"{text_a} {RelationBasedClassifierServiceBert.SEPARATOR_TOKEN} {text_b}",
                                     **tokenizer_kwargs)

        # Extract the best prediction and return the label
        best_prediction = classification_output[0]
        classification_score = best_prediction['score']
        classification_label = best_prediction['label']

        return classification_label
