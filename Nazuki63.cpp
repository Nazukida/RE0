#include <iostream>
#include <windows.h>
#include <vector>

void SendKey(WORD keyCode) {
    INPUT input = {0};
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = keyCode;
    
    // 按下按键
    SendInput(1, &input, sizeof(INPUT));
    
    // 释放按键
    input.ki.dwFlags = KEYEVENTF_KEYUP;
    SendInput(1, &input, sizeof(INPUT));
}

int main() {
    // 等待 5 秒，给你时间将光标移到输入框
    std::cout << "脚本将在 5 秒后开始，请将光标移到输入框。" << std::endl;
    Sleep(5000); 

    std::cout << "脚本已开始运行。按 Ctrl+C 终止。" << std::endl;

    while (true) {
        // 模拟输入数字 '1'
        SendKey(0x31); // 0x31 是数字 '1' 的虚拟键码
        Sleep(100); // 短暂延迟

        // 模拟按下回车键（发送）
        SendKey(VK_RETURN);
        
        // 每输入一次，等待 100 毫秒
        Sleep(200); 

    }

    return 0;
}