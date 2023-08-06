from pathlib import PurePath
import pandas as pd, numpy as np
import werkzeug, json
from .utils import get_feature_ind, get_json
from sklearn.impute import SimpleImputer


class ReadWebFile:
    def __init__(self, filepath):
        self.filepath = filepath
        if isinstance(filepath, werkzeug.datastructures.FileStorage):
            self.ext = self.extension = PurePath(filepath.filename).suffix

    def read(self):
        if self.ext in [".xlsx", ".xls"]:
            data = pd.read_excel(self.filepath)
        elif self.ext in [".txt", ".csv"]:
            if self.ext == ".txt":
                spliter = "\t"
            elif self.ext == ".csv":
                spliter = ","
            buffer = self.filepath.read()
            for encoding in ["utf-8", "gbk", "utf-16"]:
                try:
                    file_read = buffer.decode(encoding)
                    if "\r\n" in file_read:
                        line_spliter = "\r\n"
                    else:
                        line_spliter = "\n"
                    file_read = file_read.split(line_spliter)
                    error = ""
                    break
                except Exception as e:
                    error = e
                    continue
            if error:
                file_read = ""
            data = []
            if len(file_read) > 0:
                for index, line in enumerate(file_read):
                    row = []
                    for cell in line.split(spliter):
                        row.append(cell)
                    if index == 0:
                        columns = row
                    elif index == len(file_read) - 1:
                        continue
                    else:
                        data.append(row)
                data = pd.DataFrame(data, columns=columns)
            else:
                data = pd.DataFrame([])
        else:
            data = pd.DataFrame([])
        return data


def read_data(filepath: werkzeug.datastructures.FileStorage) -> pd.DataFrame:
    if isinstance(filepath, werkzeug.datastructures.FileStorage):
        return ReadWebFile(filepath).read()


def to_numeric(dataframe: pd.DataFrame, errors="ignore") -> pd.DataFrame:
    return dataframe.apply(pd.to_numeric, errors=errors)


def round_series(series: pd.Series, decimal=3) -> pd.Series:
    if series.dtype == object:
        return series
    else:
        return series.round(decimal)


def round_data(dataframe: pd.DataFrame, decimal=3) -> pd.DataFrame:
    return dataframe.apply(round_series, args=[decimal])

def std_del_features_f(dataset, na_feature_names, number_ind, target_ind):

    feature_ind = get_feature_ind(dataset.shape[1], number_ind, target_ind)
    feature_df = dataset.iloc[:, feature_ind]
    std_del_f = feature_df.columns[feature_df.std().round(2) == 0].tolist()
    na_feature_names += std_del_f
    feature_df = feature_df.loc[:, feature_df.std().round(2) > 0]

    new_dataset = pd.concat([
        dataset.iloc[:, [number_ind]+target_ind], 
        feature_df
        ], axis=1)
    return new_dataset, na_feature_names, number_ind, target_ind

def preprocess_dataset(dataset: pd.DataFrame, number_ind: int, target_ind: list, strategy: str="mean"):
    feature_ind = get_feature_ind(dataset.shape[1], number_ind, target_ind)
    feature_df = dataset.iloc[:, feature_ind]
    feature_df = feature_df.apply(pd.to_numeric, errors="coerce")
    na_feature_mask = feature_df.isna().sum(axis=0).astype(bool)
    na_feature_names = feature_df.columns[na_feature_mask].tolist()
    feature_df.dropna(axis="columns", how="all", inplace=True)
    feature_df.iloc[:, :] = SimpleImputer(strategy=strategy).fit_transform(feature_df)
    new_dataset = pd.concat([
        dataset.iloc[:, [number_ind]+target_ind], 
        feature_df
        ], axis=1)
    new_number_ind = 0
    new_target_ind = [i for i in range(1, len(target_ind)+1)]

    new_dataset, na_feature_names, new_number_ind, new_target_ind = std_del_features_f(new_dataset, na_feature_names, new_number_ind, new_target_ind)
    return new_dataset, na_feature_names, new_number_ind, new_target_ind

def get_jsons_for_dataset() -> dict:
    dataset_params = dict()
    for i, j in zip(
        ["datasetName", "targetInd", "numberInd", "uid"], 
        ["name", "target_ind", "number_ind", "uid"]
        ):
        dataset_params[j] = get_json(i)
    return dataset_params

def get_dataset_from_jsons(name: str, dataset: pd.DataFrame, number_ind: int, target_ind: list) -> dict:
    dataset, na_feature_names, number_ind, target_ind = preprocess_dataset(dataset, number_ind, target_ind)
    feature_ind = get_feature_ind(dataset.shape[1], number_ind, target_ind, [])
    dataset_p = dict()
    dataset_p.update({
        "name": name,
        "dataset": dataset,
        "number_ind": number_ind,
        "target_ind": target_ind,
        "feature_ind": feature_ind,
        "na_feature_names": na_feature_names,
    })
    return dataset_p