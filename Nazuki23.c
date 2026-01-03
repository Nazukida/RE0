#include<stdio.h>
int main(void)
{
    double second;
    int age;
    second=3.156E7L;
    printf("Now please enter your age__\b\b");
    scanf("%d",&age);
    printf("\n");
    printf("wow,you have already live on earth for %d year and that is %f second.\n",age,age*second);
    getchar();
    getchar();

    return 0;
}