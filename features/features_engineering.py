"""
Features Engineering module for main dataframe.
"""
import pandas
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, minmax_scale

from services.utils import timeit
from settings import config
from settings.config import reports
from settings import params


def main():
    fe = FeaturesEngineering()
    # fe.x_axis_scale()
    # fe.pca_transformations()
    fe.save_data()
    pass


class FeaturesEngineering:
    """
    Engineering new features for main dataframe.
    """
    def __init__(self):
        report = reports["CleanData"]
        print(f'Loading data from {report}...')
        self.dataframe = pandas.read_parquet(report)

    def drop_target(self):
        pass

    @timeit
    def x_axis_scale(self) -> pandas.DataFrame:
        x = self.dataframe.drop(config.target_cols[0], axis=1)
        x_scaled = pandas.DataFrame()
        print('Scaling by x axis...')
        for index, row in x.iterrows():
            row_scaled = minmax_scale(row)
            row_scaled = pandas.Series(row_scaled, index=x.columns)
            x_scaled = x_scaled.append(row_scaled, ignore_index=True)
        dataframe = x_scaled
        dataframe[config.target_cols[0]] = self.dataframe[config.target_cols[0]]
        print(dataframe.head())
        self.dataframe = dataframe
        return self.dataframe

    def pca_transformations(self) -> pandas.DataFrame:
        x = self.dataframe.drop(config.target_cols[0], axis=1)
        pca = PCA(n_components=params.PCA_COMPONENTS)
        x_transformed = pca.fit_transform(x)
        dataframe = pandas.DataFrame(x_transformed)
        dataframe.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        dataframe[config.target_cols[0]] = self.dataframe[config.target_cols[0]]
        print(dataframe.head())
        self.dataframe = dataframe
        return self.dataframe

    def save_data(self):
        address = f'{config.FEATURES_DATA_DIRECTORY}/data_features.parquet'
        print(f'Saving to {address}...')
        self.dataframe.to_parquet(address)
        print('OK, featured data saved.')


if __name__ == '__main__':
    main()
