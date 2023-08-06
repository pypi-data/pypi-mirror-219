
import numpy as np

class Fisher:

    """
    tags: 分类标签
    sample_dict: 每个标签对应的数据 "tag": ndarray
    sample_mean: 每个标签对应的均值 "tag": mean value
    difference_means: 总体平均值之差
    dispersion_dict: 离散度矩阵字典
    """
    def __init__(self):

        self.tags = set([]) #set
        self.sample_dict = {} #dict
        self.sample_mean_list = [] #list
        self.original_variable = None 
        self.original_classes = None
        self.difference_means = 0 #float
        self.dispersion_dict = {} #{}
        self.w = 0 #float
        self.fisvec = None
        self.secvec = None
        self.thivec = None
        self.model_vector = None
        pass


    """
    x: 已经标准后的x
    classes: 分类标签值
    """
    def fit(self, x, classes):

        self.original_variable = x
        self.original_classes = classes
        classes = classes.reshape(len(classes),)
        self.tags = list(set(classes.tolist())) #获取tags,长度<5
        self.tags.sort() #排序

        for tag in self.tags:
            #每个标签对应的数据
            tag_ndarray = x[classes==tag]
            #每个标签对应的平均值
            tag_mean = tag_ndarray.mean(axis=0)
            self.sample_mean_list.append(tag_mean)
            #每个标签对应的数据减去均值
            tag_minus = tag_ndarray - tag_mean
            self.sample_dict[tag] = tag_minus
            #计算离散度
            tag_dispersion = np.dot(tag_minus.T, tag_minus)
            tag_dispersion = tag_dispersion * (len(tag_minus)-1/len(tag_minus))
            self.dispersion_dict[tag] = tag_dispersion
            #计算矩阵w
            self.w += tag_dispersion
        #for index_outer, mean_outer in enumerate(self.sample_mean_list):
        #    for index_inner, mean_inner in enumerate(self.sample_mean_list[index_outer+1:]):
        #        self.difference_means += mean_outer - mean_inner
        for index in range(len(self.sample_mean_list)-1):
            self.difference_means += self.sample_mean_list[index] - self.sample_mean_list[index+1]

        w_inv = np.linalg.inv(self.w)
        self.w_inv = w_inv
        w_inv_2 = np.dot(w_inv, w_inv)
        w_inv_3 = np.dot(w_inv, w_inv_2)
        w_inv_4 = np.dot(w_inv, w_inv_3)

        fisvec = np.dot(self.difference_means, w_inv)
        fisvec = fisvec/np.sqrt(np.sum(np.dot(fisvec, fisvec)))

        secvec = np.dot(self.difference_means, w_inv_2)
        s1 = np.dot(secvec, self.difference_means)
        secvec = np.dot(self.difference_means, w_inv_3)
        s2 = np.dot(secvec, self.difference_means)
        s = s1/s2
        w_inv_2 = w_inv_2 * s
        w_inv = self.w_inv - w_inv_2
        secvec = np.dot(self.difference_means, w_inv)
        secvec = secvec/np.sqrt(np.sum(np.dot(secvec, secvec)))

        thivec = np.dot(self.difference_means, w_inv_3)
        s1 = np.dot(thivec, self.difference_means)
        thivec = np.dot(self.difference_means, w_inv_4)
        s2 = np.dot(thivec, self.difference_means)
        s = s1/s2
        w_inv_3 = w_inv_3 * s
        w_inv = self.w_inv - w_inv_3
        thivec = np.dot(self.difference_means, w_inv)
        thivec = thivec/np.sqrt(np.sum(np.dot(thivec, thivec)))

        v = np.array((fisvec, secvec, thivec)).T
        self.model_vector = v
        self.fisvec = fisvec
        self.secvec = secvec
        self.thivec = thivec
        # transformed_x = np.dot(x, v)
        return self

    def transform(self, new_x):
        return np.dot(new_x, self.model_vector)