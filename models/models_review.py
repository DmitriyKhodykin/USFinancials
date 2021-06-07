"""
Reviews some models on default params.
"""
import pandas


def review_classification(dataframe: pandas.DataFrame) -> None:
    """
    Reviews some models at standard settings and compares the results.
    :param dataframe: Main dataframe
    :return: None
    """

    # Hold-out
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_SEED
    )

    # CatBoost
    model_cb = CatBoostClassifier(random_state=RANDOM_SEED)
    model_cb.fit(X_train, y_train, silent=True)
    y_cb = model_cb.predict(X_test)
    f_cb = f1_score(y_test, y_cb)
    fi_cb = model_cb.get_feature_importance()

    # LightGBM
    model_lgb = LGBMClassifier(random_state=RANDOM_SEED)
    model_lgb.fit(X_train, y_train)
    y_lgb = model_lgb.predict(X_test)
    f_lgb = f1_score(y_test, y_lgb)
    fi_lgb = model_lgb.feature_importances_ / 25

    # XGBRegressor
    model_xgb = XGBClassifier(random_state=RANDOM_SEED)
    model_xgb.fit(X_train, y_train)
    y_xgb = model_xgb.predict(X_test)
    f_xgb = f1_score(y_test, y_xgb)
    fi_xgb = model_xgb.feature_importances_ * 100

    # RF
    model_rf = RandomForestClassifier(random_state=RANDOM_SEED)
    model_rf.fit(X_train, y_train)
    y_rf = model_rf.predict(X_test)
    f_rf = f1_score(y_test, y_rf)
    fi_rf = model_rf.feature_importances_ * 100

    # Метод опорных векторов
    model_svc = SVC(random_state=RANDOM_SEED, kernel='sigmoid')
    model_svc.fit(X_train, y_train)
    y_svc = model_svc.predict(X_test)
    f_svc = f1_score(y_test, y_svc)
    # importances_svc = model_svc.coef_

    # Таблица итогового сравнения
    results = pd.DataFrame({
        'Classifier': ['CatBoost', 'LGBM', 'XGB', 'RandomForest', 'SVC'],
        'F1_Score': [f_cb, f_lgb, f_xgb, f_rf, f_svc],
        'Feature_Importances': [fi_cb, fi_lgb, fi_xgb, fi_rf, '']
    })

    sorted_results = results.sort_values(by=['F1_Score'], ascending=False)

    print(sorted_results)

    top_results = sorted_results.head(3)

    mean_feature_importances = np.mean(top_results['Feature_Importances'],
                                       axis=0)

    return mean_feature_importances