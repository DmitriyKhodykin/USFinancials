"""
The module for evaluate the importance of features.
"""
import pandas

from models.models_review import review_classification
from services.utils import hold_out
from settings import params
from settings.config import reports


class FeaturesImportance:

    def __init__(self):
        self.dataframe = pandas.read_parquet(reports['FeaturesData'])
        self.x_train, self.x_test, self.y_train, self.y_test = hold_out(self.dataframe)

    def evaluate_importance(self) -> list:
        """
        Evaluates the most significant features of the model.
        :return: List with the best features
        """
        # List for best features from features importance
        best_features_indexes: list = []

        best_model_name = review_classification()
        best_model = params.models_dict[best_model_name]
        best_model.fit(self.x_train, self.y_train)
        features_importance = best_model.feature_importances_ * 100

        # Select the best features
        for index, feature in enumerate(features_importance):
            if feature > params.FEATURES_IMPORTANT_RATE:
                best_features_indexes.append(index)

        best_cols_list = [self.dataframe.columns[x] for x in best_features_indexes]

        print(best_cols_list)
        return best_cols_list


if __name__ == '__main__':
    imp = FeaturesImportance()
    imp.evaluate_importance()
