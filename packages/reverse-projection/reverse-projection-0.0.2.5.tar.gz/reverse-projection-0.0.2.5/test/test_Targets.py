import sys
sys.path.append("..")
from reverse_projection.webapis.targets import Targets
from sklearn.datasets import make_classification, make_regression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 300

x, y = make_regression(n_samples=20, n_features=2, n_informative=2, random_state=20220917)
x = PCA().fit_transform(StandardScaler().fit_transform(x))


def test_Targets():
    
    label1 = np.ones_like(y)
    label1[y>np.quantile(y, 0.75)] = 0
    label2 = np.ones_like(y)
    label2[np.logical_and(y<np.quantile(y, 0.9), y>np.quantile(y, 0.6))] = 0
    
    fig = plt.figure(3, (12, 3))
    ax = fig.add_subplot(131)
    ax.scatter(x[:, 0], x[:, 1], c=label1)
    for i, j, t in zip(x[:, 0], x[:, 1], label1):
        ax.text(i, j, int(t))
    ax.text(-0.15, 1.05, "a)", transform=ax.transAxes)
    
    ax = fig.add_subplot(132)
    ax.scatter(x[:, 0], x[:, 1], c=label2)
    for i, j, t in zip(x[:, 0], x[:, 1], label2):
        ax.text(i, j, int(t))
    ax.text(-0.15, 1.05, "b)", transform=ax.transAxes)
    
    targets = pd.DataFrame(np.concatenate([label1.reshape(-1, 1), label2.reshape(-1, 1)], axis=1))
    ts = Targets(targets)
    label3 = np.logical_not(ts.gsm).astype(int)
    ax = fig.add_subplot(133)
    ax.scatter(x[:, 0], x[:, 1], c=label3)
    for i, j, t in zip(x[:, 0], x[:, 1], label3):
        ax.text(i, j, int(t))
    ax.text(-0.15, 1.05, "c)", transform=ax.transAxes)
        
    pass

def test_Targets2():
    
    label1 = np.zeros_like(y)
    label1[y>np.quantile(y, 0.75)] = 1
    label2 = np.zeros_like(y)
    label2[np.logical_and(y<np.quantile(y, 0.9), y>np.quantile(y, 0.6))] = 1
    
    fig = plt.figure(3, (12, 3))
    ax = fig.add_subplot(131)
    ax.scatter(x[:, 0], x[:, 1], c=label1)
    for i, j, t in zip(x[:, 0], x[:, 1], label1):
        ax.text(i, j, int(t))
    ax.text(-0.15, 1.05, "a)", transform=ax.transAxes)
    
    ax = fig.add_subplot(132)
    ax.scatter(x[:, 0], x[:, 1], c=label2)
    for i, j, t in zip(x[:, 0], x[:, 1], label2):
        ax.text(i, j, int(t))
    ax.text(-0.15, 1.05, "b)", transform=ax.transAxes)
    
    targets = pd.DataFrame(np.concatenate([label1.reshape(-1, 1), label2.reshape(-1, 1)], axis=1))
    ts = Targets(targets, good_sample_indexes=[1, 1])
    label3 = ts.gsm.astype(int)
    ax = fig.add_subplot(133)
    ax.scatter(x[:, 0], x[:, 1], c=label3)
    for i, j, t in zip(x[:, 0], x[:, 1], label3):
        ax.text(i, j, int(t))
    ax.text(-0.15, 1.05, "c)", transform=ax.transAxes)
        
    pass

def test_Targets3():
    
    fig = plt.figure(1, (12, 3))
    targets = pd.DataFrame(np.concatenate([y.reshape(-1, 1), (y*1.5).reshape(-1, 1)], axis=1))
    ts = Targets(targets, good_sample_indexes=[0, 0])
    
    ax = fig.add_subplot(131)
    ax.scatter(x[:, 0], x[:, 1], c=ts[0].clsvs)
    for i, j, k in zip(x[:, 0], x[:, 1], ts[1].clsls):
        ax.text(i, j, k)
    pass

test_Targets3()