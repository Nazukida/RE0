#include<iostream>
#include<vector>
#include<numeric>

using namespace std;

int main(){
    vector<int> test = {1, 2, 3, 4, 5};
    auto sum = accumulate(test.begin(), test.end(), 0);
    cout << sum << endl;
    auto sum1 = accumulate(test.begin(), test.end(), 1);
    cout << sum1 << endl;
    return 0;
}