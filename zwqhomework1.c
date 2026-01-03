//zwqsb
#include<stdio.h>
int main(){
    int n;
    int g, s, q, w;
    scanf("%d", &n);//5 number
    w = n / 10000;
    g = n % 10;
    q = (n % 10000) / 1000;
    s = n / 10 % 10;
    if (w == g && q == s)
    {
        printf("%d", n);
    }else
    {
        printf("no");
    }
    return 0;
    
}