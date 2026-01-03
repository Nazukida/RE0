//f(x)=x^5-x+1,x=-1
#include<stdio.h>
int fx(float x, float y){
    y = x*x*x*x*x - x + 1;
    return y;
}
int dfx(float x, float y){
    y = 5*x*x*x*x - 1;
    return y;
}
int main(){
    float x = -1.0;
    float x_change = x;
    float y_change;
    float dy_change;
    for (;;)
    {
        x_change = x_change - fx(x_change, y_change)/dfx(x_change, dy_change);
        if (y_change < 0)
        {
            break;
        }
        
    }
    printf("%.4f",x_change);
    return 0;
    
}