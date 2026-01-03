#include<stdio.h>
int main(){
    char ch='C';
    char *pch=&ch;
    printf("%d\n",pch);
    printf("%c",*pch);

    return 0;
}