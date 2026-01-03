//还是第二章练习题:D
#include<stdio.h>
int main(void)
{
    jolly();
    deny();

    return 0;

}
void jolly(void)
{
    printf("123456789\n");
    printf("123456789\n");
    printf("123456789\n");
}
void deny(void)
{
    printf("111");

    return 0;
}
//嫌麻烦 就用数字代替了✌
void jolly(void);
void deny(void);
//实验结果为函数原型放哪都行