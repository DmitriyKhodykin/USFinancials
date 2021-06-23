"""
Main module for creating serialized model
"""
import pickle

import pandas
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV

from services.utils import hold_out, split_data
from settings import config, params
from settings.config import reports


class Model:

    def __init__(self):
        self.dataframe = pandas.read_parquet(reports['FeaturesData']).head(500)
        self.x, self.y = split_data(self.dataframe)
        self.x_train, self.x_test, self.y_train, self.y_test = hold_out(self.dataframe)
        self.best_model_name = None  # A variable to store the name of the best model
        self.best_cols_list = []  # List for the best features names

    def save_best_model(self):
        """
        Trains the model for the best features and parameters and serializes it.
        :return: None
        """
        # Selection of the best model
        print('Best model:', self.best_model_name)
        best_model = params.models_dict[self.best_model_name]

        # Set best params for the best model
        best_params = self.train_cv()

        # Fitting the best model on the best params
        best_model.set_params(**best_params)
        # x_best = self.x[self.best_cols_list]
        best_model.fit(self.x_train[self.best_cols_list], self.y_train)

        # Scoring model
        y_best_predict = best_model.predict(self.x_test[self.best_cols_list])
        score = f1_score(self.y_test, y_best_predict)
        print('Best F1 Score:', score)

        # Saving model
        pickle.dump(best_model, open('model.pickle', 'wb'))

    def train_cv(self) -> dict:
        """
        Returns the results of training the model for cross-validation,
        the classes of features are balanced before being fed to the input of the model.
        :return: best score, best params
        """
        # Balancing classes
        sss = StratifiedShuffleSplit(n_splits=5, random_state=config.RANDOM_SEED)

        # Selection of the best model
        best_model = params.models_dict[self.best_model_name]

        # Selection of the most important features for the model
        x_best = self.x[self.best_cols_list]

        # Cross-validation on n-folds, enumeration of the best parameters
        estimator = GridSearchCV(
            estimator=best_model,
            param_grid=params.models_params[self.best_model_name],
            scoring=params.MAIN_SCORE,
            cv=sss,
            return_train_score=True
        )

        # Fitting
        estimator.fit(x_best, self.y)

        # Fitting outcomes - vocabulary with lists of characteristics
        print('Best CV Score:', estimator.best_score_)
        print('Best CV Params:', estimator.best_params_)
        return estimator.best_params_

    def evaluate_features_importance(self) -> list:
        """
        Evaluates the most significant features of the model.
        :return: List with the best features
        """
        # List for best features from features importance
        best_features_indexes: list = []

        best_model = params.models_dict[self.best_model_name]
        best_model.fit(self.x_train, self.y_train)
        features_importance = best_model.feature_importances_ * 100

        # Select the best features
        for index, feature in enumerate(features_importance):
            if feature > params.FEATURES_IMPORTANT_RATE:
                best_features_indexes.append(index)

        self.best_cols_list = [
            self.dataframe.columns[x] for x in best_features_indexes
        ]
        print(self.best_cols_list)
        return self.best_cols_list

    def review_classification(self) -> str:
        """
        Reviews some models at standard settings and compares the results.
        :return: Best model name
        """
        # Models dict from settings.params
        models = params.models_dict

        results = pandas.DataFrame(columns=['Name', 'F1Score'])

        for name, model_ in models.items():
            model_.fit(self.x_train, self.y_train)
            y_predict = model_.predict(self.x_test)
            score = f1_score(self.y_test, y_predict)

            tmp_results = pandas.DataFrame(
                {'Name': [name], 'F1Score': [score]}
            )
            results = results.append(tmp_results,
                                     ignore_index=True)
        sorted_results = results.sort_values(
            by=['F1Score'],
            ascending=False
        )
        print(sorted_results)
        self.best_model_name = sorted_results.head(1)['Name'].values[0]
        return self.best_model_name


if __name__ == '__main__':
    model = Model()
    model.review_classification()
    model.evaluate_features_importance()
    model.save_best_model()
