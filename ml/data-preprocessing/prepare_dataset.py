import json
import os
import pandas as pd
from interface import implements, Interface

os.chdir(os.path.dirname(__file__))


class Dataset(Interface):

    def get_dataset(self):
        pass


class SrqDataset(implements(Dataset)):
    PATH = '../datasets/stance_dataset.json'

    def _get_tweet_id_mapping(self):
        tweet_mapping = {}
        with open(SrqDataset.PATH) as f:
            for line in f:
                j_content = json.loads(line)

                if 'target_text' in j_content:
                    tweet_mapping[j_content['target_id']] = j_content['target_text']

                if 'response_text' in j_content:
                    tweet_mapping[j_content['response_id']] = j_content['response_text']
        return tweet_mapping

    def get_dataset(self):
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
    PATH = '../datasets/debagreement.csv'

    def _clean_dataset(self):
        debagreement_df = pd.read_csv(DebagreementDataset.PATH, index_col=False)
        debagreement_df = debagreement_df[
            (debagreement_df['body_parent'].str.len() <= 280) & (debagreement_df['body_child'].str.len() <= 280)]
        debagreement_df = debagreement_df[~(debagreement_df['body_parent'].str.contains("#NAME?")) & ~(
            debagreement_df['body_child'].str.contains("#NAME?"))]

        debagreement_df.rename(columns={'label': 'labels', 'body_child': 'text_b', 'body_parent': 'text_a'},
                               inplace=True)

        return debagreement_df

    def get_dataset(self):
        debagreement_df = self._clean_dataset()

        return debagreement_df[['text_a', 'text_b', 'labels']]


class PrimaryDataset(implements(Dataset)):
    srqDataset = SrqDataset()
    debagreementDataset = DebagreementDataset()

    def get_dataset(self):
        srq_df = PrimaryDataset.srqDataset.get_dataset()
        debagreement_df = PrimaryDataset.debagreementDataset.get_dataset()
        df = srq_df.append(debagreement_df, ignore_index=True)
        return df


if __name__ == "__main__":
    dataset = PrimaryDataset()
    df = dataset.get_dataset()
    df.to_csv("../datasets/dataset.csv", encoding='utf-8', index=False)
