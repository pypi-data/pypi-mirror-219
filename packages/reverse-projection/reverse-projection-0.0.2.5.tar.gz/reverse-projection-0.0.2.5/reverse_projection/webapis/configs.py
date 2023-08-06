from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, QuantileTransformer
from sklearn.decomposition import PCA, KernelPCA, FactorAnalysis, FastICA, TruncatedSVD
from sklearn.cluster import KMeans
from .decomposers import Fisher
from collections import OrderedDict as dict

DECOMPOSERS = dict(
    pca=PCA,
    kmeans=KMeans,
    kernelpca=KernelPCA,
    factor_analysis=FactorAnalysis,
    fast_ica=FastICA, 
    truncated_svd=TruncatedSVD,
    fisher=Fisher,
)

DECOMPOSERS_KWARGS = dict(
    pca={},
    kmeans={"random_state": 0},
    kernelpca={},
    factor_analysis={},
    fast_ica={"random_state": 0}, 
    truncated_svd={"random_state": 0},
    fisher={},
)

DECOMPOSERS_ALIAS = dict(
    pca="主成分分析",
    kmeans="聚类分析",
    kernelpca="核函数主成分",
    factor_analysis="因子分析",
    fast_ica="独立成分分析", 
    truncated_svd="截断奇异值分解",
    fisher="Fisher判别法",
)

SCALERS = dict(
    std=StandardScaler,
    minmax=MinMaxScaler,
    quantile=QuantileTransformer,
)

SCALER_KWARGS = dict(
    std={},
    minmax={},
    quantile={"n_quantiles": 100, "random_state": 0},
)

SCALER_ALIAS = dict(
    std="零均值化",
    minmax="最小最大缩放",
    quantile="分位数缩放",
)

DECOMPOSITIONS_list = [ i for i in DECOMPOSERS.keys()]
SCALERS_list = [ i for i in SCALERS.keys()]