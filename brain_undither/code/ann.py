#Custom ANN class

import numpy as np
import pickle

class LiamANN:
    layers = []
    tol = 0.1
    alpha = 1e-5
    max_iter = 200
    w = []
    def __init__(self, layers, tol, alpha, max_iter,X,Y):
        self.data = []
        self.layers = layers
        self.tol = tol
        self.alpha = alpha
        self.max_iter = max_iter
        #self.w = pickle.load( open( "weights.p", "rb" ) )
        self.make_weights(X,Y)

    def make_weights(self,X,Y):
        self.w = dict()
        self.w[0] = np.random.randn(X.shape[1]+1, self.layers[0])
        for i in range(0,len(self.layers)-1):
            #print(len(self.layers))
            self.w[i+1] = np.random.randn(self.layers[i]+1, self.layers[i+1])
        self.w[len(self.layers)] = np.random.randn(self.layers[len(self.layers)-1]+1,Y.shape[1])
        #print(self.w[0].shape,self.w[1].shape,self.w[2].shape)
        #input()

    def sigmoid(self,out):
        return 1.0 / (1.0 + np.exp(-out))

    def weight_change(self,w_1,w_2):
        w_changes = [0]*len(w_1)
        for i in range(len(w_1)):
            w_changes[i] = np.mean(np.mean(np.abs(w_1[i]-w_2[i])))
        print(w_changes)
        return w_changes

    def feed_forward_bulk(self,x):
        for i in range(len(self.w)):
            x = np.dot(np.c_[np.ones(len(x)),x], self.w[i])
            #x = np.dot(self.w[i].T,np.c_[np.ones(len(x)), x])
            if (i != len(self.w)-1):
                x = self.sigmoid(x)
        return x

    def predict(self,X):
        return self.feed_forward_bulk(X)

    def feed_forward(self,x):
        s = [0]*(len(self.w)+1)
        u = [0]*(len(self.w)+1)
        #print(x)
        s[0] = np.hstack(([1.0],x.copy()))
        u[0] = np.hstack(([1.0],x.copy()))
        for l in range(1, len(self.w)+1): # apply forward propagation
            #print(u[l-1], self.w[l-1])
            s[l] = np.dot(u[l-1], self.w[l-1])
            u[l] = np.hstack(([1.0],self.sigmoid(s[l])))
        u[len(u)-1] = s[len(u)-1]
        return u

    def loss_calc(self,outputs,y):
        return outputs[len(outputs)-1]-y

    def back_propogation(self,outputs,y_err):
        #print("out",outputs)
        #print("y_err",y_err)
        l = len(self.w)
        #print(np.reshape(outputs[l-1],(len(outputs[l-1]),1))*np.reshape(y_err,(1,len(y_err))))
        #print(self.w[l-1])
        #delta = outputs[l-1] * y_err.T
        #input()
        #print(outputs)
        #input()
        #delta = np.dot(outputs[l-1],y_err)
        delta = np.reshape(outputs[l-1],(len(outputs[l-1]),1))*np.reshape(y_err,(1,len(y_err)))
        #print(np.dot(np.array(outputs[l-1])[np.newaxis],np.array(y_err)[np.newaxis]))
        #print(self.w[l-1])
        #print("change:",self.w[l-1], outputs[l], delta)
        #change = np.array([[outputs[l] * delta]]).repeat(self.w[l-1].shape[0],axis=1)[0]
        #print(np.array(outputs[l-1]).shape,np.array(delta).shape)
        #print(delta)
        #input()
        y_err = np.dot(y_err, self.w[l-1].T)
        self.w[l-1] = self.w[l-1] - self.alpha * delta
        #print(self.w[l-1])
        #input()
        #print(self.w[l-1])
        #if l != len(self.w)-1:
        #    self.w[l][0,0] = 0.0
        # accumulate the error at the previous layer
        #print(np.dot(self.w[l-1].T,delta))
        #input()
        #print(y_err)
        for l in range(len(self.w)-1, 0, -1): # back propagation
            #print(l)
            #print(self.w[l-1])
            #print(np.reshape(outputs[l-1],(len(outputs[l-1]),1))*np.reshape(y_err,(1,len(y_err))))
            #input()
            #delta = np.reshape((1.0-outputs[l]),(len(outputs[l]),1))*np.reshape(y_err,(1,len(y_err)))
            delta = (1.0-outputs[l])*y_err
            delta = np.reshape(outputs[l-1],(len(outputs[l-1]),1))*np.reshape(delta,(1,len(delta)))
            #print(delta)
            #input()
            #change = np.array([[outputs[l] * delta]]).repeat(self.w[l-1].shape[0],axis=1)[0]
            #change = change[:,:len(change[0])-1]
            #print(np.hstack(([1.0],self.w[l-1])))
            y_err = np.dot(y_err[1:], self.w[l-1].T)
            self.w[l-1] = self.w[l-1] - self.alpha * delta[:,1:]
            #print("change:",change)
            #if l != len(self.w)-1:
            #    self.w[l][0,0] = 0.0
            # accumulate the error at the previous layer

    def test(self,X,Y):
        avg_error = 0
        for n in range(len(X)):
            x = X[n]
            y = Y[n]
            outputs = self.feed_forward(x)
            y_err = self.loss_calc(outputs,y)
            loss_new = np.sum(np.abs(y_err))
            avg_error += loss_new
        return avg_error / len(X)

    def norm(self,dic,count):
        for i in range(len(dic)):
            dic[i] = dic[i]/float(count)
        return dic

    def dict_add(self,dic1,dic2):
        for i in range(len(dic1)):
            dic1[i] += dic2[i]
        return dic1

    def fit(self,X,Y):
        print("(Starting fit)")
        loss = 999999999999;
        test_error = 9999999999;
        #print(self.w)
        X_train = X[:int(len(X)*0.6)]
        #print(X[:int(len(X)*0.6)])
        X_test = X[int(len(X)*0.6):int(len(X)*0.8)]
        X_verify = X[int(len(X)*0.8):]
        Y_train = Y[:int(len(Y)*0.6)]
        Y_test = Y[int(len(Y)*0.6):int(len(Y)*0.8)]
        Y_verify = Y[int(len(Y)*0.8):]
        for i in range(self.max_iter):
            loss_new = 0
            indicies = [range(len(X_train))]
            np.random.shuffle(indicies)
            X_train = X_train[indicies]
            Y_train = Y_train[indicies]
            outputs = -1
            y_err = -1
            for n in range(len(X_train)):
                x = X_train[n]
                y = Y_train[n]
                outputs_new = self.feed_forward(x)
                y_err_new = self.loss_calc(outputs_new,y)
                if (outputs == -1):
                    outputs = outputs_new
                    y_err = y_err_new
                else:
                    outputs = self.dict_add(outputs_new,outputs)
                    y_err = self.dict_add(y_err_new,y_err)
                loss_new += np.sum(np.abs(y_err_new))
                #if loss - loss_new < self.tol:
                #    print("Change in loss less than tolerance!")
                #    return
                #if (loss < self.tol):
                #    print("Tolerance reached!")
                #    return
                w_old = self.w.copy()
                if (n%10) == 9:
                    self.back_propogation(self.norm(outputs,10), self.norm(y_err,10))
                if (n%10000) == 9999:
                    print("({}/{}) - {}".format(n,len(X_train),loss_new))
                    self.weight_change(self.w,w_old)
                    #print(self.w)
                #print("Loss:",y_err)
                #input()
            test_error_new = self.test(X_test,Y_test)
            print("Iteration {}. Loss change: {}. Testing average error: {}".format(i,loss-loss_new,test_error))
            print("Dumping self...")
            pickle.dump( self, open( "reg.p", "wb" ) )
            if (test_error - test_error_new <= 0.0):
                print("Convergence reached!")
                return
            test_error = test_error_new
            loss = loss_new
        verify_error = self.test(X_verify,Y_verify)
        print("Max iterations reached! Final loss: {}. Verification average error: {}".format(loss, verify_error))

    def fit_epoch(self,X,Y):
        print("(Starting fit)")
        loss = 999999999999;
        #print(self.w)
        X_train = X[:int(len(X)*0.6)]
        #print(X[:int(len(X)*0.6)])
        X_test = X[int(len(X)*0.6):int(len(X)*0.8)]
        X_verify = X[int(len(X)*0.8):]
        Y_train = Y[:int(len(Y)*0.6)]
        Y_test = Y[int(len(Y)*0.6):int(len(Y)*0.8)]
        Y_verify = Y[int(len(Y)*0.8):]
        loss_new = 0
        indicies = [range(len(X_train))]
        np.random.shuffle(indicies)
        X_train = X_train[indicies]
        Y_train = Y_train[indicies]
        #print(Y_test)
        outputs = -1
        y_err = -1
        for n in range(len(X_train)):
            x = X_train[n]
            y = Y_train[n]
            outputs = self.feed_forward(x)
            y_err = self.loss_calc(outputs,y)
            #if (outputs == -1):
            #    outputs = outputs_new
            #    y_err = y_err_new
            #else:
            #    outputs = self.dict_add(outputs_new,outputs)
            #    y_err = self.dict_add(y_err_new,y_err)
            loss_new += np.sum(np.abs(y_err))
            #if loss - loss_new < self.tol:
            #    print("Change in loss less than tolerance!")
            #    return
            #if (loss < self.tol):
            #    print("Tolerance reached!")
            #    return
            w_old = self.w.copy()
            self.back_propogation(outputs, y_err)
            if (n%10000) == 9999:
                print("({}/{}) - {}".format(n,len(X_train),loss_new))
                self.weight_change(self.w,w_old)
            #print("Loss:",y_err)
            #input()
        test_error = self.test(X_test,Y_test)
        print("Testing average error: {}".format(test_error))
        print("Dumping self...")
        pickle.dump( self, open( "reg.p", "wb" ) )
        loss = loss_new
