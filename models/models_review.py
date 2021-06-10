"""
Reviews some models on default params.
"""
import pandas
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.svm import SVC

from services.utils import hold_out
from settings.config import reports


def review_classification(dataframe: pandas.DataFrame) -> None:
    """
    Reviews some models at standard settings and compares the results.
    :param dataframe: Main dataframe
    :return: None
    """

    dataframe = dataframe.copy()

    # Delete type object cols
    for i in dataframe.columns:
        try:
            dataframe[i] = dataframe[i].astype(float)
        except (ValueError, TypeError):
            dataframe.drop(i, axis=1, inplace=True)

    # Hold-out
    x_train, x_test, y_train, y_test = hold_out(dataframe)

    # Models
    models = {
        'CatBoost': CatBoostClassifier(silent=True),
        'LGBM': LGBMClassifier(),
        'RandomForest': RandomForestClassifier(),
        'LogisticRegression': LogisticRegression(),
        'SVC': SVC(kernel='sigmoid')
    }

    results = pandas.DataFrame(columns=['Name', 'F1Score'])

    for name, model in models.items():
        model.fit(x_train, y_train)
        y_predict = model.predict(x_test)
        score = f1_score(y_test, y_predict)
        print(name, 'F1Score:', score)
        tmp_results = pandas.DataFrame({name: score})
        results = results.append(tmp_results)

    sorted_results = results.sort_values(by=['F1Score'], ascending=False)
    print(sorted_results)


if __name__ == '__main__':
    data = pandas.read_parquet(reports['FeaturesData'])
    review_classification(data)
