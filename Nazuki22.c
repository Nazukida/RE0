#include<stdio.h>//chapter3 practice
int main(void)
{
    float abc;
    abc=64.25;

    printf("Enter a floating-point value:%.2f\n",abc);
    printf("fixed-point notation:%f\n",abc);
    printf("exponential notation:%e\n",abc);
    printf("p notional:%a\n",abc);

    return 0;

}