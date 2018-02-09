import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np

saved = pickle.load( open( "final.p", "rb" ) )
X = np.array(saved["data"],dtype=np.int32)
#y = np.transpose(np.array([saved["classes"]],dtype=np.int32))
y = saved["classes"]
#print(y)
#join = np.hstack((X,y))
#np.random.shuffle(join)
#X = join[:,0:-1]
#y = np.transpose(join[:,:-1])[0]
#print(X,y)
#np.random
clf = RandomForestClassifier(verbose=0)
clf.fit(X[0:1000],y[0:1000])
pickle.dump(clf , open( "forest.p", "wb" ) )
pred = clf.predict(X[1001:])
act = np.array(y[1001:])
succ = (pred==act)
print("Successful:",np.sum(succ),"out of",len(y[1001:]), "or", np.sum(succ)/float(len(y[1001:])))
#print(y[1001:1006],pred)
