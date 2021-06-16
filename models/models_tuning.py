"""
Module for tuning model parameters.
"""
import pandas
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV

from models.models_features import FeaturesImportance
from models.models_review import review_classification
from services.utils import create_binary_target, split_data
from settings import config, params
from settings.config import reports
from settings.params import models_params, MAIN_SCORE


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

    x, y = split_data(dataframe)
    x_best = x[best_cols_list]

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


if __name__ == '__main__':
    train_cv()
