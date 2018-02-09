#Custom PCA class

import numpy as np

class LiamPCA:
    e_vect = []
    e_val = []
    means = []

    def __init__(self):
        self.e_vect = []
        self.e_val = []
        self.means = []

    def X_mean(self,X):
        return np.mean(X,axis=0)

    def fit(self,X):
        self.means = self.X_mean(X)
        #print(X)
        X_cent = X - self.means
        #print(X_cent)
        covar = 1.0 / (len(X_cent)-1) * np.dot(X_cent.T,X_cent)
        self.e_val, self.e_vect = np.linalg.eig(covar)
        # sort the eigenvectors in descending order
        li = np.argsort(self.e_val)[::-1]
        self.e_val = np.diag(self.e_val[li])
        self.e_vect = self.e_vect[:,li]

    def transform(self,X,no):
        X_cent = X - self.means
        return np.dot(X_cent,self.e_vect[:, :no])
