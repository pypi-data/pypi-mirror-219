from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler as STD
import pandas as pd, numpy as np

data = pd.read_table("ZZ72.txt").iloc[:, 3:].values

std = STD().fit(data)
data1 = std.transform(data)
pca = PCA().fit(data1)
data1 = pca.transform(data1)
a = pca.components_.T
# a[:, 0] = -a[:, 0]

a[:, 0] / std.scale_
a[:, 1] / std.scale_

np.dot(std.mean_, a[:, 0] / std.scale_) + np.dot(pca.mean_, a[:, 0]) - 1.976
np.dot(std.mean_, a[:, 0] / std.scale_) + np.dot(pca.mean_, a[:, 0]) + 1.392
np.dot(std.mean_, a[:, 1] / std.scale_) + np.dot(pca.mean_, a[:, 1]) - 1.385
np.dot(std.mean_, a[:, 1] / std.scale_) + np.dot(pca.mean_, a[:, 1]) + 0.9942

np.dot(std.mean_, (a.T / std.scale_).T) + np.dot(pca.mean_, a)

p1 = np.dot(data[0, :], a[:, 0] / std.scale_) - np.dot(std.mean_, a[:, 0] / std.scale_) - np.dot(pca.mean_, a[:, 0])
p2 = np.dot(data[0, :], a[:, 1] / std.scale_) - np.dot(std.mean_, a[:, 1] / std.scale_) - np.dot(pca.mean_, a[:, 1])
