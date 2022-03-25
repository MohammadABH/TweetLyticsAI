import os
import sys
import dill
import pandas as pd
import numpy as np
from nltk import download, word_tokenize, corpus, WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse as sp
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, PredefinedSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


download('stopwords')
download('punkt')
download('wordnet')
download('omw-1.4')

os.chdir(os.path.dirname(__file__))


class RandomForestRBAM:
    PATH = '../datasets/dataset.csv'

    def __init__(self):
        self.df = self.get_dataset()

        self.X, self.y, self.X_train, self.y_train, self.X_valid, self.y_valid, self.X_test, self.y_test = self.get_split_dataset()

        self.split_index = self.get_split_index()
        self.ps = PredefinedSplit(test_fold=self.split_index)

    def get_dataset(self):
        df = pd.read_csv(RandomForestRBAM.PATH)
        df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)

        return df

    def preprocess(self, text):
        preprocessed_text = []
        original_text_words = text.split(" ")
        for word in original_text_words:
            word = 'http' if text.startswith('http') else word  # Preprocess links
            word = '@user' if text.startswith('@') and len(word) > 1 else word  # Preprocess user handles
            preprocessed_text.append(word)
        return " ".join(preprocessed_text)

    def clean(self, text):
        processed_text = self.preprocess(text)
        tokenized_text = word_tokenize(processed_text)
        lowercased_text = [word.lower() for word in tokenized_text]

        stopwords = corpus.stopwords.words('english')
        no_stopwords = [word for word in lowercased_text if word not in stopwords]
        no_alpha = [word for word in no_stopwords if word.isalpha()]

        wordnet_lemmatizer = WordNetLemmatizer()
        lemma_text = [wordnet_lemmatizer.lemmatize(word) for word in no_alpha]

        cleaned_text = lemma_text

        return cleaned_text

    def get_split_dataset(self):
        train_size = 0.8
        test_size = 0.5

        tfidf_vectorizer = TfidfVectorizer(analyzer=self.clean)
        tfidf_vectorizer.fit(pd.concat((self.df['text_a'], self.df['text_b'])).unique())
        with open('../../backend/models/rf-rbam/tfidf_vectorizer.pkl', 'wb') as f:
            dill.dump(tfidf_vectorizer, f)

        train_a_trans = tfidf_vectorizer.transform(self.df['text_a'].values)
        train_b_trans = tfidf_vectorizer.transform(self.df['text_b'].values)

        X = sp.hstack((train_a_trans, train_b_trans))
        y = self.df[['labels']]

        X_train, X_rem, y_train, y_rem = train_test_split(X, y, train_size=train_size, random_state=42)

        X_valid, X_test, y_valid, y_test = train_test_split(X_rem, y_rem, test_size=test_size, random_state=42)

        return X, y, X_train, y_train, X_valid, y_valid, X_test, y_test

    def get_split_index(self):
        X_index = self.df[['text_a', 'text_b']]
        y_index = self.df[['labels']]

        train_size = 0.8
        test_size = 0.5

        X_train_index, X_rem_index, y_train_index, y_rem_index = train_test_split(X_index, y_index,
                                                                                  train_size=train_size,
                                                                                  random_state=42)

        X_valid_index, X_test_index, y_valid_index, y_test_index = train_test_split(X_rem_index, y_rem_index,
                                                                                    test_size=test_size,
                                                                                    random_state=42)

        split_index = [-1 if (x in X_train_index.index) or (x in X_test_index.index) else 0 for x in X_index.index]

        return split_index

    def print_results(self, results):
        print(f'BEST PARAMS: {results.best_params_}\n')

        f1s = results.cv_results_['mean_test_f1_weighted']
        accuracies = results.cv_results_['mean_test_accuracy']
        recalls = results.cv_results_['mean_test_recall_weighted']
        precisions = results.cv_results_['mean_test_precision_weighted']

        for f1, accuracy, recall, precision, params in zip(f1s, accuracies, recalls, precisions,
                                                           results.cv_results_['params']):
            print(
                f'A: {round(accuracy, 3)} / R: {round(recall, 3)} / P: {round(precision, 3)} / F1: {round(f1, 3)}, {params}')

    def evaluate_model(self, model):
        y_pred = model.predict(self.X_test)

        accuracy = round(accuracy_score(self.y_test, y_pred), 3)
        precision = round(precision_score(self.y_test, y_pred, average='weighted'), 3)
        recall = round(recall_score(self.y_test, y_pred, average='weighted'), 3)
        f1 = round(f1_score(self.y_test, y_pred, average='weighted'), 3)

        print(
            f'MAX DEPTH: {model.max_depth} / # OF EST: {model.n_estimators} -- A: {accuracy} / P: {precision} / R: {recall} / F1: {f1}')

    def grid_search_tuning(self):
        rf = RandomForestClassifier(class_weight='balanced')
        parameters = {
            'n_estimators': [5, 50, 100],
            'max_depth': [2, 10, 20, None],
        }

        rf_grid_search = GridSearchCV(estimator=rf, param_grid=parameters,
                                      scoring=['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted'],
                                      cv=self.ps, refit='f1_weighted', error_score="raise")
        rf_grid_search.fit(self.X, self.y.values.ravel())

        self.print_results(rf_grid_search)

    def best_param_grid_search(self):
        best_rf_grid = RandomForestClassifier(n_estimators=100, max_depth=None, class_weight='balanced')
        best_rf_grid.fit(self.X_train, self.y_train.values.ravel())

        self.evaluate_model(best_rf_grid)

        return best_rf_grid

    def random_search_tuning(self):
        # Number of trees in random forest
        n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]
        # Number of features to consider at every split
        max_features = ['auto', 'sqrt']
        # Maximum number of levels in tree
        max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
        max_depth.append(None)
        # Minimum number of samples required to split a node
        min_samples_split = [2, 5, 10]
        # Minimum number of samples required at each leaf node
        min_samples_leaf = [1, 2, 4]
        # Method of selecting samples for training each tree
        bootstrap = [True, False]
        # Create the random grid
        random_grid = {'n_estimators': n_estimators,
                       'max_features': max_features,
                       'max_depth': max_depth,
                       'min_samples_split': min_samples_split,
                       'min_samples_leaf': min_samples_leaf,
                       'bootstrap': bootstrap}

        # Use the random grid to search for best hyperparameters
        # First create the base model to tune
        rf = RandomForestClassifier(class_weight='balanced')
        # Random search of parameters, using 3 fold cross validation,
        # search across 100 different combinations, and use all available cores
        rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=100,
                                       scoring=['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted'],
                                       cv=self.ps, refit='f1_weighted', verbose=2, random_state=42, n_jobs=-1,
                                       error_score='raise')
        # Fit the random search model
        rf_random.fit(self.X, self.y.values.ravel())

        self.print_results(rf_random)

    def best_param_random_search(self):
        best_rf_random = RandomForestClassifier(n_estimators=1000, min_samples_split=2, min_samples_leaf=1,
                                                max_features='sqrt', max_depth=110, bootstrap=True,
                                                class_weight='balanced')
        best_rf_random.fit(self.X_train, self.y_train.values.ravel())

        self.evaluate_model(best_rf_random)

        return best_rf_random


if __name__ == "__main__":
    rf_trainer = RandomForestRBAM()

    arguments = sys.argv[1:]

    if len(arguments) == 0:
        rf_trainer.best_param_random_search()
    elif len(arguments) > 1:
        raise Exception("Too many inputs, please type one of 'tune_random', 'tune_grid', 'best_random', 'best_grid'")
    elif arguments[0] == "tune_random":
        rf_trainer.random_search_tuning()
    elif arguments[0] == "tune_grid":
        rf_trainer.grid_search_tuning()
    elif arguments[0] == "best_random":
        rf_trainer.best_param_random_search()
    elif arguments[0] == "best_grid":
        rf_trainer.best_param_grid_search()
    else:
        print("Invalid Input, please type one of 'tune_random', 'tune_grid', 'best_random', 'best_grid'")
