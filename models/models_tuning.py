"""
Module for tuning model parameters.
"""
import json

import pandas
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV

from models.models_features import FeaturesImportance
from models.models_review import review_classification
from settings import config, params
from settings.config import reports, target_cols
from settings.params import models_params, MAIN_SCORE


def train_cv() -> dict:
    """
    Returns the results of training the model for cross-validation,
    the classes of features are balanced before being fed to the input of the model.
    :return: best score, best params
    """
    dataframe = pandas.read_parquet(reports['FeaturesData'])

    # Balancing classes
    sss = StratifiedShuffleSplit(n_splits=5, random_state=config.RANDOM_SEED)

    # Selection of the best model
    best_model_name = review_classification()
    best_model = params.models_dict[best_model_name]

    # Selection of the most important features for the model
    imp = FeaturesImportance()
    best_cols_list = imp.evaluate_importance()
    x_best = dataframe[best_cols_list]
    y = dataframe[target_cols[0]]

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
    results = estimator.cv_results_
    print('Results:', results)
    print('Best Score:', estimator.best_score_)
    print('Best Params:')
    print(json.dumps(estimator.best_params_, indent=4, sort_keys=True))

    return results


if __name__ == '__main__':
    train_cv()
