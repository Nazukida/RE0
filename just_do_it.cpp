#include <iostream>
#include <ctime>
#include <windows.h>
#include<math.h>

// 执行大量的数学运算来测试性能
void testPerformance() {
    int iterationCount = 0;
    double result = 0.0;
    std::clock_t start_time = std::clock();
    std::cout << "程序开始运行，按 ENTER 键停止..." << std::endl;

    INPUT_RECORD inputRecord;
    DWORD events;
    HANDLE consoleInput = GetStdHandle(STD_INPUT_HANDLE);

    while (true) {
        // 这里进行一些简单的数学运算，你可以根据需要修改运算类型
        result += std::sqrt(iterationCount) * std::sin(iterationCount) * std::cos(iterationCount);
        iterationCount++;

        // 检查是否有键盘输入事件
        if (PeekConsoleInput(consoleInput, &inputRecord, 1, &events) && events > 0) {
            // 读取输入事件
            ReadConsoleInput(consoleInput, &inputRecord, 1, &events);

            // 如果是键盘输入且按下的是回车键
            if (inputRecord.EventType == KEY_EVENT &&
                inputRecord.Event.KeyEvent.bKeyDown &&
                inputRecord.Event.KeyEvent.wVirtualKeyCode == VK_RETURN) {
                break;
            }
        }
    }

    std::clock_t end_time = std::clock();
    double elapsed_time = static_cast<double>(end_time - start_time) / CLOCKS_PER_SEC;
    std::cout << "执行 " << iterationCount << " 次运算耗时: " << elapsed_time << " 秒" << std::endl;
    std::cout << "最终结果: " << result << std::endl;
}

int main() {
    testPerformance();
    return 0;
}