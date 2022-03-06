import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline


class RelationBasedClassifierService:
    dirname = os.path.dirname(__file__)
    PATH = os.path.join(dirname, "../models/rbam")

    MODEL = "MohammadABH/bertweet-finetuned-rbam"

    # Set tokenizer normalization to true to continue tweet preprocessing
    # (normalization) according to the model's requirements
    tokenizer = AutoTokenizer.from_pretrained(MODEL, normalization=True, cache_dir=PATH)
    tokenizer.save_pretrained(PATH)  # Save tokenizer to specified path in disk to prevent re-downloading

    # Use Pytorch model instead of tensorflow due to small performance advantage
    model = AutoModelForSequenceClassification.from_pretrained(MODEL, cache_dir=PATH)
    model.save_pretrained(PATH)  # Save model to specified path in disk to prevent re-downloading

    SEPARATOR_TOKEN = "</s> </s>"

    def predict_argumentative_relation(self, text_a, text_b):
        tokenizer_kwargs = {'padding': True, 'truncation': True, 'max_length': 128}
        pipe = TextClassificationPipeline(model=RelationBasedClassifierService.model,
                                          tokenizer=RelationBasedClassifierService.tokenizer,
                                          return_all_scores=False)
        classification_output = pipe(f"{text_a} {RelationBasedClassifierService.SEPARATOR_TOKEN} {text_b}", **tokenizer_kwargs)
        best_prediction = classification_output[0]
        classification_score = best_prediction['score']
        classification_label = best_prediction['label']

        return classification_label


# r = RelationBasedClassifierService()
# print(r.predict_argumentative_relation("i think python is really good", "on what basis are you saying its good?"))
