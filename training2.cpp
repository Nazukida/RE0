#include<bits/stdc++.h>
#include<stdio.h>
#include<iostream>
#include<vector>
#include<math.h>
#include<unordered_map>

using namespace std;

struct stu//自定义函数//两个属性
{
    string name;//字符串类型
    int id;
};

int main(){
    //int ,double ,char,long long
    int a;
    stu s1;
    a = 100;
    //s1 = {"Nazuki",1};
    //cout << s1.name << endl;//s1后面的点用来表明属性
    //cout << s1.id << endl;
    cin >> s1.name >>s1.id;
    cout << s1.name << " " << s1.id;
    
}
