#include <stdio.h>
int main() {
    int a[5];
    int i;
    for (i = 0; i < 5; i++) {
        a[i] = i;
    }
    for (i = 0; i < 5; i++) {
        printf("%d ", a[i]);
    }
    return 0;
}