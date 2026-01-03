#include<bits/stdc++.h>
#include<stdio.h>
#include<iostream>
#include<vector>
#include<math.h>
#include<unordered_map>

using namespace std;

int main(){
    //声明一个整数
    int a = 10;
    cout << a <<endl;
    cin >> a;
    cout << a;
    int b;
    cin >> b;
    a = b;
    cout << b;
    long long c = 10000000;
    cout << a << endl;
    cout << b << endl;
    cout << c << endl;
    if (a==b) cout << "Yes" << endl;
    else cout << "No"  << endl;
    bool flag = true;//一般都这么用，命名为flag。赋值仅可赋ture 0 1
    if (flag) cout <<"This will always be printed.";
    else cout << "Damn!";
    return 0;
}