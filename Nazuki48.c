//zwqsb, bu hui xie cheng xu
#include<stdio.h>
#include<math.h>
int main(){
    double x, y;
    scanf("%lf", &x);
    if (x < 0)
    {
        y = pow(x, 5) + 2 * x + 1 / x;
        printf("%.2f", y);
    }else
    {
        y = sqrt(x);
        printf("%.2f", y);
    }
    return 0;
    
}