#include<stdio.h>
#include<float.h>
int main(){
    double d_third=10./3.0;
    float f_third=10./3.0;
    printf("%.6f",f_third);
    printf(" %.12f",f_third);
    printf(" %.16f",f_third);
    printf(" %.6lf",d_third);
    printf(" %.12lf",d_third);
    printf(" %.16lf",d_third);
    printf(" %d",FLT_DIG);
    printf(" %d",DBL_DIG);

    return 0;
}