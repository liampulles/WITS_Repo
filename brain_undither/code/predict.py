import numpy as np
import pickle
import sys
import unmask
import ann
import pca
from PIL import Image

#Must be odd!
region_dim = 7

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
    #print("check",xi,yi)
    return data, width, height

def undither(img_dither,img_out,reg,pca):
    data, width, height = img_to_vecs(img_dither)
    data = pca.transform(data,no_components)
    outputimage = Image.new('RGB',(width,height),0)
    #pixelsout = outputimage.load()
    raw = reg.predict(data).astype(int)
    outputimage.putdata(list(zip(raw[:,0],raw[:,1],raw[:,2])))
    #outputimage = outputimage.filter(ImageFilter.Kernel((3,3), [1]*9))
    #outputimage = outputimage.filter(ImageFilter.SMOOTH)
    outputimage.save(img_out)

no_components = region_dim*region_dim
print("Loading PCA...")
pca = pickle.load( open( "pca-ours-final.p", "rb" ) )
print("Load Network...")
reg = pickle.load( open( "reg-ours-final.p", "rb" ) )
print("Test...")
print(sys.argv)
undither(sys.argv[1],"{}-out.png".format(sys.argv[1]),reg,pca)
