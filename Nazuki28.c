#include <stdio.h>
#include <unistd.h>

int main() {
    printf("\x1b[2J"); // 清屏
    printf("\x1b[H");  // 将光标移至左上角
    printf("\x1b[12;40H"); // 将光标移至行 12，列 40（大致屏幕中心）
    printf("Hello, World!\n"); // 打印在中心位置
    sleep(3); // 保持 3 秒钟以查看效果
    return 0;
}
