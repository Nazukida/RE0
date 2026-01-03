#include<stdio.h>
const int M_PER_H=60;
int main(){
    int min,hour,latemin;
    min = 1;
    hour = 0;
    latemin = 0;

    while (min > 0)
    {
        printf("please enter the minutes in integer(press 0 to stop)____\b\b\b\b");
        scanf("%d",&min);
        hour = min / M_PER_H;
        latemin = min % M_PER_H;
        printf("\nThen the time is %d hour %d minute.\n",hour,latemin);

    }
    printf("Thanks for using my programme:D,have a nice day.\n");

    return 0;

}