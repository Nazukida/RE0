#include<stdio.h>
int main(){
    
    //bianliang
    int in,again;
    printf("Please enter an integer____\b\b\b\b");
    scanf("%d",&in);
    again=0;

    while (again/*输出10次的条件*/< 10)
    {
        
        printf("%d\n",++in);
        
        again++;
    }
    
    

}