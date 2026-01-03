#include <stdio.h>

int main() {
    double u, a, t, v, s;
    
    printf("=== 物理运动计算 ===\n");
    printf("请输入物体的初始速度 (m/s): ");
    scanf("%lf", &u);
    printf("请输入物体的加速度 (m/s²): ");
    scanf("%lf", &a);
    printf("请输入经过的时间 (s): ");
    scanf("%lf", &t);
    
    v = u + a * t;
    
    s = u * t + 0.5 * a * t * t;
    
    printf("\n计算结果:\n");
    printf("最终速度 v = %.2f m/s\n", v);
    printf("移动距离 s = %.2f m\n", s);
    
    return 0;
}