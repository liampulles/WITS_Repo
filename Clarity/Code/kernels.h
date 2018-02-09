/*
 * This header describes the kernel class.
 * The kernel class is used to easily generate various kernel matrices.
 */

#ifndef KERNELS_H
#define KERNELS_H

#include "matrix.h"
#include <string.h>

class Kernels {
 public:
  Kernels();
  static Matrix* genMatrix(int size, std::string type);
};

#endif
