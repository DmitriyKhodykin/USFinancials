"""
Reviews some models on default params.
"""
import pandas
from sklearn.metrics import f1_score

from services.utils import hold_out
from settings import params
from settings.config import reports


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
    review_classification()
