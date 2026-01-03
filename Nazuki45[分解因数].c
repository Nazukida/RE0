#include<stdio.h>
#include<stdbool.h>
int main(){
    unsigned long num;
    unsigned long div;
    _Bool isPrime;

    printf("Enter an integer.");
    printf("(Enter q to quit.)");
    while (scanf("%lu",&num) == 1)
    {
        for (div = 2, isPrime = true; (div * div) <= num; div++)
        {
            if (num % div == 0)
            {
                if ((div * div) != num)
                {
                    printf("%lu is divisible by %lu and %lu.\n",num,div,num/div);
                }else
                {
                    printf("%lu is divisible by %lu.\n",num,div);
                }isPrime=false;
                
                
            }
            if (isPrime)
            {
                printf("%lu is prime.\n",num);
            }
             
        }
        printf("Please enter another integer for ananysis; ");
        printf("Enter q to quit.\n");
    }
    printf("Bye.\n");
    return 0;
}