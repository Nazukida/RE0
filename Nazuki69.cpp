#include<iostream>

using namespace std;

int a[100005];
int dp[100005];
int n;

int main(){
    cin >> n;
    for(int i = 1; i <= n; i++){
        cin >> a[i];
    }
    dp[1] = a[1];
    int ans = dp[1];
    for(int i = 2; i <= n; i++){
        dp[i] = max(a[i], dp[i-1] + a[i]);
        ans = max(ans, dp[i]);
    }
    cout << ans << endl;
    return 0;
}
// #include <iostream>
// #include <algorithm> // 1. 引入算法头文件

// using namespace std;

// int a[100005];
// long long dp[100005]; // 2. 使用 long long 防止溢出
// int n;

// int main(){
//     // 3. IO 加速
//     ios::sync_with_stdio(false);
//     cin.tie(0);

//     cin >> n;
//     for(int i = 1; i <= n; i++){
//         cin >> a[i];
//     }
    
//     dp[1] = a[1];
//     long long ans = dp[1]; // ans 也要改成 long long
    
//     for(int i = 2; i <= n; i++){
//         dp[i] = max((long long)a[i], dp[i-1] + a[i]); // 确保比较时类型一致
//         ans = max(ans, dp[i]);
//     }
    
//     cout << ans << endl;
//     return 0;
// }