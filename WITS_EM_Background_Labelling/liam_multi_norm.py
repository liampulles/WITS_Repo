import numpy as np
from scipy.stats import multivariate_normal

class LiamMultivariateNormal:
    cov = None
    mean = None

    def multi_norm_pdf(self,x):
        #print(((((2*np.pi)**len(mean))*np.linalg.det(cov))**0.5))
        #inv_cov = np.linalg.inv(self.cov)
        #centred = x-self.mean
        #probs = []
        #for single in centred:
        #    probs += [np.exp(-0.5*np.transpose(single).dot(inv_cov).dot(single))/((((2*np.pi)**len(self.mean))*inv_cov)**0.5)]
        #return probs
        probs = multivariate_normal.pdf(x,mean=self.mean,cov=self.cov)
        #print(probs)
        return probs

    def multi_norm_pdf_single(self,x):
        #print(((((2*np.pi)**len(mean))*np.linalg.det(cov))**0.5))
        inv_cov = np.linalg.inv(self.cov)
        centred = x-self.mean
        return np.exp(-0.5*np.transpose(centred).dot(inv_cov).dot(centred))/((((2*np.pi)**len(self.mean))*inv_cov)**0.5)

    def diag_cov_direct(self,data):
        #get variances independently
        variances = np.var(data,axis=0)
        out = np.identity(data.shape[1],dtype=np.float64)
        for i in range(data.shape[1]):
            out[i,i] = variances[i]
        return out

    def update_direct(self,data):
        self.mean = np.mean(data,axis=0,dtype=np.float64)
        self.cov = self.diag_cov_direct(data)
