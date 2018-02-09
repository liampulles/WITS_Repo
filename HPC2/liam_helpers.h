#ifndef LIAM_HELPERS
#define LIAM_HELPERS

#include <string.h>

int kernelWidth(const char* maskName) {
    if (strcmp(maskName,"edge3x3") == 0) return 3;
    if (strcmp(maskName,"sharpen3x3") == 0) return 3;
    if (strcmp(maskName,"emboss3x3") == 0) return 3;
    if (strcmp(maskName,"bench3x3") == 0) return 3;
    if (strcmp(maskName,"bench5x5") == 0) return 5;
    if (strcmp(maskName,"gauss5x5") == 0) return 5;
    return -1;
}

void loadKernel(const char* maskName, float* k)
{
    if (strcmp(maskName,"edge3x3") == 0)
    {
        *k++ = -1.0f; *k++ = 0.0f; *k++ = 1.0f;
        *k++ = -2.0f; *k++ = 0.0f; *k++ = 2.0f;
        *k++ = -1.0f; *k++ = 0.0f; *k++ = 1.0f;
        return;
    }
    if (strcmp(maskName,"sharpen3x3") == 0)
    {
        *k++ = -1.0f; *k++ = -1.0f; *k++ = -1.0f;
        *k++ = -1.0f; *k++ = 9.0f;  *k++ = -1.0f;
        *k++ = -1.0f; *k++ = -1.0f; *k++ = -1.0f;
        return;
    }
    if (strcmp(maskName,"emboss3x3") == 0)
    {
        *k++ = 2.0f; *k++ = 0.0f;  *k++ = 0.0f;
        *k++ = 0.0f; *k++ = -1.0f; *k++ = 0.0f;
        *k++ = 0.0f; *k++ = 0.0f;  *k++ = -1.0f;
        return;
    }
    if (strcmp(maskName,"bench3x3") == 0)
    {
        *k++ = 1.0f/9; *k++ = 1.0f/9; *k++ = 1.0f/9;
        *k++ = 1.0f/9; *k++ = 1.0f/9; *k++ = 1.0f/9;
        *k++ = 1.0f/9; *k++ = 1.0f/9; *k++ = 1.0f/9;
        return;
    }
    if (strcmp(maskName,"gauss5x5") == 0)
    {
        *k++ = 1.0f/273;*k++ = 4.0f/273;*k++ = 7.0f/273;*k++ = 4.0f/273;*k++ = 1.0f/273;
        *k++ = 4.0f/273;*k++ = 16.0f/273;*k++ = 26.0f/273;*k++ = 16.0f/273;*k++ = 4.0f/273;
        *k++ = 7.0f/273;*k++ = 26.0f/273;*k++ = 41.0f/273;*k++ = 26.0f/273;*k++ = 7.0f/273;
        *k++ = 4.0f/273;*k++ = 16.0f/273;*k++ = 26.0f/273;*k++ = 16.0f/273;*k++ = 4.0f/273;
        *k++ = 1.0f/273;*k++ = 4.0f/273;*k++ = 7.0f/273;*k++ = 4.0f/273;*k++ = 1.0f/273;
        return;
    }
    if (strcmp(maskName,"bench5x5") == 0)
    {
        *k++ = 1.0f/25; *k++ = 1.0f/25;*k++ = 1.0f/25;*k++ = 1.0f/25;*k++ = 1.0f/25;
        *k++ = 1.0f/25; *k++ = 1.0f/25;*k++ = 1.0f/25;*k++ = 1.0f/25;*k++ = 1.0f/25;
        *k++ = 1.0f/25; *k++ = 1.0f/25;*k++ = 1.0f/25;*k++ = 1.0f/25;*k++ = 1.0f/25;
        *k++ = 1.0f/25; *k++ = 1.0f/25;*k++ = 1.0f/25;*k++ = 1.0f/25;*k++ = 1.0f/25;
        *k++ = 1.0f/25; *k++ = 1.0f/25;*k++ = 1.0f/25;*k++ = 1.0f/25;*k++ = 1.0f/25;
        return;
    }
        k = NULL;
}

float clamp(float d, float min, float max) {
    float t = d < min ? min : d;
    return t > max ? max : t;
}

__device__ float gpuclamp(float d, float min, float max) {
    float t = d < min ? min : d;
    return t > max ? max : t;
}

#endif
