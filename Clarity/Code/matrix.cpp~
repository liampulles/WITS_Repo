#ifndef MATRIX
#define MATRIX

#include "EasyBMP/EasyBMP.h"

class Matrix {
 public:
  Matrix(int** matrix_in, int width, int height);
  ~Matrix();
  int width;
  int height;
  int[][] matrix;

  static void kernel(Matrix* matrix, RGB* source, int x, int y);
  static RGB* convolution(Matrix* matrix, RGB* source);
  static void edge_extrapolate_source(RGB* source);
  static RGBAPixel* edge_extrapolate_pixel(RGB* source, int x, int y);
};

#endif
