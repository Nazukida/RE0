//zwqsb, zhe dou bu hui xie, lan de pen
#include <stdio.h>
int main() {
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);
    int max = ((a > b) ? a : b) > c ? ((a > b) ? a : b) : c;
    printf("%d\n", max);

    return 0;
}