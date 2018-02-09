About the programs:

demoBW.cpp just converts any input image to black and white by naively averaging out a pixel's RGB value and setting it to white if the average is > than 127 (255/2 flored) otherwise it's set to black;

demoCol.cpp trys to act as an image filter... Similar to demoBW.cpp

Also, both programs take in 2 arguments, arg1 = source.BMP and arg2=outputName.BMP
Example,
./demoCol.o falls.BMP fallout.BMP

To compile demoBW.cpp:
g++ demoBW.cpp -o demoBW.o EasyBMP/EasyBMP.cpp

To compile demoCol.cpp:
g++ demoCol.cpp -o demoCol.o EasyBMP/EasyBMP.pp

Note, to avoid clutter the EasyBMP library is placed in its own directory and has to be refrenced appropriatly.