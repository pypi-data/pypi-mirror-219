# 必须要安装hyperopt
from hyperopt import hp, tpe, STATUS_OK, Trials, fmin
import numpy as np

def searching_fn(params, point, transformer, axises):
    point = np.array(point)
    outputted_point = transformer.transform(np.array(params).reshape(1, -1)).reshape(-1, )[axises]
    error = outputted_point - point
    error = (error**2).sum()
    return error, outputted_point

def default_early_stop_fn(criterion=0.00001):
    def early_stop_fn(trials, *args, **wargs):
        best_loss = trials.best_trial["result"]["loss"]
        if best_loss < criterion:
            return True, dict(loss=trials.losses()[-1])
        else:
            return False, dict(loss=trials.losses()[-1])
    return early_stop_fn

def hpopt(feature_ranges, target_point, transformer, iteration, verbose, early_stop_fn, axises, choices, **kwargs):
    """

    feature_ranges包含的是特征们的上下限或者多个选择
    上下限的情况，则传入[start, end]，此时约定start与end均为float类型
    多个选择的情况，则传入[choice1, choice2, ...]，此时约定它们均为int类型

    feature_ranges自身为一个字典
    feature_ranges = dict(
        X1 = list(start, end),
        X2 = list(start, end),
        X3 = list(choice1, choice2)
    )

    target_point是一个二维点，比如[3.14, 1.45]

    transformer是一个拥有transform方法的对象，负责把feature_ranges内生成的点转变成二维点

    """

    # 在feature_ranges中迭代，制作hpopt所需要的space
    hpspace = []
    for choice, (fname, frange) in zip(choices, feature_ranges.items()):
        if choice is True:
            hpobj = hp.choice(fname, frange)
        elif choice is False:
            hpobj = hp.uniform(fname, frange[0], frange[1])
        hpspace.append(hpobj)

    def f(params):
        error = searching_fn(params, target_point, transformer, axises)
        return {'loss': error[0], 'status': STATUS_OK}

    trials = Trials()
    best = fmin(fn=f, space=hpspace, algo=tpe.suggest, max_evals=iteration, verbose=verbose, trials=trials, early_stop_fn=early_stop_fn)

    # best = np.array([ best[i] for i in feature_ranges.keys()]).reshape(1, -1)

    best_fvalues = []
    for choice, (i, j) in zip(choices, feature_ranges.items()):
        if choice is True:
            best_fvalues.append(j[best[i]])
        elif choice is False:
            best_fvalues.append(best[i])

    return np.array(best_fvalues).reshape(1, -1)


def scipy_minimizer(x, *args):
    transformer = args[1]
    t = args[0]
    axises = args[2]
    x = transformer.transform(x.reshape(1, -1))[0, axises]
    return ((x - t) ** 2).sum() ** 0.5

from scipy.optimize import minimize, Bounds
def scipy_minimize(feature_ranges, target_point, transformer, iteration, verbose, criterion, axises, **kwargs):
    mins = []
    maxs = []
    fnames = []
    means = []
    for i,j in feature_ranges.items():
        fnames.append(i)
        mins.append(j[0])
        maxs.append(j[1])
        means.append(np.random.uniform(j[0], j[1]))
    bounds = Bounds(mins, maxs)
    res = minimize(scipy_minimizer, means, 
                   bounds=bounds, 
                   tol=criterion,
                   options={"verbose": verbose, 'maxiter': iteration,},
                   args=(target_point, transformer, axises),
                   method="trust-constr")
    return res.x.reshape(1, -1)