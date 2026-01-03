#include<stdio.h>

int main()
{
    int arr[6]={1,1,4,5,1,4};
    int *pt=&arr[3];
    printf("%d\n",*pt);
    pt--;
    printf("%d\n",*pt);
    pt--;
    printf("%d\n",*pt);

    return 0;

}