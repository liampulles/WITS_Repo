import numpy as np
from os import listdir
from os.path import isfile
import cv2
import pickle
import sys
from sklearn.decomposition import PCA
from sklearn.covariance import empirical_covariance
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
#from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.preprocessing import RobustScaler
#from sklearn.gaussian_process import GaussianProcessClassifier
#from sklearn.ensemble import AdaBoostClassifier
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def extract_data(image,mask):
    #print(image,mask)
    img = cv2.imread(image,cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    msk = cv2.imread(mask,cv2.IMREAD_COLOR)
    msk = cv2.cvtColor(msk, cv2.COLOR_BGR2GRAY)
    white_indices = np.where(msk >= 128)
    #black_indices = np.where(msk < 128)
    #print(img[indices])
    return img[white_indices]#, img[black_indices]

black_files = sorted(listdir("Black/"))
blue_files = sorted(listdir("Blue/"))
darkpiece_files = sorted(listdir("DarkPiece/"))
green_files = sorted(listdir("Green/"))
red_files = sorted(listdir("Red/"))
training_files = sorted(listdir("Training/"))
white_files = sorted(listdir("White/"))
whitepiece_files = sorted(listdir("WhitePiece/"))
yellow_files = sorted(listdir("Yellow/"))
#label_files = label_files[:10]
#train_files = listdir("Training/")

print("\nLoading data into memory...")

black_data = []
blue_data = []
darkpiece_data = []
green_data = []
red_data = []
white_data = []
whitepiece_data = []
yellow_data = []

for train_file in training_files:
    full_train = "Training/{}".format(train_file)
    for folder, data, files in [("Black",black_data,black_files),("Blue",blue_data,blue_files),("DarkPiece",darkpiece_data,darkpiece_files),("Green",green_data,green_files),("Red",red_data,red_files),("White",white_data,white_files),("WhitePiece",whitepiece_data,whitepiece_files),("Yellow",yellow_data,yellow_files)]:
        if train_file in files:
            full_label = "{}/{}".format(folder,train_file)
            pixels = extract_data(full_train,full_label)
            data += [pixels]
    #base = label_file[1:-4]
    #full_train = "{}/t{}.jpg".format(args.training[0],base)


black_data = np.vstack(black_data).astype(np.uint8)
np.random.shuffle(black_data)
blue_data = np.vstack(blue_data).astype(np.uint8)
np.random.shuffle(blue_data)
green_data = np.vstack(green_data).astype(np.uint8)
np.random.shuffle(green_data)
red_data = np.vstack(red_data).astype(np.uint8)
np.random.shuffle(red_data)
white_data = np.vstack(white_data).astype(np.uint8)
np.random.shuffle(white_data)
yellow_data = np.vstack(yellow_data).astype(np.uint8)
np.random.shuffle(yellow_data)
darkpiece_data = np.vstack(darkpiece_data).astype(np.uint8)
np.random.shuffle(darkpiece_data)
whitepiece_data = np.vstack(whitepiece_data).astype(np.uint8)
np.random.shuffle(whitepiece_data)

all_data = np.vstack((black_data,blue_data,green_data,red_data,white_data,yellow_data,darkpiece_data,whitepiece_data))

print("Do PCA")
liam_pca = PCA(n_components=3, copy=True, whiten=True, svd_solver='auto', tol=0.0)
#liam_pca = RobustScaler()
liam_pca.fit(all_data)
black_data = liam_pca.transform(black_data)
blue_data = liam_pca.transform(blue_data)
green_data = liam_pca.transform(green_data)
red_data = liam_pca.transform(red_data)
white_data = liam_pca.transform(white_data)
yellow_data = liam_pca.transform(yellow_data)
darkpiece_data = liam_pca.transform(darkpiece_data)
whitepiece_data = liam_pca.transform(whitepiece_data)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for c, m, data in [('xkcd:black', 'o', black_data[:100,]), ('xkcd:blue', 'o', blue_data[:100,:]),('xkcd:green', 'o', green_data[:100,:]),('xkcd:red', 'o', red_data[:100,:]),('xkcd:light grey', 'o', white_data[:100,:]),('xkcd:yellow', 'o', yellow_data[:100,:]),('xkcd:brown', 'o', darkpiece_data[:100,]),('xkcd:beige', 'o', whitepiece_data[:100,])]:
    xs = data[:,0]
    ys = data[:,1]
    zs = data[:,2]
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Value')

print("\nTraining on data...")
cut = 0
if cut > 0:
    all_data = np.vstack((black_data[:cut,:],blue_data[:cut,:],green_data[:cut,:],red_data[:cut,:],white_data[:cut,:],yellow_data[:cut,:],darkpiece_data[:cut,:],whitepiece_data[:cut,:]))
    labels = ([0]*cut)+([1]*cut)+([2]*cut)+([3]*cut)+([4]*cut)+([5]*cut)+([6]*cut)+([7]*cut)
else:
    all_data = np.vstack((black_data,blue_data,green_data,red_data,white_data,yellow_data,darkpiece_data,whitepiece_data))
    labels = ([0]*black_data.shape[0])+([1]*blue_data.shape[0])+([2]*green_data.shape[0])
    labels += ([3]*red_data.shape[0])+([4]*white_data.shape[0])+([5]*yellow_data.shape[0])+([6]*darkpiece_data.shape[0])+([7]*whitepiece_data.shape[0])

#liam_svc = SVC()
#liam_svc.fit(all_data,np.array(labels))


#Mean calc, Covariance estimation
total = black_data.shape[0]+blue_data.shape[0]+green_data.shape[0]+red_data.shape[0]
total += white_data.shape[0]+yellow_data.shape[0]+darkpiece_data.shape[0]+whitepiece_data.shape[0]
total = float(total)
final = dict()
# final['black'] = dict()
# final['black']['mean'] = np.mean(black_data,axis=0)
# final['black']['cov'] = empirical_covariance(black_data, assume_centered=True)
# final['black']['weight'] = black_data.shape[0]/total
# final['blue'] = dict()
# final['blue']['mean'] = np.mean(blue_data,axis=0)
# final['blue']['cov'] = empirical_covariance(blue_data, assume_centered=True)
# final['blue']['weight'] = blue_data.shape[0]/total
# final['green'] = dict()
# final['green']['mean'] = np.mean(green_data,axis=0)
# final['green']['cov'] = empirical_covariance(green_data, assume_centered=True)
# final['green']['weight'] = green_data.shape[0]/total
# final['red'] = dict()
# final['red']['mean'] = np.mean(red_data,axis=0)
# final['red']['cov'] = empirical_covariance(red_data, assume_centered=True)
# final['red']['weight'] = red_data.shape[0]/total
# final['white'] = dict()
# final['white']['mean'] = np.mean(white_data,axis=0)
# final['white']['cov'] = empirical_covariance(white_data, assume_centered=True)
# final['white']['weight'] = white_data.shape[0]/total
# final['yellow'] = dict()
# final['yellow']['mean'] = np.mean(yellow_data,axis=0)
# final['yellow']['cov'] = empirical_covariance(yellow_data, assume_centered=True)
# final['yellow']['weight'] = yellow_data.shape[0]/total
# final['darkpiece'] = dict()
# final['darkpiece']['mean'] = np.mean(darkpiece_data,axis=0)
# final['darkpiece']['cov'] = empirical_covariance(darkpiece_data, assume_centered=True)
# final['darkpiece']['weight'] = darkpiece_data.shape[0]/total
# final['whitepiece'] = dict()
# final['whitepiece']['mean'] = np.mean(whitepiece_data,axis=0)
# final['whitepiece']['cov'] = empirical_covariance(whitepiece_data, assume_centered=True)
# final['whitepiece']['weight'] = whitepiece_data.shape[0]/total

#knn = KNeighborsClassifier(n_neighbors=3)
#knn.fit(all_data,np.array(labels))
#dtc = DecisionTreeClassifier()
#dtc.fit(all_data,np.array(labels))
#weights = []
#for key in ['black','blue','green','red','white','yellow','darkpiece','whitepiece']:
#    weights += [final[key]['weight']]
#weights = np.array(weights,dtype=np.float64)
#weights /= np.sum(weights)
#print(np.sum(weights))
gnb = GaussianNB()
gnb.fit(all_data,np.array(labels))
#qda = QuadraticDiscriminantAnalysis()
#qda.fit(all_data,np.array(labels))
#gpc = GaussianProcessClassifier()
#gpc.fit(all_data,np.array(labels))
#abc = AdaBoostClassifier()
#abc.fit(all_data,np.array(labels))

final['pca'] = liam_pca
#final['knn'] = knn
#final['dtc'] = dtc
final['gnb'] = gnb
#final['qda'] = qda
#final['abc'] = gnb
#final['gpc'] = gpc
#final['svc'] = liam_svc
#print(final['red']['cov'])
#knn = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto',n_jobs=1)

print("Dumping trained EM classifier...")
pickle.dump( final, open( "norms.p", "wb" ) )
