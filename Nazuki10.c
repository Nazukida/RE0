#include <stdio.h>
#include <float.h>

int main() {
    long double ld = 1234567890123456789.123456789L;

    printf("Long double value with %Lf format: %Lf\n", ld);
    printf("Long double value with %Le format: %Le\n", ld);

    // 显示精度信息
    printf("\nPrecision information:\n");
    printf("Long double precision: %d decimal digits\n", (int)log10(LDBL_EPSILON) * -1);

    return 0;
}