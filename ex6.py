import numpy as np
from sklearn.feature_selection import mutual_info_classif
from sklearn.datasets import load_iris
iris=load_iris()
x,y=iris.data,iris.target
def evaluate_subset(x_subset):
    mi=mutual_info_classif(x_subset,y)
    return np.mean(mi)
def backtrack(x,k,current_subset=[]):
    if len(current_subset)==k:
        return evaluate_subset(x[:,current_subset]),current_subset
    best_score=-np.inf
    best_subset=None
    for i in range (x.shape[1]):
        if i not in current_subset:
            score,subset=backtrack(x,k,current_subset+[i])
            if score>best_score:
                best_score=score
                best_subset=subset
    return best_score,best_subset
k=3
score,optimal_subset=backtrack(x,k)
print(optimal_subset)
print(score)