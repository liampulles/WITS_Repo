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

//Define texture
texture<float, 2, cudaReadModeElementType> tex;

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

__global__ void singlePixel(float* out, float* kernel, int width, int kwidth)
{
    int i = (blockIdx.x * blockDim.x) + threadIdx.x;
    int j = (blockIdx.y * blockDim.y) + threadIdx.y;
    float total = 0;
    for (int v=0; v<kwidth; v++)
    {
        for (int u=0; u<kwidth; u++)
        {
            total += tex2D(tex, i+u, j+v) * kernel[v*kwidth + u];
        }
    }
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
    float * temp = (float *)malloc(bigSize);
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

    // Allocate and copy image, bind texture
    cudaArray *cuArray;
    cudaChannelFormatDesc channelDesc =
        cudaCreateChannelDesc(32, 0, 0, 0, cudaChannelFormatKindFloat);
    checkCudaErrors(cudaMallocArray(&cuArray,
                                    &channelDesc,
                                    width+bwidth,
                                    height+bwidth));
    checkCudaErrors(cudaMemcpyToArray(cuArray,
                                      0,
                                      0,
                                      in,
                                      bigSize,
                                      cudaMemcpyHostToDevice));
    tex.normalized = false;
    tex.filterMode = cudaFilterModePoint;
    checkCudaErrors(cudaBindTextureToArray(tex, cuArray, channelDesc));

    // Perform Convolution
    int threadsx = 16;
    int threadsy = 16;
    dim3 threadsPerBlock(threadsx, threadsy);
    int blockx = width/threadsx;
    int blocky = height/threadsy;
    if (blockx%threadsx != 0) blockx++;
    if (blocky%threadsy != 0) blocky++;
    dim3 numBlocks(blockx,blocky);
    if (strcmp(overhead,"false")==0) singlePixel<<<numBlocks,threadsPerBlock>>>(dData, cuKernel, width, kwidth);

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
    checkCudaErrors(cudaUnbindTexture(tex));
    checkCudaErrors(cudaFreeArray(cuArray));
    checkCudaErrors(cudaFree(cuKernel));
    free(kernel);
    free(imagePath);
    free(out);
    free(in);
}
