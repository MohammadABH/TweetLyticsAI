import os
import sys
import pandas as pd
import numpy as np
import scipy.sparse as sp
from nltk import download, word_tokenize, corpus, WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, PredefinedSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


download('stopwords')
download('punkt')
download('wordnet')
download('omw-1.4')

os.chdir(os.path.dirname(__file__))


class RandomForestRBAM:
    """
    Class that performs training, hyperparameter tuning and evaluation on a Random Forest classifier.

    Note: The prepare_dataset.py file must be run before this, or ensure that the dataset.csv file exists.
    """
    PATH = '../datasets/dataset.csv'

    def __init__(self):
        self.df = self.get_dataset()

        self.X, self.y, self.X_train, self.y_train, self.X_valid, self.y_valid, self.X_test, self.y_test = self.get_split_dataset()

        self.split_index = self.get_split_index()
        self.ps = PredefinedSplit(test_fold=self.split_index)

    def get_dataset(self):
        """
        Gets the dataset from disk
        :return:    dataframe encoding the dataset
        """
        df = pd.read_csv(RandomForestRBAM.PATH)
        df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)

        return df

    def preprocess(self, tweet):
        """
        Function that preprocesses the input tweet by removing user handles and http
        links

        :param tweet: the input tweet (text) to be preprocessed

        :return       pre-processed tweet
        """
        preprocessed_tweet = []
        original_tweet_words = tweet.split(" ")
        for word in original_tweet_words:
            word = 'http' if word.startswith('http') else word  # Preprocess links
            word = '@user' if word.startswith('@') and len(word) > 1 else word  # Preprocess twitter handles

            preprocessed_tweet.append(word)  # Add the processed word to the list

        preprocessed_tweet_string = " ".join(preprocessed_tweet)
        return preprocessed_tweet_string

    def clean(self, text):
        """
        Function that cleans a text needed for Random Forest classification.

        This function draws on the following resource:
            https://www.kaggle.com/onadegibert/sentiment-analysis-with-tfidf-and-random-forest

        :param text:    text to clean
        :return:        cleaned text
        """
        # Pre-process the text
        processed_text = self.preprocess(text)

        # Tokenize the text
        tokenized_text = word_tokenize(processed_text)

        # Lowercase the text
        lowercased_text = [word.lower() for word in tokenized_text]

        # Remove stopwords
        stopwords = corpus.stopwords.words('english')
        no_stopwords = [word for word in lowercased_text if word not in stopwords]
        no_alpha = [word for word in no_stopwords if word.isalpha()]

        # Lemmatize the text
        wordnet_lemmatizer = WordNetLemmatizer()
        lemma_text = [wordnet_lemmatizer.lemmatize(word) for word in no_alpha]

        # Return the final cleaned text
        cleaned_text = lemma_text

        return cleaned_text

    def get_split_dataset(self):
        """
        Splits the dataset into 80/10/10
        :return:    split dataset
        """
        # Split the dataset
        train_size = 0.8
        test_size = 0.5

        tfidf_vectorizer = TfidfVectorizer(analyzer=self.clean)
        tfidf_vectorizer.fit(pd.concat((self.df['text_a'], self.df['text_b'])).unique())

        # Encode the dataset using TF-IDF
        train_a_trans = tfidf_vectorizer.transform(self.df['text_a'].values)
        train_b_trans = tfidf_vectorizer.transform(self.df['text_b'].values)

        # Use hstack to stack the TF-IDF of text_a and text_b over each other
        X = sp.hstack((train_a_trans, train_b_trans))
        y = self.df[['labels']]

        X_train, X_rem, y_train, y_rem = train_test_split(X, y, train_size=train_size, random_state=42)

        X_valid, X_test, y_valid, y_test = train_test_split(X_rem, y_rem, test_size=test_size, random_state=42)

        return X, y, X_train, y_train, X_valid, y_valid, X_test, y_test

    def get_split_index(self):
        """
        Gets the index in which the data was split on
        :return:    a list of -1's and 0's, where -1 is if it is in the train or test set, 0 if it is in the validation
                    set
        """
        # Split the dataset
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

        # List where -1 = test ot train, 0 = validation
        split_index = [-1 if (x in X_train_index.index) or (x in X_test_index.index) else 0 for x in X_index.index]

        return split_index

    def print_results(self, results):
        """
        Prints the results of running hyperaparameter tuning models on a set
        :param results:     results of a model's effectiveness to print
        """
        # Print the params of the best model
        print(f'BEST PARAMS: {results.best_params_}\n')

        # Loop through each hyperparameter and print the model's effectiveness
        f1s = results.cv_results_['mean_test_f1_weighted']
        accuracies = results.cv_results_['mean_test_accuracy']
        recalls = results.cv_results_['mean_test_recall_weighted']
        precisions = results.cv_results_['mean_test_precision_weighted']

        for f1, accuracy, recall, precision, params in zip(f1s, accuracies, recalls, precisions,
                                                           results.cv_results_['params']):
            # Print the models result on current hyperparameters
            print(
                f'A: {round(accuracy, 3)} / R: {round(recall, 3)} / P: {round(precision, 3)} / F1: {round(f1, 3)}, {params}')

    def evaluate_model(self, model):
        """
        Evaluate the input model on the test set
        :param model:   model to evaluate on the test set
        """
        # Use the model to predict the test set
        y_pred = model.predict(self.X_test)

        # Compare the prediction with the real label and compute evaluation metrics
        accuracy = round(accuracy_score(self.y_test, y_pred), 3)
        precision = round(precision_score(self.y_test, y_pred, average='weighted'), 3)
        recall = round(recall_score(self.y_test, y_pred, average='weighted'), 3)
        f1 = round(f1_score(self.y_test, y_pred, average='weighted'), 3)

        # Print the model's effectiveness
        print(
            f'MAX DEPTH: {model.max_depth} / # OF EST: {model.n_estimators} -- A: {accuracy} / P: {precision} / R: {recall} / F1: {f1}')

    def grid_search_tuning(self):
        """
        Runs grid search hyperparameter tuning on the Random Forest model

        Takes influence from the following source:
            https://www.kaggle.com/code/onadegibert/sentiment-analysis-with-tfidf-and-random-forest/notebook

        """
        # Create the RF classifier with balanced class weights
        rf = RandomForestClassifier(class_weight='balanced')

        # Test the following hyperparameters as influenced from:
        # https://www.kaggle.com/code/onadegibert/sentiment-analysis-with-tfidf-and-random-forest/notebook
        parameters = {
            'n_estimators': [5, 50, 100],
            'max_depth': [2, 10, 20, None],
        }

        # Run grid search and compute f1, recall, precision and accuracy
        rf_grid_search = GridSearchCV(estimator=rf, param_grid=parameters,
                                      scoring=['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted'],
                                      cv=self.ps, refit='f1_weighted', error_score="raise")
        rf_grid_search.fit(self.X, self.y.values.ravel())

        # Print results of grid search
        self.print_results(rf_grid_search)

    def best_param_grid_search(self):
        """
        Trains a random forest model using the optimal hyperparameters found from grid search.
        :return:    the trained random forest model using the optimal hyperparameters found from grid search
        """
        # Train the random forest classifier with the optimal hyperparameters found from grid search
        best_rf_grid = RandomForestClassifier(n_estimators=100, max_depth=None, class_weight='balanced')
        best_rf_grid.fit(self.X_train, self.y_train.values.ravel())

        # Evaluate the model on the test set and print them
        self.evaluate_model(best_rf_grid)

        # Return the best model
        return best_rf_grid

    def random_search_tuning(self):
        """
        Runs random search hyperparameter tuning on the Random Forest model

        Takes influence from the following source:
            https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74

        """
        # Random search hyperparameters to test, takes influence from:
        # https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74

        n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]
        min_samples_split = [2, 5, 10]
        min_samples_leaf = [1, 2, 4]
        max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
        max_depth.append(None)
        bootstrap = [True, False]
        max_features = ['auto', 'sqrt']
        random_grid = {'n_estimators': n_estimators,
                       'min_samples_split': min_samples_split,
                       'min_samples_leaf': min_samples_leaf,
                       'max_depth': max_depth,
                       'max_features': max_features,
                       'bootstrap': bootstrap}

        # Use the random grid to search for best hyperparameters
        # Random forest model with balanced class weights
        rf = RandomForestClassifier(class_weight='balanced')

        # Use random search to test 100 different random hyperparameter instantiations
        # Compute f1, recall, precision and accuracy
        rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=100,
                                       scoring=['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted'],
                                       cv=self.ps, refit='f1_weighted', verbose=2, random_state=42, n_jobs=-1,
                                       error_score='raise')
        # Fit the random search model
        rf_random.fit(self.X, self.y.values.ravel())

        # Print results of random search
        self.print_results(rf_random)

    def best_param_random_search(self):
        """
        Trains a random forest model using the optimal hyperparameters found from random search.
        :return:    the trained random forest model using the optimal hyperparameters found from random search
        """
        # Train the random forest classifier with the optimal hyperparameters found from random search
        best_rf_random = RandomForestClassifier(n_estimators=1000, min_samples_split=2, min_samples_leaf=1,
                                                max_features='sqrt', max_depth=110, bootstrap=True,
                                                class_weight='balanced')
        best_rf_random.fit(self.X_train, self.y_train.values.ravel())

        # Evaluate the model on the test set and print them
        self.evaluate_model(best_rf_random)

        # Return the best model
        return best_rf_random


if __name__ == "__main__":
    rf_trainer = RandomForestRBAM()

    arguments = sys.argv[1:]

    # Handle which random forest task to do based on user input
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
