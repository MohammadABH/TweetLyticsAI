import json
import os
import pandas as pd
from interface import implements, Interface

os.chdir(os.path.dirname(__file__))


class Dataset(Interface):

    def get_dataset(self):
        """
        Computes the dataset and return it in a pandas data frame
        :return: return the dataset in a pandas dataframe
        """
        pass


class SrqDataset(implements(Dataset)):
    """
    Class that processes the SRQ dataset and converts it into a pandas dataframe
    """
    PATH = '../datasets/stance_dataset.json'

    def _get_tweet_id_mapping(self):
        """
        Given the SRQ JSON dataset is malformed, this function fixes it by returning a tweet mapping from
        ID to text, as text with the same ID is not repeated, hence, must be reconstructed using a map.
        :return:
        """
        tweet_mapping = {}
        with open(SrqDataset.PATH) as f:
            for line in f:
                # For each valid data point, add it to the tweet mapping from id to text
                j_content = json.loads(line)

                if 'target_text' in j_content:
                    tweet_mapping[j_content['target_id']] = j_content['target_text']

                if 'response_text' in j_content:
                    tweet_mapping[j_content['response_id']] = j_content['response_text']
        return tweet_mapping

    def get_dataset(self):
        """
        Loads the SRQ JSON dataset, processes it and converts it into a pandas dataframe
        :return:    SRQ dataset in a dataframe
        """
        # Reconstruct the dataset and cast the label mapping to {attack, support, neutral}
        data = []
        label_mapping = {'Implicit_Support': 2, 'Explicit_Support': 2, 'Implicit_Denial': 0, 'Explicit_Denial': 0,
                         'Queries': 1, 'Comment': 1}
        tweet_mapping = self._get_tweet_id_mapping()
        with open(SrqDataset.PATH) as f:
            for line in f:
                j_content = json.loads(line)

                target_text = tweet_mapping[j_content['target_id']]
                response_text = tweet_mapping[j_content['response_id']]
                label = label_mapping[j_content['label']]

                data.append([target_text, response_text, label])

        df = pd.DataFrame(data, columns=['text_a', 'text_b', 'labels'])
        return df


class DebagreementDataset(implements(Dataset)):
    """
    Class that processes the Debagreement dataset and converts it into a pandas dataframe
    """
    PATH = '../datasets/debagreement.csv'

    def _clean_dataset(self):
        """
        Removes invalid data and pairs where one text is longer than 280 chars
        :return:    debagreement dataset in a pandas dataframe
        """
        debagreement_df = pd.read_csv(DebagreementDataset.PATH, index_col=False)
        debagreement_df = debagreement_df[
            (debagreement_df['body_parent'].str.len() <= 280) & (debagreement_df['body_child'].str.len() <= 280)]
        debagreement_df = debagreement_df[~(debagreement_df['body_parent'].str.contains("#NAME?")) & ~(
            debagreement_df['body_child'].str.contains("#NAME?"))]

        debagreement_df.rename(columns={'label': 'labels', 'body_child': 'text_b', 'body_parent': 'text_a'},
                               inplace=True)

        return debagreement_df

    def get_dataset(self):
        """
        Cleans and returns the debagreement dataset
        :return:    debagreement dataset in a pandas dataframe
        """
        debagreement_df = self._clean_dataset()

        return debagreement_df[['text_a', 'text_b', 'labels']]


class PrimaryDataset(implements(Dataset)):
    """
    Class that processes the Debagreement and SRQ dataset into one
    """
    srqDataset = SrqDataset()
    debagreementDataset = DebagreementDataset()

    def get_dataset(self):
        """
        Function that combines the debagreement and SRQ dataset together
        :return:    pandas dataframe of the debagreement and SRQ dataset together
        """
        srq_df = PrimaryDataset.srqDataset.get_dataset()
        debagreement_df = PrimaryDataset.debagreementDataset.get_dataset()
        df = srq_df.append(debagreement_df, ignore_index=True)
        return df

    def save_dataset(self):
        """
        Saves the final dataset to disk
        """
        dataset_df = self.get_dataset()
        dataset_df.to_csv("../datasets/dataset.csv", encoding='utf-8', index=False)


if __name__ == "__main__":
    dataset = PrimaryDataset()
    dataset.save_dataset()
