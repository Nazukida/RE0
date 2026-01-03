#include<bits/stdc++.h>

using namespace std;

int a,b,c[2010],cnt=0;

bool pd(int n){
    if(n % 400==0){
        return true;
    }
    if (n % 4==0 && n % 100 != 0)
    {
        return true;
    }
    return false;
}

int main(){
    int a,b;
    cin >> a >> b;
    for (int i = a; i <= b; i++)
    {
        if(pd(i)){
            c[cnt++] = i;
        }
    }
    cout << cnt << endl;
    for (int i = 0; i < cnt; i++)
    {
        cout << c[i] << "";

    }
    return 0;
    
}



/*
int fib(int n){
    if(n==1 || n==2){
    return 1;
    }
    return fib(n-1) + fib(n-2)
}

int f(int n){
    if(n=1)
    cout
}

*/