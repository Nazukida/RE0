#include<stdio.h>
int main(void)
{
    int www;
    float ppp,ooo;
    www=2147483647;
    ppp=2147483647.1;
    ooo=1.000001;
    
    printf("%d\n",www+1);
    printf("%f\n",ppp);
    printf("%f\n",ooo/2);

    return 0;
}