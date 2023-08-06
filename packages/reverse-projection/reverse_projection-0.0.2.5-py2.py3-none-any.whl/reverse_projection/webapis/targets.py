import pandas as pd, numpy as np, scipy as sp
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

class REGTarget:
    """
    预处理1个reg的Target
    1. 可能存在reg中有非数值的情况,先作一步数值预处理(dataset预处理中,只对特征变量作了预处理)
    2. 原始值(连续值)存储值存入self.target中备用,同时也存储至regvs
    3. 转换regvs中的值,使之成为clsvs与clsls
    4. 确保regvs, clsvs, clsls
    """
    def __init__(self, 
                 target: np.array,
                 reg2cls: str="mean", 
                 impute: str="mean") -> None:
        self.target = target
        self.reg2cls = reg2cls
        self.impute = impute
        # 初始化其他属性
        self.regvs = None # reg values
        self.criteriion = None # reg 的分类阈值
        self.clsvs = None # cls values
        self.clsls = None # cls labels
        self.uv = []

        self.process()
    
    def process(self) -> None:
        self.preprocess() # 1. 预处理reg中可能存在的非数值的情况
        self.regvs = self.target # 2. 原始值self.target赋予给regvs

        # 3. 转换regvs中的值,使之成为clsvs与clsls
        # 3.1 定义criterion的值,转换时根据criterion的值来分割regvs中的值
        #     预留接口"mean", "median"等
        if self.reg2cls == "mean":
            self.criteriion = np.mean(self.target).reshape(-1, )[0]
        elif self.reg2cls == "median": 
            self.criteriion = np.mean(self.target).reshape(-1, )[0]
        elif self.reg2cls == "modal":
            self.criteriion = sp.stat.modal(self.target)[0][0]
        elif self.reg2cls == "quantile1":
            self.criteriion = np.quantile(self.target, 0.25)
        elif self.reg2cls == "quantile2":
            self.criteriion = np.quantile(self.target, 0.75)
        # 3.2 大于criterion,为0,反之为1
        self.clsvs = np.zeros_like(self.regvs).astype(int)
        self.clsls = self.clsvs.copy().astype(str)
        mask_0 = self.regvs >= self.criteriion
        mask_1 = self.regvs < self.criteriion
        for i, (mask, _) in enumerate(zip([mask_0, mask_1], [">=", "<"])):
            self.clsvs[mask] = i
            self.clsls[mask] = f"{_}{round(self.criteriion, 2)}"
            self.uv.append(f"{_}{round(self.criteriion, 2)}")
    
    def preprocess(self) -> None:
        self.target = pd.to_numeric(self.target, errors="coerce")
        self.target = SimpleImputer(strategy=self.impute).\
            fit_transform(self.target.reshape(-1, 1)).reshape(-1, )
    
    # 4. 确保regvs, clsvs, clsls
    @property
    def values(self):
        return {
            "regvs": self.regvs,
            "clsvs": self.clsvs,
            "clsls": self.clsls,
            "uv": self.uv,
        }

class CLSTarget:
    """
    预处理1个cls的Target(应该不需要预处理)
    1. 原始值(离散值)存储在self.target中,也存储在clsls中
    2. 根据离散值中的取值个数,判定需要多少个数值标签(0,1,2,...)
    3. regvs存放数值标签,与clsvs相同
    """
    def __init__(self, target: np.array) -> None:
        self.target = target
        # 初始化属性
        self.regvs = None
        self.clsvs = None
        self.clsls = None
        self.uv = []
        self.process()
    
    def process(self) -> None:
        self.clsls = self.target
        self.clsvs = np.full_like(self.target, 99).astype(int)

        for i, unique_v in enumerate(np.unique(self.clsls)):
            mask = self.clsls==unique_v
            self.clsvs[mask] = i
            self.uv.append(str(unique_v))
        self.regvs = self.clsvs.copy()

    @property
    def values(self):
        return {
            "regvs": self.regvs,
            "clsvs": self.clsvs,
            "clsls": self.clsls,
            "uv": self.uv,
        }

class Target:
    """
    预处理1个Target内容

    保留原始目标值前期下,准备reg以及cls两种情况的取值: 
    1. 判断传入的target是连续值还是离散值,目前只能借助取值个数来判断(<5)
       小于等于5个取值认定为分类,大于5个取值认定为回归.这个阈值可以更改,默认为5.
    2. 如果判断是回归(task==reg),按照REGTarget处理
    3. 如果判断是分类(task==cls),按照CLSTarget处理
    4. 20220916追加:增加参数task,直接指定reg还是cls
    """
    def __init__(self, 
                 original_target: pd.Series, 
                 unique: int=5, 
                 reg2cls: str="mean", 
                 task: str=None, 
                 good_sample_index: int=0) -> None:
        self.original_target = original_target
        self.original_target_values = original_target.values.reshape(-1, )
        self.name = original_target.name
        self.index = original_target.index
        self.unique = unique
        self.reg2cls = reg2cls
        self.task = task # None, cls, reg
        self.good_sample_index = good_sample_index

        self.uv = original_target.unique() # 取值 => unique values => uv: np.array
        self.nv = self.uv.shape[0] # 取值个数 => number of values => nv: int

        if self.task is None: # 如果task没有指定,就根据uv与nv来判断
            if self.nv > unique:
                self.task = "reg"
            elif self.nv <= unique:
                self.task = "cls"
        self.process()
    
    def process(self) -> None:
        if self.task == "reg":
            self.t = REGTarget(self.original_target_values, self.reg2cls)
        elif self.task == "cls":
            self.t = CLSTarget(self.original_target_values)
        self.regvs = self.t.regvs
        self.clsvs = self.t.clsvs
        self.clsls = self.t.clsls
        self.uv = self.t.uv

        self.gsm = self.clsvs==self.good_sample_index
        self.bsm = np.logical_not(self.gsm)
    
    def set_gli(self, good_sample_index) -> None:
        self.good_sample_index = good_sample_index
        self.gsm = self.clsvs==self.good_sample_index
        self.bsm = np.logical_not(self.gsm)

    def __str__(self) -> str:
        return f"""
            task: {self.task}\n
            regvs: {self.regvs[:3]} ... \n
            clsls: {self.clsls[:3]} ... \n
            clsvs: {self.clsvs[:3]} ... \n
            gsm: {self.gsm[:3]} ... \n
            bsm: {self.bsm[:3]} ... \n
        """

class Targets:
    """
    旨在预处理targets内容
    1个Targets存放多个Target对象
    """
    def __init__(self, 
                 original_targets: pd.DataFrame,
                 unique: int=5,
                 reg2cls: str="mean",
                 good_sample_indexes: list=[],
                 task: str=None,
                 ) -> None:
        self.original_targets = original_targets

        if len(good_sample_indexes) == 0:
            good_sample_indexes = [0 for i in range(original_targets.shape[1])]
        self.targets = [
            Target(original_targets.iloc[:, i], unique, reg2cls, task, good_sample_index)
            for i, good_sample_index in zip(range(original_targets.shape[1]), good_sample_indexes)
        ]

        self.good_sample_indexes = good_sample_indexes
        self.gsm = None
        self.bsm = None

        self._determine_good_samples()
    
    def _determine_good_samples(self) -> None:
        gsm = np.ones_like(self.targets[0].clsvs).astype(bool)
        for t in self.targets:
            gsm &= t.gsm
        self.gsm = gsm
        if (gsm.astype(int).sum()==0):
            self.gsm[:2] = True
        self.bsm = np.logical_not(gsm)
    
    def __getitem__(self, i: int) -> Target:
        return self.targets[i]
    
    def set_glis(self, good_sample_indexes: list) -> None:
        for t, gli in enumerate(self.targets, good_sample_indexes):
            t.set_gli(gli)
        self._determine_good_samples()
    
    @property
    def Y(self):
        y = np.ones_like(self.gsm)
        y[self.gsm] = 0
        y[self.bsm] = 1
        return y

    @property
    def good_sample_reference(self):
        good_sample_indexes = []
        unique_values = []
        for t in self.targets:
            good_sample_indexes.append(t.good_sample_index)
            unique_values.append(t.uv)
        return {
            "good_sample_indexes": good_sample_indexes,
            "unique_values": unique_values,
        }
