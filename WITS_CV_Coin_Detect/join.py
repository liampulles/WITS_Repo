import pickle
from os import listdir
from os.path import isfile, splitext

files = ["0-14-final.p","15-56-final.p","57-78-final.p","79-85-final.p"]
files += ["86-127-final.p","128-145-final.p","146-183-final.p","184-199-final.p"]
files += ["200-end-final.p"]
classes = []
data = []
for single in files:
    saved = pickle.load( open( single, "rb" ) )
    classes += saved["classes"]
    data += saved["data"]

#print(len(data),len(classes))
final = {"data":data,"classes":classes}
pickle.dump(final , open( "final.p", "wb" ) )
