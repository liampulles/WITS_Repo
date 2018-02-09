/*
 * This header describes the matrix class
 * The matrix class is responsible for describing the kernel matrix
 * and functions which will perform the convolution process.
 */

#ifndef MATRIX
#define MATRIX

#include "EasyBMP/EasyBMP.h"

class Matrix {
 public:
  Matrix(int** matrix_in, int wid, int hei, int divisor);
  ~Matrix();
  int width;
  int height;
  int** mat;
  int divisor;

  static void kernel(int mat[][7], int div, int width, BMP* source, BMP* output, int x, int y);
  static BMP* convolution_parallel(Matrix* matrix, BMP* source, int n);
  static BMP* convolution(Matrix* matrix, BMP* source);
  static RGBApixel* edge_extrapolate_pixel(BMP* source, int x, int y);
};

#endif
