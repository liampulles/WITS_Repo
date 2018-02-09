ID=-I inc
DEP=liam_helpers.h

convolution: serial naive shared constant texture

serial: serial.cu $(DEP)
	nvcc serial.cu $(ID) -o serial

naive: naive.cu $(DEP)
	nvcc naive.cu $(ID) -o naive

shared: shared.cu $(DEP)
	nvcc shared.cu $(ID) -o shared

constant: constant.cu $(DEP)
	nvcc constant.cu $(ID) -o constant

texture: texture.cu $(DEP)
	nvcc texture.cu $(ID) -o texture

clean:
	rm serial naive shared constant texture
