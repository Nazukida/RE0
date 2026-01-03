#include<stdio.h>
int main(void)
{
    float pt,b,zs,dts,cs;
    printf("请输入杯数______\b\b\b\b\b\b");
    scanf("%f",&b);
    pt=b/2;
    zs=b*8;
    dts=zs*2;
    cs=dts*3;
    printf("\n");
    printf("现在你拥有%f品脱,%f盅司,%f大汤勺以及%f茶勺:D\n",pt,zs,dts,cs);

    getchar();
    getchar();
    return 0;

}
//此程序可运行，但C语言本身不支持中文