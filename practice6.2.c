#include<stdio.h>
int main(){
    int count,count1,j;
    count1 = 1;
    char ch,ch1;
    scanf("%c",&ch);
    ch1 = ch;
    count = (int)ch - 65;
    for (int i = 0; i <= count; i++)
    {
        ch = ch1;
        for (  j = 1 ; j <= count1; j++)
        {
            printf("%c",ch);
            ch--;
        }
        printf("\n");
        count1++;
        
    }
    
    return 0;
    
}

/*简化版本
#include<stdio.h>
int main() {
    char ch;
    scanf("%c", &ch);
    int count = ch - 'A';  // 计算循环次数
    
    for (int i = 0; i <= count; i++) {
        for (char c = ch; c >= ch - i; c--) {
            printf("%c", c);  // 直接打印字符
        }
        printf("\n");  // 换行
    }
    
    return 0;
}



*/