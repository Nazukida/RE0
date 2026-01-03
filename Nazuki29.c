#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    scanf("%d", &n);
     int* data = (int*)malloc(n * sizeof(int));
    if (data == NULL) {
        return 1;
}
    printf("\n");
    for (int i = 0; i < n; i++) {
        scanf("%d", &data[i]);
    }
    
    int* jiaodu = (int*)malloc((n + 1) * sizeof(int));
    if (jiaodu == NULL) {
        free(data);
        return 1; 
    }

    int qiege = 0;
    jiaodu[0] = 0;

    for (int i = 0; i < n; i++) {
        qiege = (qiege + data[i]) % 360;
        jiaodu[i + 1] = qiege;
    }

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n + 1; j++) {
            if (jiaodu[i] > jiaodu[j]) {
                int temp = jiaodu[i];
                jiaodu[i] = jiaodu[j];
                jiaodu[j] = temp;
            }
        }
    }

    int da = 0;
    for (int i = 0; i < n; i++) {
        int shengyujiaodu = jiaodu[i + 1] - jiaodu[i];
        if (shengyujiaodu > da) {
            da = shengyujiaodu;
        }
    }

    int zuihou = 360 - jiaodu[n];
    if (zuihou > da) {
        da = zuihou;
    }

    printf(" %d \n", da);

    free(data);
    free(jiaodu);

    return 0;
}
