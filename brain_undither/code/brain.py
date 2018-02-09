import numpy as np
import pickle
import unmask
import ann
import pca
from PIL import Image, ImageFilter
import os

#Must be odd!
region_dim = 7

img_dither_folder = "./data/dither/"
img_orig_folder = "./data/orig/"

def mirror_load(img_in):
    img_file = Image.open(img_in)
    img_file = unmask.unmask(img_file)
    width, height = img_file.size
    half = int(region_dim/2)
    outputimage = Image.new('RGB',(width+region_dim-1,height+region_dim-1),0)
    #Paste center
    outputimage.paste(img_file, box=(half,half))
    #Paste top
    outputimage.paste(img_file.crop((0,0,width,half)), box=(half,0))
    #Paste bottom
    outputimage.paste(img_file.crop((0,height-half,width,height)), box=(half,half+height))
    #Paste left
    outputimage.paste(img_file.crop((0,0,half,height)), box=(0,half))
    #Paste right
    outputimage.paste(img_file.crop((width-half,0,width,height)), box=(half+width,half))
    #Paste top left corner
    outputimage.paste(img_file.crop((0,0,half,half)), box=(0,0))
    #Paste top right corner
    outputimage.paste(img_file.crop((width-half,0,width,half)), box=(width+half,0))
    #Paste bottom right corner
    outputimage.paste(img_file.crop((width-half,height-half,width,height)), box=(width+half,height+half))
    #Paste bottom left corner
    outputimage.paste(img_file.crop((0,height-half,half,height)), box=(0,half+height))

    img_file.close()
    return outputimage

def crop_and_copy(img_border_file,lxi,lyi):
    #half = int(region_dim/2)
    width, height = img_border_file.size
    width -= (region_dim-1)
    height -= (region_dim-1)
    crop_left = lxi
    crop_tot_left = width+lxi
    crop_top = lyi
    crop_tot_top = height+lyi
    #img_border_file.crop((crop_left,crop_top,crop_tot_left,crop_tot_top)).save("border ({},{}).png".format(lxi,lyi))
    return img_border_file.crop((crop_left,crop_top,crop_tot_left,crop_tot_top))

def img_to_vecs(img_dither):
    #load
    img_dither_file = mirror_load(img_dither)
    width, height = img_dither_file.size
    width -= (region_dim-1)
    height -= (region_dim-1)
    half_region = int(region_dim/2)
    data = np.zeros((height*width,3*region_dim*region_dim), float)
    for lyi in range(0,region_dim):
        for lxi in range(0,region_dim):
            temp = crop_and_copy(img_dither_file,lxi,lyi)
            data[:,lyi*region_dim+lxi] = np.array(list(temp.getdata(0)))/255.0
            data[:,(lyi*region_dim+lxi)*2] = np.array(list(temp.getdata(1)))/255.0
            data[:,(lyi*region_dim+lxi)*3] = np.array(list(temp.getdata(2)))/255.0
            temp.close()

    img_dither_file.close()
    return data, width, height

def imgs_to_x_y_vecs(img_dither,img_orig,keep):
    #load
    img_dither_file = mirror_load(img_dither)
    img_orig_file = Image.open(img_orig)
    width, height = img_orig_file.size
    half_region = int(region_dim/2)

    indicies = np.arange(width*height)
    np.random.shuffle(indicies)
    indicies = indicies[:keep]

    data = np.zeros((len(indicies),3*(region_dim*region_dim+1)), float)
    for lyi in range(0,region_dim):
        for lxi in range(0,region_dim):
            temp = crop_and_copy(img_dither_file,lxi,lyi)
            #print(list(temp.getdata(0)))
            data[:,lyi*region_dim+lxi] = (np.array(list(temp.getdata(0)))/255.0)[indicies]
            data[:,(lyi*region_dim+lxi)*2] = (np.array(list(temp.getdata(1)))/255.0)[indicies]
            data[:,(lyi*region_dim+lxi)*3] = (np.array(list(temp.getdata(2)))/255.0)[indicies]
            temp.close()

    data[:,region_dim*region_dim*3] = (np.array(list(img_orig_file.getdata(0))))[indicies].tolist()
    data[:,region_dim*region_dim*3+1] = (np.array(list(img_orig_file.getdata(1))))[indicies].tolist()
    data[:,region_dim*region_dim*3+2] = (np.array(list(img_orig_file.getdata(2))))[indicies].tolist()

    img_dither_file.close()
    img_orig_file.close()

    #np.random.shuffle(data)
    return data

def load_data(percentage):
    """
    loads training and testing data
    """
    #We will presume the files in both directories have the same names.
    files = os.listdir(img_orig_folder)
    data = np.empty((0,3*(region_dim*region_dim+1)), float)
    count = 0

    keep = int(1000*1000*0.01)
    np.random.shuffle(files)
    files = files[:int(percentage*len(files))]

    for name in files:
        count += 1
        print("Getting {} ({} of {})".format(name,count,len(files)))
        data = np.append(data,imgs_to_x_y_vecs(img_dither_folder+name,img_orig_folder+name,keep),axis=0)

    np.random.shuffle(data)

    X = data[:,:region_dim*region_dim*3]
    Y = data[:,region_dim*region_dim*3:]
    return X, Y

def train(X,Y):
    reg = ann.LiamANN(layers=(len(X[0]),int(0.5*len(X[0]))),tol=0.1,alpha=1e-3,max_iter=200,X=X,Y=Y)
    #reg = pickle.load( open( "reg.p", "rb" ) )
    reg.fit(X,Y)
    return reg

def train_epoch(X,Y,pca):
    #reg = ann.LiamANN(layers=(len(X[0]),int(0.5*len(X[0]))),tol=0.1,alpha=0.5,max_iter=200,X=X,Y=Y)
    reg = pickle.load( open( "reg.p", "rb" ) )
    count = 0
    while 1==1:
        count += 1
        reg.fit_epoch(X, Y)
        undither("./data/dither/1.gif","./resolved-iteration({}).png".format(count),reg,pca)
    #print(reg.coefs_)
    return reg

def undither(img_dither,img_out,reg,pca):
    data, width, height = img_to_vecs(img_dither)
    data = pca.transform(data,no_components)
    outputimage = Image.new('RGB',(width,height),0)
    raw = reg.predict(data).astype(int)
    formatd = list(zip(raw[:,0],raw[:,1],raw[:,2]))
    outputimage.putdata(formatd)
    #outputimage = outputimage.filter(ImageFilter.Kernel((3,3), [1]*9))
    #outputimage = outputimage.filter(ImageFilter.SMOOTH)
    outputimage.save(img_out)

print("Loading data...")
X,Y = load_data(1.0)
print("Running PCA...")
no_components = region_dim*region_dim
pca = pca.LiamPCA()
pca.fit(X)
X = pca.transform(X,no_components)
print("Dumping PCA...")
pickle.dump( pca, open( "pca.p", "wb" ) )
print("Training...")
reg = train(X,Y)
print("Dumping network...")
pickle.dump( reg, open( "reg.p", "wb" ) )
print("Test...")
undither("./data/dither/2.gif","./test-result.png",reg,pca)
