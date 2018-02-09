[![Stories in Ready](https://badge.waffle.io/sl1msn1per/Clarity.svg?label=ready&title=Ready)](http://waffle.io/sl1msn1per/Clarity)

# Clarity
WITS Parallel Computing Project - Convolution filter

Prezi slides https://prezi.com/yuh92p337p7l

#How it could work
The way I see the program it could work as follows:
* from main() in main.cpp you load a bmp image using standard easybmp functions.
* from main() you create an instance of the matrix class. It takes a matrix**, a width and a height which describes a 5x5 , 3x3, etc. matrix. (remember that you use ** to pass 2d arrays in c++ and c).
* main() would then call the convolution() funcion from Matrix. It would pass the Matric object we just created and the BMP* object we loaded from file.
* convolution() would create an empty output BMP* with the same dimensions as source. It would then use something like a double for loop to iterate through wach pixel in source, then for each pixel it would get a new pixel (RGBAPixel*) by calling kernel on that pixel. It would store this new pixel in the output image and return that output at the end.
* kernel() would have to do the actual kernel for a pixel. It would thus have to figure out the range of pixels it needs from x,y, and Matrix*'s width and height fields. Then it does a calculation for r, g, and b for the x,y pixel. Where kernel would call source->(x,y), it should instead call edge_extrapolation_pixel(source,x,y). Then edge_extrapolation_pixel will figure out whether a pixel from the image can be returned or whether it would have to return one on the border (edge extrapolation).
* So now that edge_extrapolation_pixel(), kernel() and ultimatelly convolution() do all their jobs, we should result back at main() with a finnished image whcih we can save.