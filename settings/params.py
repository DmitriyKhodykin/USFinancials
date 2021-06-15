"""
Parameters for models.
"""
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from settings import config

FEATURES_IMPORTANT_RATE = 2.5
MAIN_SCORE = 'f1'

models_dict = {
    'CatBoost': CatBoostClassifier(
        silent=True,
        random_state=config.RANDOM_SEED
    ),
    'LGBM': LGBMClassifier(
        random_state=config.RANDOM_SEED
    ),
    'RandomForest': RandomForestClassifier(
        random_state=config.RANDOM_SEED
    ),
    'LogisticRegression': LogisticRegression(
        random_state=config.RANDOM_SEED
    )
}

models_params = {
    'CatBoost': {
        'iterations': [1500, 2000],
        'learning_rate': [0.3, 0.4],
        'l2_leaf_reg': [3, 5],
        'bagging_temperature': [1],
        'random_strength': [1],
        'one_hot_max_size': [2],
        'leaf_estimation_method': ['Newton']
    },
    'LGBM': {
        'boosting_type': ['gbdt'],
        'num_leaves': [31],
        'max_depth': [- 1],
        'learning_rate': [0.1, 0.3],
        'n_estimators': [100, 500],
        'subsample_for_bin': [200000],
        'objective': [None],
        'class_weight': [None],
        'min_split_gain': [0.0],
        'min_child_weight': [0.001],
        'min_child_samples': [20],
        'subsample': [1.0],
        'subsample_freq': [0],
        'colsample_bytree': [1.0],
        'reg_alpha': [0.0],
        'reg_lambda': [0.0],
        'random_state': [None],
        'n_jobs=': [1],
        'silent': [True],
        'importance_type': ['split']
    },
    'RandomForest': {
        'n_estimators': [10, 100, 1000],
        'criterion': ['gini'],
        'max_depth': [None, 10, 100],
        'min_samples_split': [2, 4, 8],
        'min_samples_leaf': [1, 3],
        'min_weight_fraction_leaf': [0.0],
        'max_features': ['sqrt'],
        'max_leaf_nodes': [None],
        'min_impurity_decrease': [0.0],
        'min_impurity_split': [None],
        'bootstrap': [True],
        'oob_score': [False],
        'n_jobs': [-1],
        'random_state': [config.RANDOM_SEED],
        'verbose': [0],
        'warm_start': [False],
        'class_weight': [None],
        'ccp_alpha': [0.0],
        'max_samples': [None]
    },
    'LogisticRegression': {
        'penalty': ['l2'],
        'dual': [False],
        'tol': [0.0001],
        'C': [1.0],
        'fit_intercept': [True],
        'intercept_scaling': [1],
        'class_weight': [None],
        'random_state': [config.RANDOM_SEED],
        'solver': ['lbfgs'],
        'max_iter': [100],
        'multi_class': ['auto'],
        'verbose': [0],
        'warm_start': [False],
        'n_jobs': [None],
        'l1_ratio': [None]
    }
}
