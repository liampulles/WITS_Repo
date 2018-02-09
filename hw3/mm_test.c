/* A simple test harness for memory alloction. */
/* modified by Liam. (855442)*/
#include "mm_alloc.h"
#include <stdio.h>
int main(int argc, char **argv)
{ 
  int temp; 
  int* data1 = (int*) mm_malloc(18);
  int* data2 = (int*) mm_malloc(8);
  int* data3 = (int*) mm_malloc(20);
  int* data4 = (int*) mm_malloc(5);
  int* data5 = (int*) mm_malloc(17);
  data1[0] = 1;
  data2[0] = 20;
  data3[0] = 3;
  data4[0] = 4;
  data5[0] = 5;
  /* Let's see if it keeps space contiguous and allocates in gaps. */
  temp = (int)sbrk(0);
  mm_free(data2);
  mm_free(data3);
  mm_free(data4);
  data2 = (int*) mm_malloc(8);
  data3 = (int*) mm_malloc(20);
  data4 = (int*) mm_malloc(5);
  printf("malloc sanity test successful!%d\n", temp - (int)sbrk(0));
  /* returns 0, so yes! */
  return 0;
}
