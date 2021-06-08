"""
Reviews some models on default params.
"""
import pandas
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from xgboost import XGBClassifier

from services.utils import hold_out
from settings import params
from settings.params import reports


def review_classification(dataframe: pandas.DataFrame) -> None:
    """
    Reviews some models at standard settings and compares the results.
    :param dataframe: Main dataframe
    :return: None
    """

    dataframe = dataframe.copy()
    # for i in dataframe.columns:
    #     try:
    #         dataframe[i] = dataframe[i].astype(float)
    #     except (ValueError, TypeError):
    #         dataframe.drop(i, axis=1, inplace=True)

    dataframe = dataframe.drop(['date', 'ticker', 'alter_filing_date',
                                ], axis=1)
    x = dataframe.drop('y_1y', axis=1)
    y = dataframe['y_1y'].apply(lambda t: 1 if t > 1.05 else 0)
    print(y)
    # Hold-out
    # x_train, x_test, y_train, y_test = hold_out(dataframe)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    # CatBoost
    catboost_model = CatBoostClassifier(
        random_state=params.RANDOM_SEED
    )
    catboost_model.fit(x_train, y_train, silent=True)
    y_catboost_model = catboost_model.predict(x_test)
    f1_score_catboost = f1_score(y_test, y_catboost_model)
    print(f1_score_catboost)

    # Models
    models = {
        # 'CatBoost': CatBoostClassifier(),
        'LGBM': LGBMClassifier(),
        'XGB': XGBClassifier,
        'RandomForest': RandomForestClassifier(),
        'SVC': SVC()
    }

    # for name, model in models.items():
    #     model.fit(x_train, y_train)
    #     y_predict = model.predict(x_test)
    #     score = f1_score(y_test, y_predict)
    #     print(name, 'F1Score:', score)

    # # CatBoost
    # catboost_model = CatBoostClassifier(
    #     random_state=params.RANDOM_SEED
    # )
    # catboost_model.fit(x_train, y_train, silent=True)
    # y_catboost_model = catboost_model.predict(x_test)
    # f1_score_catboost = f1_score(y_test, y_catboost_model)
    #
    # # LightGBM
    # lgbm_model = LGBMClassifier(
    #     random_state=params.RANDOM_SEED
    # )
    # lgbm_model.fit(x_train, y_train)
    # y_lgbm_model = lgbm_model.predict(x_test)
    # f1_score_lgbm = f1_score(y_test, y_lgbm_model)
    # print(f1_score_lgbm)
    #
    # # XGBRegressor
    # model_xgb = XGBClassifier(
    #     random_state=params.RANDOM_SEED
    # )
    # model_xgb.fit(x_train, y_train)
    # y_xgb = model_xgb.predict(X_test)
    # f_xgb = f1_score(y_test, y_xgb)
    # fi_xgb = model_xgb.feature_importances_ * 100
    #
    # # RF
    # model_rf = RandomForestClassifier(
    #     random_state=params.RANDOM_SEED
    # )
    # model_rf.fit(x_train, y_train)
    # y_rf = model_rf.predict(x_test)
    # f_rf = f1_score(y_test, y_rf)
    # print(f_rf)
    #
    # # Метод опорных векторов
    # model_svc = SVC(
    #     random_state=params.RANDOM_SEED, kernel='sigmoid'
    # )
    # model_svc.fit(x_train, y_train)
    # y_svc = model_svc.predict(X_test)
    # f_svc = f1_score(y_test, y_svc)
    # # importances_svc = model_svc.coef_

    # Result table
    # results = pandas.DataFrame({
    #     'Classifier': ['CatBoost', 'LGBM', 'XGB', 'RandomForest', 'SVC'],
    #     'F1Score': [f1_score_catboost,
    #                 f1_score_lgbm,
    #                 f_xgb,
    #                 f_rf,
    #                 f_svc]
    # })
    #
    # sorted_results = results.sort_values(by=['F1Score'], ascending=False)
    #
    # print(sorted_results)


if __name__ == '__main__':
    data = pandas.read_parquet(reports['FeaturesData'])
    review_classification(data)
