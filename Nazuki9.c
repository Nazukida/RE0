//用于对浮点数据关键字精度的测试
#include <stdio.h>
#include <float.h>

int main() {
    float f = 123456.789f;
    double d = 123456789.123456789;
    long double ld = 1234567890123456789.123456789L;
    printf("Float value: %f\n", f);
    printf("Double value: %lf\n", d);
    printf("Long double value: %Lf\n", ld);

    // 显示精度信息
    printf("\nPrecision information:\n");
    printf("Float precision: %d decimal digits\n", (int)log10(FLT_EPSILON) * -1);
    printf("Double precision: %d decimal digits\n", (int)log10(DBL_EPSILON) * -1);
    printf("Long double precision: %d decimal digits\n", (int)log10(LDBL_EPSILON) * -1);

    return 0;
}