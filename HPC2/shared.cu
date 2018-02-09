// Includes, system
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
// Includes CUDA
#include <cuda_runtime.h>
#include <helper_functions.h>    // includes cuda.h and cuda_runtime_api.h
#include <helper_cuda.h>         // helper functions for CUDA error check
// Liam helper functions
#include "liam_helpers.h"

const char *imageFilename = "lena_bw.pgm";
const char *maskName = "edge3x3";
const char *sampleName = "naive";
const char *bench = "false";
const char *overhead = "false";

//Define threads per block
#define THREADS_X 16
#define THREADS_Y 16

void runConvolution(int argc, char **argv);

int main(int argc, char **argv)
{

    // Process command-line arguments
    if (argc > 1)
    {
        if (checkCmdLineFlag(argc, (const char **) argv, "input"))
        {
            getCmdLineArgumentString(argc,
                                     (const char **) argv,
                                     "input",
                                     (char **) &imageFilename);
        }
        if (checkCmdLineFlag(argc, (const char **) argv, "mask"))
        {
            getCmdLineArgumentString(argc,
                                     (const char **) argv,
                                     "mask",
                                     (char **) &maskName);
        }
        if (checkCmdLineFlag(argc, (const char **) argv, "bench"))
        {
            getCmdLineArgumentString(argc,
                                     (const char **) argv,
                                     "bench",
                                     (char **) &bench);
        }
        if (checkCmdLineFlag(argc, (const char **) argv, "overhead"))
        {
            getCmdLineArgumentString(argc,
                                     (const char **) argv,
                                     "overhead",
                                     (char **) &overhead);
        }
    }

    if (strcmp(bench,"false")!=0) {
        //Need to make some images to process
        const char *masks[2];
        masks[0] = "bench3x3";
        masks[1] = "bench5x5";
        for (int k=0; k<2; k++) {
          maskName = masks[k];
          for (int i=512; i<6200; i+=512) {
            float* test = (float *)malloc(i*i*sizeof(float));
            time_t t;
            srand((unsigned)time(&t));
            for (int j=0; j<i*i; j++) {\
                test[j] = rand()/(RAND_MAX*1.0f);
            }
            imageFilename = "test.pgm";
            sdkSavePGM(imageFilename, test, i, i);
            runConvolution(argc,argv);
          }
        }
    }
    else {
      printf("%s starting...\n", sampleName);
      runConvolution(argc, argv);
    }
    cudaDeviceReset();
    return 0;
}

__global__ void singlePixel(float* in, float* out, float* kernel, int width, int kwidth)
{
    extern __shared__ float s[];
    //Global coordinates
    int i = (blockIdx.x * blockDim.x) + threadIdx.x;
    int j = (blockIdx.y * blockDim.y) + threadIdx.y;
    //position of block's 1st element
    int startx = blockIdx.x * blockDim.x;
    int starty = blockIdx.y * blockDim.y;

    //Put stuff into shared memory
    int half = kwidth/2;
    int bwidth = half*2;
    int swidth = blockDim.x+bwidth;
    int iwidth = width+bwidth;
    int endx = half+startx+blockDim.x;
    int endy = half+starty+blockDim.y;
    /* Put in the middle, excluding the borders */
    s[(threadIdx.y+half)*(swidth)+(threadIdx.x+half)] = in[(j+half)*(iwidth)+(i+half)];
    /*Add border sides */
    //Note: The unfortunate complexity of indices here is due to the mapping of
    //      a portion of the image to a local block, which requires some
    //      coordinate shifting.
    //* Top */
    if (threadIdx.y == 0) {
      for (int k=0; k<half; k++) {
        s[k*(swidth)+(threadIdx.x+half)] = in[(starty+k)*(iwidth)+(i+half)];
      }
    }
    //* Bottom */
    else if (threadIdx.y == blockDim.y-1) {
      for (int k=0; k<half; k++) {
        s[(half+blockDim.y+k)*(swidth)+(threadIdx.x+half)] = in[(endy+k)*(iwidth)+(i+half)];
      }
    }
    //* Left */
    if (threadIdx.x == 0) {
      for (int k=0; k<half; k++) {
        s[(threadIdx.y+half)*(swidth)+k] = in[(j+half)*(iwidth)+(startx+k)];
      }
    }
    //* Right */
    else if (threadIdx.x == blockDim.x-1) {
      for (int k=0; k<half; k++) {
        s[(threadIdx.y+half)*(swidth)+(half+blockDim.x+k)] = in[(j+half)*(iwidth)+(endx+k)];
      }
    }
    //Add corners
    if ((threadIdx.x == 1)&&(threadIdx.y == 1)) {
      for (int k=0; k<half; k++) {
        for (int l=0; l<half; l++) {
          s[k*(swidth)+l] = in[(k+starty)*(iwidth)+(startx+l)];
        }
      }
    }
    else if ((threadIdx.x == blockDim.x-2)&&(threadIdx.y == 1)) {
      for (int k=0; k<half; k++) {
        for (int l=0; l<half; l++) {
          s[k*(swidth)+(half+blockDim.x+l)] = in[(k+starty)*(iwidth)+(endx+l)];
        }
      }
    }
    else if ((threadIdx.x == 1)&&(threadIdx.y == blockDim.y-2)) {
      for (int k=0; k<half; k++) {
        for (int l=0; l<half; l++) {
          s[(k+half+blockDim.y)*(swidth)+l] = in[(k+endy)*(iwidth)+(startx+l)];
        }
      }
    }
    else if ((threadIdx.x == blockDim.x-2)&&(threadIdx.y == blockDim.y-2)) {
      for (int k=0; k<half; k++) {
        for (int l=0; l<half; l++) {
          s[(k+half+blockDim.y)*(swidth)+(half+blockDim.x+l)] = in[(k+endy)*(iwidth)+(endx+l)];
        }
      }
    }
    __syncthreads();

    //Do convolution
    float total = 0;
    for (int v=0; v<kwidth; v++)
    {
        for (int u=0; u<kwidth; u++)
        {
            //total += in[(j+v)*(width+kwidth) + (i+u)] * kernel[v*kwidth + u];
            total += s[(threadIdx.y+v)*(swidth) + (threadIdx.x+u)] * kernel[v*kwidth + u];
        }
    }
    //printf("%f\n",s[181]);
    out[j*width + i] = gpuclamp(total,0.0f,1.0f);
}

void runConvolution(int argc, char **argv)
{
    if (strcmp(bench,"false")==0) int devID = findCudaDevice(argc, (const char **) argv);

    // Load image from disk
    float *in = NULL;
    unsigned int width, height;
    char *imagePath = sdkFindFilePath(imageFilename, argv[0]);
    if (imagePath == NULL)
    {
        printf("Unable to source image file: %s\n", imageFilename);
        exit(EXIT_FAILURE);
    }
    sdkLoadPGM(imagePath, &in, &width, &height);
    unsigned int size = width * height * sizeof(float);
    if (strcmp(bench,"false")==0) printf("Loaded '%s', %d x %d pixels\n", imageFilename, width, height);

    //Create Timer
    StopWatchInterface *timer = NULL;
    checkCudaErrors(cudaDeviceSynchronize());
    sdkCreateTimer(&timer);
    sdkStartTimer(&timer);

    //Get Convolution array
    float* kernel;
    int kwidth = kernelWidth(maskName);
    if (kwidth == -1)
    {
        printf("Invalid mask name: %s\n", maskName);
        exit(EXIT_FAILURE);
    }
    kernel = (float *)malloc(sizeof(float)*kwidth*kwidth);
    loadKernel(maskName, kernel);

    //Create Border
    int half = kwidth/2;
    int bwidth = half*2;
    int bigSize = (width+bwidth)*(height+bwidth)*sizeof(float);
    float *temp = (float *)malloc(bigSize);
    for (int y=0; y<height; y++) {
        for (int x=0; x<width; x++)
        {
            temp[(y+half)*(width+bwidth) + (x+half)] = in[y*height+x];
        }
    }
    /* Initialize edges */
    for (int j=0; j<half; j++) {
      for (int i=0; i<width+bwidth; i++) {
        temp[j*(width+bwidth)+i] = 0.0f;
        temp[(width+bwidth-(1+j))*(width+bwidth)+(i+j)] = 0.0f;
        temp[i*(width+bwidth)+j] = 0.0f;
        temp[i*(width+bwidth)+(width+bwidth-(1+j))] = 0.0f;
      }
    }
    free(in);
    in=temp;

    // Allocate memory for result
    float *out = NULL;
    out = (float *)malloc(size);

    // Allocate and initialize device memory for result
    float *dData = NULL;
    checkCudaErrors(cudaMalloc((void **) &dData, size));
    checkCudaErrors(cudaMemset(dData, 0, size));

    //Allocate and copy kernel
    float *cuKernel;
    checkCudaErrors(cudaMalloc((void **) &cuKernel, kwidth*kwidth*sizeof(float)));
    checkCudaErrors(cudaMemcpy(cuKernel,
                               kernel,
                               kwidth*kwidth*sizeof(float),
                               cudaMemcpyHostToDevice));

    // Allocate and copy image
    float *cuArray;
    checkCudaErrors(cudaMalloc((void **) &cuArray, bigSize));
    checkCudaErrors(cudaMemcpy(cuArray,
                               in,
                               bigSize,
                               cudaMemcpyHostToDevice));

    // Perform Convolution
    dim3 threadsPerBlock(THREADS_X, THREADS_Y);
    int blockx = width/THREADS_X;
    int blocky = height/THREADS_Y;
    if (blockx%THREADS_X != 0) blockx++;
    if (blocky%THREADS_Y != 0) blocky++;
    dim3 numBlocks(blockx,blocky);
    int sharedmemsize = (THREADS_X+bwidth)*(THREADS_Y+bwidth)*sizeof(float);
    if (strcmp(overhead,"false")==0) singlePixel<<<numBlocks,threadsPerBlock,sharedmemsize>>>(cuArray, dData, cuKernel, width, kwidth);

    // Copy back results
    checkCudaErrors(cudaMemcpy(out,
                               dData,
                               size,
                               cudaMemcpyDeviceToHost));

    //Read timer, print stats
    checkCudaErrors(cudaDeviceSynchronize());
    sdkStopTimer(&timer);
    int flo = 2*width*height*kwidth*kwidth;
    if (strcmp(bench,"false")==0) {
      printf("Processing time: %f (ms)\n", sdkGetTimerValue(&timer));
      printf("Floating Point Operations: %d\n",flo);
      printf("GFLOPS: %f\n", (flo/(sdkGetTimerValue(&timer)/1000))/1000000000);
    }
    else {
      printf("%d,%d,%f,%d,%f\n",width*width,kwidth*kwidth,sdkGetTimerValue(&timer),flo,(flo/(sdkGetTimerValue(&timer)/1000))/1000000000);
    }
    sdkDeleteTimer(&timer);

    // Write result to file
    char outputFilename[1024];
    strcpy(outputFilename, imagePath);
    strcpy(outputFilename + strlen(imagePath) - 4, "_out.pgm");
    sdkSavePGM(outputFilename, out, width, height);
    if (strcmp(bench,"false")==0) printf("Wrote '%s'\n", outputFilename);

    checkCudaErrors(cudaFree(dData));
    checkCudaErrors(cudaFree(cuArray));
    checkCudaErrors(cudaFree(cuKernel));
    free(kernel);
    free(imagePath);
    free(out);
    free(in);
}
