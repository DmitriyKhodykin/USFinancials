"""
Main module for creating serialized model
"""
import pandas
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedShuffleSplit

from services.utils import hold_out
from settings import config, params
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


def train_cv() -> dict:
    """
    Returns the results of training the model for cross-validation,
    the classes of features are balanced before being fed to the input of the model.
    :return: best score, best params
    """
    dataframe = pandas.read_parquet(reports['FeaturesData']).head(1000)

    # Balancing classes
    sss = StratifiedShuffleSplit(n_splits=5, random_state=config.RANDOM_SEED)

    # Selection of the best model
    best_model_name = review_classification()
    best_model = params.models_dict[best_model_name]

    # Selection of the most important features for the model
    imp = FeaturesImportance()
    best_cols_list = imp.evaluate_importance()
    x_best = dataframe[best_cols_list]

    y = create_binary_target(
        dataframe,
        config.target_cols[0],
        config.CUT_OFF_VALUE
    )

    # Cross-validation on n-folds, enumeration of the best parameters
    estimator = GridSearchCV(
        estimator=best_model,
        param_grid=models_params[best_model_name],
        scoring=MAIN_SCORE,
        cv=sss,
        return_train_score=True
    )

    # Fitting
    estimator.fit(x_best, y)

    # Fitting outcomes - vocabulary with lists of characteristics
    print('Best Score:', estimator.best_score_)
    print('Best Params:', estimator.best_params_)

    return estimator.best_params_

def review_classification() -> str:
    """
    Reviews some models at standard settings and compares the results.
    :return: Best model name
    """
    dataframe = pandas.read_parquet(reports['FeaturesData'])
    dataframe = dataframe.copy()

    # Hold-out
    x_train, x_test, y_train, y_test = hold_out(dataframe)

    # Models from
    models = params.models_dict

    results = pandas.DataFrame(columns=['Name', 'F1Score'])

    for name, model in models.items():
        model.fit(x_train, y_train)
        y_predict = model.predict(x_test)
        score = f1_score(y_test, y_predict)

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
    best_model_name: str = sorted_results.head(1)['Name'].values[0]

    return best_model_name


if __name__ == '__main__':
    pass
