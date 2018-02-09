# Compiling
Simply run make in the main directory. This presumes you've exported nvcc properly.
The result will be a number of executables which demontrate the different approaches.

# Usage
Without any parameters, the program will perform a 3x3 horizontal edge detection convolution on lena_bw.pgm in data, saving to lena_bw_out.pgm and overwriting if neccesary.

The program will also print to terminal some statistics about the execution time, number of effective floating point operations, and the GFLOPs.

The behaviour of the program can be overriden with the following console commands:

-input=<input_filename>:
Specify the name of a different .pgm file to take as input. It is not necesary to give the path in the name, the program will search for it under the main directory. The resulting image will be saved to the director of the input image, with the suffix "_out" (without quotes).
By default this uses lena.

-mask=<mask_name>
Specify the name of a different convolution mask to use. See liam_helpers.h for a list.
By default this uses a 2x2 horizontal edge detection filter.

-overhead=<true|false>
Specify whether to calculate the overhead, by not executing the kernel function. FLO and GFLOPS read outs are not valid in this case.
Default is false.

-bench=<true|false>
Will benchmark the implementation on random images of increasing size, and with a 3x3 and 5x5 filter (overrides -mask and -input). The results will be printed out in Comma Seperated Value form, with the following column names:
No. of Pixels,Kernel size,Execution Time (ms),FLO,GFLOPs
Default is false.