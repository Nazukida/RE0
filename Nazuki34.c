//仍然是4.8的练习题
//我需要让名字打印字段比姓名总量宽3
#include<stdio.h>
#include<string.h>
int main()
{
    char name[40];
    int width;

    printf("输入你的名字叭：");
    scanf("%s",name);
    width=strlen(name);
    printf("好的你的名字多三个宽度长成这样：%*s",(width+3),name);

    return 0;

}
