import numpy as np
import copy
from liam_multi_norm import LiamMultivariateNormal
from sklearn.cluster import KMeans

class LiamEM:
    fdists = None
    bdists = None
    fweights = None
    bweights = None
    mode = None
    prop = None
    def __init__(self,k_background,k_foreground):
        self.bdists = []
        for i in range(k_background):
            self.bdists += [LiamMultivariateNormal()]
        self.fdists = []
        for i in range(k_foreground):
            self.fdists += [LiamMultivariateNormal()]
        self.fweights = [0]*(k_foreground)
        self.bweights = [0]*(k_background)

    def initial_classify(self,bdata,fdata):
        cut = int(fdata.shape[0]*0.5)
        #Group
        print("Intial: Foreground Clustering")
        self.fweights = [1.0/len(self.fdists)]*len(self.fdists)
        fclusts = KMeans(n_clusters=len(self.fdists))
        fclusts.fit(fdata[:cut,:])
        for i in range(len(fclusts.cluster_centers_)):

        #self.fweights = np.random.rand(1,len(self.fdists))[0]
        #print(self.fweights)
        #for i in range(len(self.fdists)):
            self.fdists[i].mean = fclusts.cluster_centers_[i]
            self.fdists[i].cov = np.diag([100.0]*fdata.shape[1])
            #print(self.fdists[i].cov)

        print("Intial: Background Clustering")
        #cut = int(bdata.shape[0]*0.1)
        self.bweights = [1.0/len(self.bdists)]*len(self.bdists)
        bclusts = KMeans(n_clusters=len(self.bdists))
        bclusts.fit(bdata[:cut,:])
        for i in range(len(bclusts.cluster_centers_)):

        #self.fweights = np.random.rand(1,len(self.fdists))[0]
        #print(self.fweights)
        #for i in range(len(self.fdists)):
            self.bdists[i].mean = bclusts.cluster_centers_[i]
            self.bdists[i].cov = np.diag([100.0]*fdata.shape[1])
            #print(self.fdists[i].cov)

    def e_step(self,data,focus):
        if focus == "background":
            weights = self.bweights
            dists = self.bdists
        else:
            weights = self.fweights
            dists = self.fdists

        possibs = np.zeros((0,data.shape[0]),dtype=np.float64)
        count = 0
        for dist in dists:
            #print(dist)
            try:
                possibs = np.vstack((possibs,dist.multi_norm_pdf(data)*weights[count]))
                #print(dist.cov,dist.mean,weights[count],possibs)
            except:
                return possibs, True
            count += 1
        #print(possibs)
        denoms = np.sum(possibs,axis=0)
        #print(denoms)
        #input()
        res = possibs/denoms
        return res.T, False

    def m_step(self,data,res):
        #weights
        tot = np.sum(res)
        col_sum = np.sum(res,axis=0)
        weights = col_sum/tot

        #covariance matrices and means
        covs = []
        means = []
        #print(res.shape[0])
        for k in range(res.shape[1]):
            top = np.sum(res[:,k]*data.T,axis=1)
            mean = top/col_sum[k]
            means += [mean]
            centered = data - mean
            #print(col_sum[k])
            centered = np.sum(res[:,k]*(centered**2).T,axis=1)
            #print(centered)
            centered /= col_sum[k]
            sing_cov = np.diag(centered)
            covs += [sing_cov]
            #print(mean, sing_cov)

        return weights,means,covs

    def sum_change(self,old_self,focus):
        if focus == "background":
            weights = self.bweights
            dists = self.bdists
            old_weights = old_self.bweights
            old_dists = old_self.bdists
        else:
            weights = self.fweights
            dists = self.fdists
            old_weights = old_self.fweights
            old_dists = old_self.fdists

        sum_weights = 0
        sum_means = 0
        sum_covar = 0
        for k in range(len(weights)):
            sum_weights += abs(weights[k]-old_weights[k])
            sum_means += np.sum(np.abs(dists[k].mean-old_dists[k].mean))
            sum_covar += np.sum(np.abs(dists[k].cov-old_dists[k].cov))
        return sum_weights, sum_means,sum_covar

    def res_delta(self,res,res_old):
        return np.sum(np.abs(res-res_old))

    #From https://stackoverflow.com/questions/17931613/how-to-decide-a-whether-a-matrix-is-singular-in-python-numpy
    def is_invertible(self,a):
        try:
            np.linalg.inv(a)
            return True
        except:
            return False

    def EMIter(self,data,delta,focus, iterations):

        #Background EM
        if focus == "background":
            res = np.ones((len(data),len(self.bdists)))*999
        else:
            res = np.ones((len(data),len(self.fdists)))*999
        resdiff = delta*2
        sum_cov = 99
        iteration = 0
        weights = []
        covs = []
        means = []
        while (sum_cov > delta) & (iteration < iterations):
            iteration += 1
            res_old = res
            print("Training [{}] {}(E Step)".format(focus,iteration))
            res, singular = self.e_step(data,focus)
            if singular:
                print("Training: Singular covariance matrix detected during E Step")
                for k in range(len(weights)):
                    if focus == "background":
                        self.bdists[k].mean = old_means[k]
                        self.bdists[k].cov = old_covs[k]
                    else:
                        self.fdists[k].mean = old_means[k]
                        self.fdists[k].cov = old_covs[k]
                break
            print("Training [{}] {}(M Step)".format(focus,iteration))
            old_covs = covs
            old_weights = weights
            old_means = means
            weights,means,covs = self.m_step(data,res)
            old_self = copy.deepcopy(self)
            for k in range(len(weights)):
                if focus == "background":
                    self.bdists[k].mean = means[k]
                    self.bdists[k].cov = covs[k]
                    det = np.linalg.det(self.bdists[k].cov)
                else:
                    self.fdists[k].mean = means[k]
                    self.fdists[k].cov = covs[k]
                    det = np.linalg.det(self.fdists[k].cov)
                    #self.bdists[k].cov /= det
                #tiny = det
            if focus == "background":
                self.bweights = weights
            else:
                self.fweights = weights
            #print(weights)
            resdiff = self.res_delta(res,res_old)
            sum_weights,sum_means,sum_cov = self.sum_change(old_self,focus)
            print("Training [{}] {}(Res. Delta = {}; Weights Delta = {}; Means Delta = {}; Cov. Delta = {})".format(focus,iteration,resdiff,sum_weights,sum_means,sum_cov))

    def train(self,bdata,fdata,iterations,prop_in,delta=10):
        #Intialization
        self.initial_classify(bdata,fdata)
        #Background
        print("=====Training Background=====")
        self.EMIter(bdata,delta,"background",iterations)
        #Foreground
        print("=====Training Foreground=====")
        self.EMIter(fdata,delta,"foreground",iterations)
        #Balance weights
        print("=====Balancing Weights=====")
        self.prop = prop_in
        #data = np.vstack((bdata,fdata))
        #bbres,sing = self.e_step(bdata,"background")
        #fbres,sing = self.e_step(bdata,"foreground")
        #bfres,sing = self.e_step(fdata,"background")
        #ffres,sing = self.e_step(fdata,"foreground")
        #bsum = np.average(bbres)
        #fsum = np.average(ffres)
        #print(bsum,fsum)
        #self.prop =
        #data = np.vstack((bdata,fdata))
        #print(data.shape)
        #bres,sing = self.e_step(fdata,"background")
        #fres,sing = self.e_step(fdata,"foreground")
        #res = np.hstack((bres,fres))
        #print(res)
        #tot = np.sum(res)
        #col_sum = np.sum(res,axis=0)
        #print(tot)
        #weights = col_sum/tot
        #print(weights)

        #self.bweights = weights[:len(self.bweights)]
        #self.fweights = weights[len(self.bweights):]

        cut = min(fdata.shape[0],5000)
        data = np.vstack((bdata[:cut,:],fdata[:cut,:]))
        foreprobcoin = np.zeros((1,data.shape[0]))
        for i in range(len(self.fdists)):
            fdist = self.fdists[i]
            weight = self.fweights[i]
            foreprobcoin += fdist.multi_norm_pdf(data)*weight
             #print(fdist.cov)
        #
        backprobcoin = np.zeros((1,data.shape[0]))
        for i in range(len(self.bdists)):
            bdist = self.bdists[i]
            weight = self.bweights[i]
            backprobcoin += bdist.multi_norm_pdf(data)*weight

        prob = (1.0/np.vstack((np.zeros((cut,1))+0.001,np.ones((cut,1)))))+1.0
        uprop = prob-foreprobcoin
        uprop = backprobcoin/uprop
        print(np.average(uprop),np.var(uprop))
        self.prop = np.average(uprop)
        #if np.average((foreprobcoin[cut:]*self.prop)/((foreprobcoin[cut:]*(self.prop))+(backprobcoin[cut:]*(1.0-self.prop)))) >= 0.5:
        #    self.prop = 1 - self.prop
        #
        # foreprobback = np.zeros((1,bdata.shape[0]))
        # for i in range(len(self.fdists)):
        #     fdist = self.fdists[i]
        #     weight = self.fweights[i]
        #     foreprobback += fdist.multi_norm_pdf(bdata)*weight
        #     #print(fdist.cov)
        #
        # backprobback = np.zeros((1,bdata.shape[0]))
        # for i in range(len(self.bdists)):
        #     bdist = self.bdists[i]
        #     weight = self.bweights[i]
        #     backprobback += bdist.multi_norm_pdf(bdata)*weight
        #
        # foreprobacc = np.average(foreprobcoin)-np.average(foreprobback)
        # backprobacc = np.average(backprobback)-np.average(backprobcoin)
        # self.prop = foreprobacc / (backprobacc+foreprobacc)
        # print(foreprobacc,backprobacc,self.prop)

    def classify(self,x,invert=False,flip=False):
        foreprob = np.zeros((1,x.shape[0]))
        for i in range(len(self.fdists)):
            fdist = self.fdists[i]
            weight = self.fweights[i]
            foreprob += fdist.multi_norm_pdf(x)*weight
            #print(fdist.mean)

        backprob = np.zeros((1,x.shape[0]))
        for i in range(len(self.bdists)):
            bdist = self.bdists[i]
            weight = self.bweights[i]
            backprob += bdist.multi_norm_pdf(x)*weight
            #print(bdist.multi_norm_pdf(x))
            #print(bdist.cov)

        uprop = self.prop
        if flip:
            uprop = 1.0-uprop
        #print(backprob)
        finalprob = (foreprob*uprop) /((foreprob*(uprop))+(backprob*(1.0-uprop)))
        if invert:
            finalprob = 1.0-finalprob
        #print(finalprob)
        mask = (finalprob*255).astype(np.uint8)
        return mask
