/*
 * This file contains the main() function which is executed.
 */
#include "EasyBMP/EasyBMP.h"
#include "matrix.h"
#include "kernels.h"
#include "omp.h"
#include <string.h>
using namespace std;

//Note: BMP* deletes itself at the end of scope.

int images_test(int argc, char* argv[]) {
  double start,end;
  double time;
  //Loop 10 times for accuracy
  int loop=10; 

  BMP* Background = new BMP(); 
  BMP* Output;
  Background->ReadFromFile(argv[1]); 
	
  //Use a helper function to create a matrix.
  Matrix* mat = Kernels::genMatrix(5,"gaussian_blur");

  //Do Parallel
  if(*argv[3]=='p' || *argv[3]=='P') {
    for(int i=0;i<loop;i++)
    {
      //We only measure the time taken to do the convolution of the whole image.
      start = omp_get_wtime();
      Output = Matrix::convolution_parallel(mat,Background,4);
      end = omp_get_wtime();

      time +=(end-start);
      cout<<i <<" : "<<time <<"(+"<<end-start<<")"<<endl;
    }
    cout<<"Execution Time (Parallel) : "<<(time/loop)<<endl;

  }

  //Do Serial
  else if(*argv[3]=='s' || *argv[3]=='S'){

    for(int i=0;i<loop;i++)
    {
      start = omp_get_wtime();
      Output = Matrix::convolution(mat,Background);
      end = omp_get_wtime();

      time+=(end-start);
      cout<<i <<" : "<<time <<"(+"<<end-start<<")"<<endl;
    }
    cout<<"Execution Time (Serial): "<<(time/loop)<<endl;
  }

  delete mat;
  //No need to save image.
  return 0;
}

int thread_test(int argc, char* argv[]) {
  double start,end;
  double time;

  //Loop 10 times for accuracy (per thread count)
  int loop=10;
  int threads_max=24;

  BMP* Background = new BMP(); 
  BMP* Output;

  Background->ReadFromFile(argv[1]); 

  Matrix* mat = Kernels::genMatrix(5,"gaussian_blur");

  //"0" is serial implementation
  for (int j=0; j<loop; j++) {
    start = omp_get_wtime();
    Output = Matrix::convolution(mat,Background);
    end = omp_get_wtime();

    time = (end-start);
    cout << 0 << ' ' << time << endl;
  }

  //Parallel implementation (1-...)
  for(int i=1;i<threads_max;i++)
  {
    for (int j=0; j<loop; j++) {
      start = omp_get_wtime();
      Output = Matrix::convolution_parallel(mat,Background,i);
      end = omp_get_wtime();

      time = (end-start);
      cout << i << ' ' << time << endl;
    }
  }

  delete mat;
  return 0;
}

int simple( int argc, char* argv[] )
{
  BMP* Background = new BMP(); 
  BMP* Output;

  Background->ReadFromFile(argv[1]); 

  Matrix* mat = Kernels::genMatrix(5,"gaussian_blur");

  double start,end;
  double time;

  //Do Parallel
  if(*argv[3]=='p' || *argv[3]=='P') {
    start = omp_get_wtime();
    Output = Matrix::convolution_parallel(mat,Background,4);
    end = omp_get_wtime();

    time +=(end-start);
    cout<<"Execution Time (Parallel) : "<<time<<endl;
  }
  //Do Serial
  else if(*argv[3]=='s' || *argv[3]=='S'){
    start = omp_get_wtime();
    Output = Matrix::convolution(mat,Background);
    end = omp_get_wtime();

    time+=(end-start);
    cout<<"Execution Time (Serial) : "<<time<<endl;
  }
  delete mat;	
	  
  //Save the image
  Output->WriteToFile(argv[2]);

  return 0;
}

//Arguments to the executable are as follows:
// 1: input filename
// 2: output filename
// 3: parallel or serial
// 4: Choice between 2 tests or straight run.
int main( int argc, char* argv[] ) 
{
  if (argc != 5) {
    printf("Number of arguments must be 4.\n");
    return 1;
  }
  string argv4 = argv[4];
  if (argv4=="thread") {
    return thread_test(argc,argv);
  }
  if (argv4=="simple") {
    return simple(argc,argv);
  }
  else if (argv4=="images") {
    return images_test(argc,argv);
  }
  else {
    printf("Argument \"%s\" (without quotes) not recognized.\n",argv[4]);
  }
  return 1; 
} 
