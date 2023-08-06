import sys, pandas as pd, numpy as np
sys.path.append("..")
from reverse_projection.webapis.algorithms import Decomposition
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 300

x, y = make_classification(n_samples=100, n_features=15, n_informative=15, 
                           n_redundant=0)
x = StandardScaler().fit_transform(x)
data = np.concatenate([
    np.arange(100).reshape(-1, 1), 
    y.reshape(-1, 1),
    x
], axis=1)
data = pd.DataFrame(data)

d = Decomposition(dataset=data, number_ind=0, target_ind=[1])

fig = plt.figure(1, (4, 3))
ax = fig.add_subplot(111)
dfs = d.decomposed_features
ax.scatter(dfs[:, 0], dfs[:, 1], c=y)
rr = d.rect_range
ax.add_patch(
    plt.Rectangle(
        (rr[0], rr[2]), 
        rr[1] - rr[0],
        rr[3] - rr[2],
        facecolor="None",
        edgecolor="red",
        linewidth=1,
        )
    )
