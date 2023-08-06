from collections import OrderedDict as dict
from email import iterators
import pandas as pd, numpy as np, uuid
from sklearn.preprocessing import StandardScaler
import scipy.optimize as opt
from flask import current_app
import warnings
from .db import SQLiteDB
from .utils import get_feature_ind, get_json
from .targets import Targets
from .configs import SCALERS, DECOMPOSERS, DECOMPOSERS_KWARGS, SCALER_KWARGS
from ..search import ReverseProjection

warnings.filterwarnings("ignore")


mapping_jsons_dict = dict()
mapping_jsons_dict.update({
    "uid": "uid",
    "name": "name",
    "datasetId": "dataset_id",
    "omitInd": "omit_ind",
    "decomposer": "decomposer",
    "scaler": "scaler",
    "unique": "unique",
    "reg2cls": "reg2cls",
    "goodSampleIndexes": "good_sample_indexes",
    "plotLabelTypes": "plot_label_types",
    "axis": "axis",
    "rectRange": "rect_range",
    "featureRange": "feature_range",
    "datasetName": "dataset_name"
})

def get_jsons_for_model(**kwargs) -> dict:
    mapping_jsons_dict_ = dict()
    mapping_jsons_dict_.update(mapping_jsons_dict)
    mapping_jsons_dict_.update(kwargs)
    model_params = dict()
    for k, v in mapping_jsons_dict_.items():
        model_params[v] = get_json(k)
    if model_params["name"] is None:
        model_params["name"] = "新建模型"
    if model_params["uid"] == -1:
        model_params["uid"] = str(uuid.uuid4())
    
    dataset_id = model_params["dataset_id"]
    with SQLiteDB(current_app.db_url) as db:
        dbmsg = db.get_dataset_by_id(dataset_id, post=False)
        data = dbmsg.return_values
    model_params.update({
        "dataset": data["dataset"], 
        "number_ind": data["number_ind"], 
        "target_ind": data["target_ind"],
        "dataset_name": data["name"],
    })

    if model_params["good_sample_indexes"] is None or len(model_params["good_sample_indexes"]) == 0:
        model_params["good_sample_indexes"] = [0 for i in range(len(model_params["target_ind"]))]

    if model_params["plot_label_types"] is None:
        model_params["plot_label_types"] = []

    if model_params["feature_range"] is None:
        model_params["feature_range"] = data["feature_range"]
    return model_params

class Decomposition:

    def __init__(self,
                 name: str,
                 uid: str,
                 dataset: pd.DataFrame, 
                 number_ind: int, 
                 target_ind: list, 
                 omit_ind: list=[],
                 scaler: str="std", 
                 decomposer: str="pca",
                 unique: int=5, 
                 reg2cls: str="mean",
                 good_sample_indexes: list=[],
                 plot_label_types: list=[],
                 shrink: float=0.8, 
                 learning_rate: float=0.618,
                 axis: list=[],
                 rect_range: list=[],
                 dataset_id: int=0,
                 dataset_name: str="",
                 feature_range: list=[],
                 **kwargs):

        if name: 
            self.name = name
        else:
            self.name = "新建模型"

        self.uid = uid
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.feature_range = np.array(feature_range)
        # self.feature_range2 = self.feature_range[self.feature_ind]

        self.dataset = dataset
        self.index = dataset.iloc[:, number_ind].values.reshape(-1, )
        self.origin_targets = dataset.iloc[:, target_ind]
        self.feature_ind = get_feature_ind(dataset.shape[1], number_ind, target_ind, omit_ind)
        self.feature_ind2 = get_feature_ind(dataset.shape[1], number_ind, target_ind)
        self.features = dataset.iloc[:, self.feature_ind].values
        self.features2 = dataset.iloc[:, self.feature_ind2].values
        self.feature_names = dataset.columns[self.feature_ind].values
        self.columns = dataset.columns.values

        self.number_ind = number_ind
        self.target_ind = target_ind
        self.omit_ind = omit_ind
        self.unique = unique
        self.reg2cls = reg2cls
        self.good_sample_indexes = good_sample_indexes
        self.plot_label_types = plot_label_types
        self.shrink = shrink
        self.learning_rate = learning_rate
        self.axis = self.check_axis(axis)
        
        self.rect_range = np.reshape(rect_range, (-1, )).round(2)

        self.targets = Targets(dataset.iloc[:, target_ind], unique, reg2cls, good_sample_indexes)
        if len(self.plot_label_types) == 0:
            self.plot_label_types = []
            for i in self.targets:
                if i.task == "cls":
                    self.plot_label_types.append(1)
                elif i.task == "reg":
                    self.plot_label_types.append(0)

        self.scaler = scaler
        self.decomposer = decomposer
        self._scaler = SCALERS.get(scaler)
        self.s_kwargs = SCALER_KWARGS.get(scaler)
        self._decomposer = DECOMPOSERS.get(decomposer)
        self.d_kwargs = DECOMPOSERS_KWARGS.get(decomposer)

        self.process()
    
    # 检查axis是否超出变量维度上限
    def check_axis(self, axis):
        adjusted_axis = []
        for axis_ in axis:
            if axis_ >= len(self.feature_ind):
                axis_ = len(self.feature_ind) - 1
            adjusted_axis.append(axis_)
        return adjusted_axis

    
    def process(self) -> None:
        self._scaler = self._scaler().fit(self.features)
        self.scaled_features = self._scaler.transform(self.features)
        self._decomposer = self._decomposer(**self.d_kwargs)
        self._decomposer.fit(self.scaled_features, self.targets.Y)
        self.decomposed_features = self._decomposer.transform(self.scaled_features)
        # if len(self.rect_range) != 4:
        self._optimize_rect_range()
    
    def _optimize_rect_range(self) -> None:
        # scipy.optimize 搜索优化区域
        gsm = self.targets.gsm # 优类样本mask
        bsm = self.targets.bsm # 劣类样本mask
        dfs = self.decomposed_features[:, self.axis] # 降维后变量，取axis维度

        gdfs = dfs[gsm] # 优类样本的降维变量 good decomposed features
        bdfs = dfs[bsm] # 劣类样本的降维变量 bad decomposed features

        # 修改gdfs中的样本，将过于偏远样本去除
        tmp = StandardScaler().fit_transform(gdfs)
        tmp_mask = np.ones(gdfs.shape[0]).astype(bool)
        for i in range(dfs.shape[1]):
            tmp_mask &= tmp[:, i]<=2
        gdfs = gdfs[tmp_mask]

        mins = [
            np.quantile(gdfs[:, 0], 0),
            np.quantile(gdfs[:, 0], 0.45),
            np.quantile(gdfs[:, 1], 0),
            np.quantile(gdfs[:, 1], 0.45),
        ]
        maxs = [
            np.quantile(gdfs[:, 0], 0.55),
            np.quantile(gdfs[:, 0], 1),
            np.quantile(gdfs[:, 1], 0.55),
            np.quantile(gdfs[:, 1], 1),
        ]
        criterion = 0.1
        starts = [
            np.quantile(gdfs[:, 0], criterion), np.quantile(gdfs[:, 0], 1-criterion), 
            np.quantile(gdfs[:, 1], criterion), np.quantile(gdfs[:, 1], 1-criterion),
        ]
        def minimizer(new_rr, *args):
            rect_gsample_mask = np.ones(gdfs.shape[0]).astype(bool)
            for i, j in enumerate([0, 2]):
                rect_gsample_mask &= np.logical_and(
                    gdfs[:, i]>=new_rr[j], gdfs[:, i]<=new_rr[j+1]
                    )
            rect_bsample_mask = np.ones(bdfs.shape[0]).astype(bool)
            for i, j in enumerate([0, 2]):
                rect_bsample_mask &= np.logical_and(
                    bdfs[:, i]>=new_rr[j], bdfs[:, i]<=new_rr[j+1]
                    )
            good_sums = rect_gsample_mask.astype(int).sum()
            bad_sums = rect_bsample_mask.astype(int).sum()
            new_rgs =  good_sums / (good_sums+bad_sums)
            return 1 - new_rgs
        
        bounds = opt.Bounds(mins, maxs)
        res = opt.minimize(minimizer, starts, 
                           bounds=bounds, 
                           tol=0.00001, 
                           options={
                               "maxiter": 500,
                           }, 
                           method="trust-constr",
                           hess=lambda x: np.zeros((4)),
                           )
        self.rect_range_auto = res.x.reshape(-1, )
        if len(self.rect_range) == 0:
            self.rect_range = self.rect_range_auto.copy()
        self.origin_rect_range = starts

    def predict(self, new_features: np.array, axis=True) -> np.array:
        scaled_f = self._scaler.transform(new_features)
        decomposed_f = self._decomposer.transform(scaled_f)
        return decomposed_f[:, self.axis]
    
    @property
    def plot_data(self) -> dict:
        data = []
        good_means = []
        bad_means = []
        dfeatures = self.decomposed_features
        for i, t in enumerate(self.targets):
            data.append(
                np.concatenate([
                    self.index.reshape(-1, 1),
                    t.regvs.reshape(-1, 1),
                    t.clsls.reshape(-1, 1),
                    t.clsvs.reshape(-1, 1),
                    dfeatures[:, self.axis].round(3)
                ], axis=1).tolist()
            )
            good_means.append(
                t.regvs[t.gsm].mean()
            )
            bad_means.append(
                t.regvs[t.bsm].mean()
            )

        model_tmp = dict()
        model_tmp.update(dict(
            uid=self.uid,
            name=self.name,
            omit_ind=self.omit_ind,
            decomposer=self.decomposer,
            scaler=self.scaler,
            unique=self.unique,
            reg2cls=self.reg2cls,
            good_sample_indexes=self.good_sample_indexes,
            plot_label_types=self.plot_label_types,
            axis=self.axis,
            rect_range=self.rect_range.round(2).tolist(),
            dataset_name=self.dataset_name,
            dataset_id=self.dataset_id,
        ))
        model = dict()
        for k, v in mapping_jsons_dict.items():
            if v in model_tmp.keys():
                model[k] = model_tmp[v]
        rpr = dict()
        rpr.update(dict(
            decision_function=self.decision_function,
            unique_values=self.targets.good_sample_reference["unique_values"],
            target_ind=self.target_ind,
            number_ind=self.number_ind,
            fstarti=len(self.target_ind)+1,
            feature_ind=self.feature_ind,
            feature_names=self.feature_names.tolist(),
            columns=self.columns.tolist(),
            orders=self.orders,
            rect_range_auto=self.rect_range_auto.round(2).tolist(),
            optimize_solution=self.optimize_solution,
            stat_rect=self.stat_rect,
            feature_range=np.concatenate([
                np.min(self.features, axis=0).reshape(-1, 1),
                np.max(self.features, axis=0).reshape(-1, 1),
            ], axis=1).round(2).tolist(),
        ))
        return_dict = dict()
        return_dict.update(dict(
            data=data,
            model=model,
            rpr=rpr,
        ))
        return return_dict

    @property
    def decision_function(self) -> dict:
        if self.decomposer in ["pca"] and self.scaler in ["std"]:
            components = self._decomposer.components_.T
            components_ = (components.T / self._scaler.scale_).T
            original_rect_range = self.rect_range.copy()
            if components_.shape[0] != components_.shape[1]:
                return {
                    "components": [],
                    "original_rect_range": []
                }
            tmp = np.dot(self._scaler.mean_, components_) + \
                np.dot(self._decomposer.mean_, components.T)
            tmp = tmp[self.axis]
            for i in range(tmp.shape[0]):
                original_rect_range[i*2: i*2+2] += tmp[i]
            return {
                "components": components_[:, self.axis].round(3).tolist(),
                "original_rect_range": original_rect_range.round(3).tolist()
            }
        else:
            return {
                "components": [],
                "original_rect_range": []
            }
    
    @property
    def orders(self) -> list:
        results = [{
            "label": "默认顺序",
            "importance": "",
            "findex": self.feature_ind2,
        }]
        for i, t in enumerate(self.targets):
            imp = np.abs(np.corrcoef(self.features2, t.regvs, rowvar=False)[-1, :-1]).round(3)
            argsort = np.argsort(imp)[::-1]
            results.append({
                "label": f"与目标值{i+1}相关性顺序",
                "importance": imp[argsort].tolist(),
                "findex": np.array(self.feature_ind2)[argsort].tolist(),
            })
        return results
    
    @property
    def optimize_solution(self) -> list:
        reverse_p = dict(
            feature_values=self.scaled_features[self.targets.gsm],
            feature_names=self.feature_names.tolist(),
            transformer=self._decomposer,
            verbose=False,
            axises=self.axis,
            iteration=200,
        )
        reverse = ReverseProjection(**reverse_p)

        samples = self.decomposed_features[:, self.axis]
        original_samples = self.features
        good_rect_mask, bad_rect_mask, rect_mask = self.rect_mask
        good_rect_samples = samples[self.targets.gsm][good_rect_mask]
        good_original_samples = original_samples[self.targets.gsm][good_rect_mask]
        if good_original_samples.shape[0] > 0:
            original_minimum = good_original_samples.min(axis=0).round(3).tolist()
            original_maximum = good_original_samples.max(axis=0).round(3).tolist()
        else:
            original_minimum = original_maximum = np.zeros_like(original_samples.min(axis=0)).tolist()

        rect_samples = original_samples[rect_mask]
        if rect_samples.shape[0] > 0:
            rect_minimum = rect_samples.min(axis=0).round(3).tolist()
            rect_maximum = rect_samples.max(axis=0).round(3).tolist()
        else:
            rect_minimum = rect_maximum = np.zeros_like(original_samples.min(axis=0)).tolist()

        # grsmin = []
        # grsmax = []
        # if len(good_rect_samples) > 0:
        #     grsmin = good_rect_samples_mins = good_rect_samples.min(axis=0).tolist()
        #     grsmax = good_rect_samples_maxs = good_rect_samples.max(axis=0).tolist()

        # if len(good_rect_samples) > 0:
        #     zip_ = zip(grsmin, grsmax)
        # else:
        #     zip_ = zip(self.rect_range[:2], self.rect_range[2:])

        # results = []
        # for i, j in zip_:
        #     search_r = reverse.search([i, j])
        #     features = search_r["features"]
        #     features = np.reshape(features, (1, -1))
        #     features = self._scaler.inverse_transform(features)
        #     results.append(
        #         features.reshape(1, -1)
        #     )
        # results = np.concatenate([results], axis=0).round(3)
        # maximum = np.max(results, axis=0).reshape(-1, ).tolist()
        # minimum = np.min(results, axis=0).reshape(-1, ).tolist()
        # rect_center_point = [self.rect_range[0:2].mean(), self.rect_range[2:].mean()]
        # results = []
        # for i in range(10):
        #     search_r = reverse.search(rect_center_point)
        #     features = search_r["features"]
        #     features = np.reshape(features, (1, -1))
        #     features = self._scaler.inverse_transform(features)
        #     results.append(
        #         features.reshape(1, -1)
        #     )
        # results = np.concatenate([results], axis=0).round(3)
        # opt_maximum = np.max(results, axis=0).reshape(-1, ).tolist()
        # opt_minimum = np.min(results, axis=0).reshape(-1, ).tolist()
        return {
            # "opt": [ minimum, maximum ],
            "good_mean": [
                original_minimum, 
                original_maximum,
            ],
            "rect_mean": [
                rect_minimum,
                rect_maximum,
            ],
            # "opt_mean": [
            #     opt_minimum,
            #     opt_maximum,
            # ]
        }
    
    @property
    def rect_mask(self) -> list:
        samples = self.decomposed_features[:, self.axis]
        good_samples = samples[self.targets.gsm]
        bad_samples = samples[self.targets.bsm]

        good_rect_mask = np.ones_like(good_samples[:, 0]).astype(bool)
        bad_rect_mask = np.ones_like(bad_samples[:, 0]).astype(bool)
        rect_mask = np.ones_like(samples[:, 0]).astype(bool)

        for i in range(2):
            good_rect_mask = np.logical_and(
                good_rect_mask, good_samples[:, i]>=self.rect_range[2*i]
            )
            good_rect_mask = np.logical_and(
                good_rect_mask, good_samples[:, i]<=self.rect_range[2*i+1]
            )
            bad_rect_mask = np.logical_and(
                bad_rect_mask, bad_samples[:, i]>=self.rect_range[2*i]
            )
            bad_rect_mask = np.logical_and(
                bad_rect_mask, bad_samples[:, i]<=self.rect_range[2*i+1]
            )
            rect_mask = np.logical_and(
                rect_mask, samples[:, i]>=self.rect_range[2*i]
            )
            rect_mask = np.logical_and(
                rect_mask, samples[:, i]<=self.rect_range[2*i+1]
            )
        return good_rect_mask, bad_rect_mask, rect_mask

    @property
    def stat_rect(self) -> list:

        good_rect_mask, bad_rect_mask, rect_mask = self.rect_mask

        good_sample_sum = good_rect_mask.astype(int).sum()
        bad_sample_sum = bad_rect_mask.astype(int).sum()
        sample_sum = good_sample_sum + bad_sample_sum

        results = [
            f"{sample_sum}个投影点, "
            f"{good_sample_sum}个优类投影点, "
            f"{bad_sample_sum}个劣类投影点. "
        ]

        for i, t in enumerate(self.targets):
            results.append(
                f"目标{i}的优类均值: {round(t.regvs[self.targets.gsm][good_rect_mask].mean(), 2)}"
            )
            results.append(
                f"目标{i}的劣类均值: {round(t.regvs[self.targets.bsm][bad_rect_mask].mean(), 2)}"
            )
            results.append(
                f"目标{i}的选区均值: {round(t.regvs[rect_mask].mean(), 2)}"
            )
        return results



