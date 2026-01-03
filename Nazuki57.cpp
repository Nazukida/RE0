#include <bits/stdc++.h>
#include <ctime>

using namespace std;

#define Swap(a, b) (a ^= b, b ^= a, a ^= b)

int data[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20};
int num = 0;
int Perm(int begin, int end)
{
    int i;
    if (begin == end)
    {
        num++;
    }
    else
    {
        for (i = begin; i <= end; i++)
        {
            Swap(data[i], data[begin]);
            Perm(begin + 1, end);
            Swap(data[i], data[begin]);
        }
    }
    return num;
}

int main()
{
    char ch = getchar();
    while (ch != 'q')
    {
        clock_t start, end;
        start = clock();
        int a;
        cin >> a;
        // 输入验证
        cout << Perm(0, a - 1) << endl;
        end = clock();
        cout << (double)(end - start) / CLOCKS_PER_SEC << "s" << endl;
        ch = getchar(); // 读取下一个字符
    }
    return 0;
}