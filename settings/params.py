"""
Parameters for models.
"""
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from settings import config

FEATURES_IMPORTANT_RATE = 2.5

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
