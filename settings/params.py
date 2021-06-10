"""
Parameters for models.
"""
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

models_list = {
    'CatBoost': CatBoostClassifier(silent=True),
    'LGBM': LGBMClassifier(),
    'RandomForest': RandomForestClassifier(),
    'LogisticRegression': LogisticRegression(),
    'SVC': SVC(kernel='sigmoid')
}
