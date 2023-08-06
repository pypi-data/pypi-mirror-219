import pandas as pd
from pandas import DataFrame
import numpy as np
from .algorithms import hpopt, default_early_stop_fn, scipy_minimize
from collections import OrderedDict
from collections.abc import Iterable

METHODS = ["hpopt", "scipy_minimize"]

# 考虑输入的内容：
# 1、变量范围
# 2、目标点
# 3、搜索方法选择？

class ReverseProjection(object):

    def __init__(self,
                 feature_ranges=None,
                 feature_values=None,
                 feature_names=None,
                 transformer=None,
                 method="scipy_minimize",
                 choices=None,
                 axises=None,
                 iteration=200,
                 criterion=0.001,
                 verbose=False):
        """
        feature_ranges 用于定义特征的范围
        期望格式：
        dict(
            x1 = [bottom, top],
            ...
        )
        feature_values 为传入的变量数据集
        如果feature_ranges没有定义的话，则可以从feature_values中生成
        feature_values 应当为ndarray或者DataFrame

        feature_names: 用于规定features的顺序，没的话就不考虑了

        transformer: 类似于PCA()的实例，具有transform方法

        method: 用于选择优化方法，目前分为hpopt与scipy的minimize
        choices: 如果method选择hpopt，那么可以有hp.choice的选择。也就是说此时变量的选择可以是离散的（或者说categorical）。
        我在这里设置了2种选择，hp.choice与hp.uniform。定义choices为[True, False, ...]的话，对应True为hp.choice，False为uniform。

        axises: 用于选择降维的主成分维度。比如传入的点是第1、4主成分，那么这里axises就是[0, 3]。那你想传入第1,2,3，那就是[0,1,2]了。
        默认写个None，我会在search时根据point的维度来生成[0,1]或者[0,1,2]。

        iteration: 搜索最大轮数
        criterion: 精度。精度到了就提前停止。
        """

        # 检查feature_ranges
        # 如果feature_ranges非空
        if feature_ranges is not None:
            # 检查feature_ranges是否是dict
            if isinstance(feature_ranges, (dict, OrderedDict)):
                # 如果是的话，检查values是否是可迭代对象，并且其值是否为数字
                for v in feature_ranges.values():
                    if isinstance(v, Iterable):
                        for i in v:
                            if not isinstance(i, (int, float)):
                                raise Exception(f"ranges in feature_ranges should be int, float, ,e.g., 'x1': [0, 1]"
                                                f"not {type(i)}.")
                    elif not isinstance(v, Iterable):
                        raise Exception(f"values in feature_ranges should be Iterable, not {type(v)}.")
                tmp = OrderedDict()
                for (i, j) in feature_ranges.items():
                    tmp[i] = j
                feature_ranges = tmp
            else:
                raise Exception(f"feature_ranges should be dict or OrderDict, not {type(feature_ranges)}.")
        # 如果feature_ranges为None
        elif feature_ranges is None:
            # 考虑feature_values
            if feature_values is None:
                # 两者不能同时为None
                raise Exception("one of feature_ranges and feature_values should not be None.")
            elif feature_values is not None:
                # 如果feature_values不为None，而feature_ranges为None，则可以从feature_values中生成
                if not isinstance(feature_values, (np.ndarray, pd.DataFrame)):
                    # 但必须是ndarray或者DataFrame
                    raise Exception(f"feature_values should be ndarray or DataFrame, not {type(feature_values)}.")
                else:
                    if isinstance(feature_values, (np.ndarray)):
                        if feature_names:
                            fnames = feature_names
                        else:
                            fnames = [ "XX"+str(i) for i in range(feature_values.shape[1])]
                        fvalues = feature_values
                    elif isinstance(feature_values, (pd.DataFrame)):
                        fnames = feature_values.columns.tolist()
                        fvalues = feature_values.values
                    feature_ranges = OrderedDict()
                    for i in range(len(fnames)):
                        feature_ranges[fnames[i]] = [fvalues.min(), fvalues.max()]
        franges = OrderedDict()
        if feature_names is None:
            self.feature_names = []
            for (i, j) in feature_ranges.items():
                franges[i] = j
                self.feature_names.append(i)
        elif feature_names is not None:
            self.feature_names = feature_names
            if not isinstance(feature_names, Iterable):
                raise Exception(f"feature_names should be Iterable, not {type(feature_names)}")
            if len(feature_names) != len(feature_ranges):
                raise Exception(f"length of feature_names should be equal to feature_names, not {len(feature_names)} : "
                                f"{len(feature_ranges)}")
            for fname in feature_names:
                franges[str(fname)] = feature_ranges[str(fname)]
        self.feature_ranges = franges

        # 检查transformer
        if not "transform" in dir(transformer):
            raise Exception("transformer should have member function 'transform'")
        self.transformer = transformer

        # 检查method
        if method not in METHODS:
             raise Exception(f"method should one of {METHODS}")
        self.method = method

        # 检查choices
        if choices is not None:
            if not isinstance(choices, Iterable):
                raise Exception(f"choices should be Iterable, not {type(choices)}")
            if len(choices) != len(feature_ranges):
                raise Exception(f"length of choices should be equal to feature_names, not {len(choices)} : "
                                f"{len(feature_ranges)}")
        else:
            choices = np.zeros(len(feature_ranges))
        self.choices = [bool(i) for i in choices]

        # 检查axises
        if axises is not None:
            if not isinstance(axises, Iterable):
                raise Exception(f"axises should be Iterable, not {type(axises)}")
            else:
                self.axises = []
                for i in axises:
                    if not isinstance(i, (int, float)):
                        raise Exception(f"member of axises should be int or float (could convert to int), not {type(i)}")
                    self.axises.append(int(i))
        else:
            self.axises = None

        # 检查iterations
        if not isinstance(iteration, (int, float)):
            raise Exception(f"iteration should be int or float (could convert to int), not {type(iteration)}")
        self.iteration = iteration

        # 检查criterion
        if not isinstance(criterion, (float)):
            raise Exception(f"criterion should be float, not {type(iteration)}")
        self.criterion = criterion

        # 检查verbose
        self.verbose = bool(verbose)

    def search(self, target_point):

        if self.axises is None:
            self.axises = range(len(target_point))

        if self.method == "hpopt" or True in self.choices:
            result = hpopt(self.feature_ranges,
                           target_point,
                           self.transformer,
                           self.iteration,
                           self.verbose,
                           default_early_stop_fn(self.criterion),
                           self.axises,
                           self.choices)
        elif self.method == "scipy_minimize" and True not in self.choices:
            result = scipy_minimize(self.feature_ranges,
                                    target_point,
                                    self.transformer,
                                    self.iteration,
                                    self.verbose,
                                    self.criterion,
                                    self.axises)
        return dict(
            points=self.transformer.transform(result)[0, self.axises].tolist(),
            features=result.tolist()[0],
            feature_names=self.feature_names
            )