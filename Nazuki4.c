//尝试进行一个注释，并进行多个函数的学习
/*换个格式的注释玩一玩*/
#include<stdio.h>
void butler(void);
int main(void)
{
    printf("I will summon the butler function.\n");
    butler();
    printf("Yes.Bring me some tea.\n");

    return 0;
}
void butler(void)
{
    printf("You rang,sir?\n");
}