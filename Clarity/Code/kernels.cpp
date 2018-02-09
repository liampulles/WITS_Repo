/*
 * See kernels.h for the class header.
 */

#include "kernels.h"
#include "matrix.h"
#include <string.h>

Kernels::Kernels() {}
/* Generate a kernel matric object. */
Matrix* Kernels::genMatrix(int size, std::string type) {
  int divisor;
  // Make a blank square 2d array.
  int** kern = new int*[size];
  for(int i=0; i < size; ++i) {
    kern[i] = new int[size];
    for (int j=0; j<size; j++) {
      kern[i][j] = 0;
    }
  }

  //Names are self explanatory really.
  if (size==3) {
    if (type=="box_blur") {
      divisor=9;
      kern[0][0] = 1; kern[0][1] = 1; kern[0][2] = 1;
      kern[1][0] = 1; kern[1][1] = 1; kern[1][2] = 1; 
      kern[2][0] = 1; kern[2][1] = 1; kern[2][2] = 1;
    }
    if (type=="slight_blur") {
      divisor=9;
      kern[0][0] = 0; kern[0][1] = 1; kern[0][2] = 0;
      kern[1][0] = 1; kern[1][1] = 5; kern[1][2] = 1; 
      kern[2][0] = 0; kern[2][1] = 1; kern[2][2] = 0;
    }
    if (type=="noise") {
      divisor=1;
      kern[0][0] = 0; kern[0][1] = -1; kern[0][2] = 0;
      kern[1][0] = -1; kern[1][1] = 4; kern[1][2] = -1; 
      kern[2][0] = 0; kern[2][1] = -1; kern[2][2] = 0;
    }
    if (type=="slight_sharpen") {
      divisor=16;
      kern[0][0] = 0; kern[0][1] = -1; kern[0][2] = 0;
      kern[1][0] = -1; kern[1][1] = 20; kern[1][2] = -1; 
      kern[2][0] = 0; kern[2][1] = -1; kern[2][2] = 0;
    }
  }
  if (size==5) {
    //This is the one we used for our report.
    if (type=="gaussian_blur") {
      divisor=256;
      kern[0][0] = 1; kern[0][1] = 4; kern[0][2] = 6; kern[0][3] = 4; kern[0][4] = 1;
      kern[1][0] = 4; kern[1][1] = 16; kern[1][2] = 24; kern[1][3] = 16; kern[1][4] = 4;
      kern[2][0] = 6; kern[2][1] = 24; kern[2][2] = 36; kern[2][3] = 24; kern[2][4] = 6;
      kern[3][0] = 4; kern[1][1] = 16; kern[3][2] = 24; kern[1][3] = 16; kern[3][4] = 4;
      kern[4][0] = 1; kern[4][1] = 4; kern[4][2] = 6; kern[4][3] = 4; kern[4][4] = 1;
    }
    if (type=="gaussian_blur2") {
      divisor=273;
      kern[0][0] = 1; kern[0][1] = 4; kern[0][2] = 7; kern[0][3] = 4; kern[0][4] = 1;
      kern[1][0] = 4; kern[1][1] = 16; kern[1][2] = 26; kern[1][3] = 16; kern[1][4] = 4;
      kern[2][0] = 7; kern[2][1] = 26; kern[2][2] = 41; kern[2][3] = 26; kern[2][4] = 7;
      kern[3][0] = 4; kern[1][1] = 16; kern[3][2] = 26; kern[1][3] = 16; kern[3][4] = 4;
      kern[4][0] = 1; kern[4][1] = 4; kern[4][2] = 7; kern[4][3] = 4; kern[4][4] = 1;
    }
    if (type=="box_blur") {
      divisor=25;
      kern[0][0] = 1; kern[0][1] = 1; kern[0][2] = 1; kern[0][3] = 1; kern[0][4] = 1;
      kern[1][0] = 1; kern[1][1] = 1; kern[1][2] = 1; kern[1][3] = 1; kern[1][4] = 1;
      kern[2][0] = 1; kern[2][1] = 1; kern[2][2] = 1; kern[2][3] = 1; kern[2][4] = 1;
      kern[3][0] = 1; kern[1][1] = 1; kern[3][2] = 1; kern[1][3] = 1; kern[3][4] = 1;
      kern[4][0] = 1; kern[4][1] = 1; kern[4][2] = 1; kern[4][3] = 1; kern[4][4] = 1;
    }
    if (type=="sharpen") {
      divisor=8;
      kern[0][0] = -1; kern[0][1] = -1; kern[0][2] = -1; kern[0][3] = -1; kern[0][4] = -1;
      kern[1][0] = -1; kern[1][1] = 2; kern[1][2] = 2; kern[1][3] = 2; kern[1][4] = -1;
      kern[2][0] = -1; kern[2][1] = 2; kern[2][2] = 8; kern[2][3] = 2; kern[2][4] = -1;
      kern[3][0] = -1; kern[1][1] = 2; kern[3][2] = 2; kern[1][3] = 2; kern[3][4] = -1;
      kern[4][0] = -1; kern[4][1] = -1; kern[4][2] = -1; kern[4][3] = -1; kern[4][4] = -1;
    }
  }
  return new Matrix(kern,size,size,divisor);
}
