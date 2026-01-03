#include<bits/stdc++.h>

using namespace std;

void print_subset(int n){
    for (int i = 0; i < (1 << n); i++)
    {
        for(int j = 0; j < n; j++){
            if(i & (1 << j)){ // 检查第j位是否为1
                cout << j << " "; // 输出子集元素
            }
            cout << endl; // 换行
        }
    }
}

int main(){
    int n;
    cin >> n; // 输入集合元素个数
    print_subset(n); // 输出所有子集
    return 0;
}