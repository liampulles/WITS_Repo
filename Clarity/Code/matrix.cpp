/*
 * See matrix.h for the class header.
 * A high level description of how these functions work is given in
 * section 2 of the report.
 */
#include "EasyBMP/EasyBMP.h"
#include "matrix.h"
#include <omp.h>

/* Constructor for the matrix class. */
/* matrix_in is on the heap. */
Matrix::Matrix(int **matrix_in, int wid, int hei, int div) {
  mat = matrix_in;
  width = wid;
  height = hei;
  divisor = div;
}

/* Destructor for the matrix class. */
Matrix::~Matrix() {
  for (int i=0; i<width; i++) {
    delete mat[i];
  }
  delete mat;
}

/* Kernel function */
/* Basically we have avoided passing in the Matrix object as a whole by passing in the matrix, div, width*/
void Matrix::kernel(int mat[][7], int div, int width, BMP* source, BMP* output, int x, int y) {
  //Need to use temporary variables because result of kernel may exceed 255 or go below 0.
  int Red = 0;
  int Green = 0;
  int Blue = 0;
  int border = (width-1)/2;
  for(int i = -border; i<=border; i++) {
    for(int j = -border; j<=border; j++) {
      Red = Red + Matrix::edge_extrapolate_pixel(source,x+i,y+j)->Red * mat[i+border][j+border];
      Blue = Blue + Matrix::edge_extrapolate_pixel(source,x+i,y+j)->Blue * mat[i+border][j+border];
      Green = Green + Matrix::edge_extrapolate_pixel(source,x+i,y+j)->Green * mat[i+border][j+border];
    }
  }

  //EasyBMP will automatically clamp these values to the range 0-255, if neccesary.
  (*output)(x,y)->Red = Red/div; //divide by divisor
  (*output)(x,y)->Blue = Blue/div;
  (*output)(x,y)->Green = Green/div;
}

/* Serial version of the convolution function. */
BMP* Matrix::convolution(Matrix* matrix, BMP* source) {
  //Make output canvas
  BMP* output = new BMP();

  int tempmat[7][7];
  for (int l=0; l<matrix->width; l++) {
    for (int o=0; o<matrix->height; o++) {
      tempmat[l][o] = matrix->mat[l][o];
    }
  }
  int width = matrix->width;
  int div = matrix->divisor;

  
  //Get dimensions fom source
  int picWidth = source->TellWidth(); 
  int picHeight = source->TellHeight(); 

  output->SetSize( picWidth , picHeight); 
  //set outputs bit depth to 24 since we're using RGB 8bit+8bit+8bit=24bit
  output->SetBitDepth(24); 

   for (int i = 0; i < picWidth; ++i)
   {
     for (int j = 0; j < picHeight; ++j) 
     { 
       kernel(tempmat,div,width,source,output,i,j);
     } 
   }
 
    //Return the final BMP

   return output;
}

/* Parallel version of the convolution function  */
BMP* Matrix::convolution_parallel(Matrix* matrix, BMP* source, int n) {
  int tempmat[7][7];
  for (int l=0; l<matrix->width; l++) {
    for (int o=0; o<matrix->height; o++) {
      tempmat[l][o] = matrix->mat[l][o];
    }
  }
  int width = matrix->width;
  int div = matrix->divisor;
  
  //Make output canvas
  BMP* output = new BMP();

  //Get dimensions fom source
  int picWidth = source->TellWidth(); 
  int picHeight = source->TellHeight(); 

  output->SetSize(picWidth, picHeight); 
  //set outputs bit depth to 24 since we're using RGB 8bit+8bit+8bit=24bit
  output->SetBitDepth(24);

  int i, j, k;
  omp_set_num_threads(n);
#pragma omp parallel for schedule(dynamic,1), private(k,i), firstprivate(tempmat,width,div,picWidth), shared(source,output)
  for (j=0; j<picWidth/(width*2); j++) {
    for (i=j*width*2; i<(j+1)*width*2; i++) {
      for (k=0; k<picHeight; k++) {
	kernel(tempmat,div,width,source,output,i,k);
      }
    }
  }
  
  /* Do the remainder of the image on the right */
  for (j=(picWidth/(width*2))*(width*2); j<picWidth; j++) {
    for (k=0; k<picHeight; k++) {
      kernel(tempmat,div,width,source,output,j,k);
    }
  }

  return output;
}

/* Edge extrapolation function */
RGBApixel* Matrix::edge_extrapolate_pixel(BMP* source, int x, int y) {
  if ((x>=0)&&(x<source->TellWidth())&&(y>=0)&&(y<source->TellHeight())) {
    return (*source)(x,y);
  }
  else {
    //On the left
    if (x<0) {
      //Top-left.
      if (y<0) {
	return (*source)(0,0);
      }
      //Bottom-left
      if (y>=(*source).TellHeight()) {
	return (*source)(0,(*source).TellHeight()-1);
      }
      //Left side somewhere
      return (*source)(0,y);
    }
    //On the right
    if (x>=(*source).TellWidth()) {
      //Top-right
      if (y<0) {
	return (*source)(source->TellWidth()-1,0);
      }
      //Bottom-right
      if (y>=source->TellHeight()) {
	return (*source)(source->TellWidth()-1,source->TellHeight()-1);
      }
      //Right side somewhere
      return (*source)(source->TellWidth()-1,y);
    }
    //On the top
    if (y<0) {
      //Can only be on the top somewhere
      return (*source)(x,0);
    }
    //Can only be on the bottom somewhere
    return (*source)(x,source->TellHeight()-1);
  }
  //Should not be reached.
  return nullptr;
}
