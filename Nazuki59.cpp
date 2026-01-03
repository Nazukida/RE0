#include <vector>  // 包含 vector 头文件
#include <string>  // 包含 string 头文件
#include <set>     // 包含 multiset 头文件

class Solution {
    int getLongest(const string& str1, const string& str2){
        int maxlen = 0;
        while(maxlen < str1.size() && maxlen < str2.size() && str1[maxlen] == str2[maxlen]){
            maxlen++;
        }
        return maxlen;
    }
public:
    vector<int> longestCommonPrefix(const vector<string>& words) {
        int n = words.size();
        vector<int> ans(n);

        if (n <= 1) {
            return ans;
        }

        multiset<int> lens;

        for (int i = 0; i < n - 1; ++i) {
            int len = getLongest(words[i], words[i + 1]);
            lens.insert(len);
        }

        for (int i = 0; i < n; ++i) {
            int old1 = -1;
            int old2 = -1;

            if (i > 0) {
                old1 = getLongest(words[i - 1], words[i]);
                auto it = lens.find(old1);
                if (it != lens.end()) {
                    lens.erase(it);
                }
            }
            if (i < n - 1) {
                old2 = getLongest(words[i], words[i + 1]);
                auto it = lens.find(old2);
                if (it != lens.end()) {
                    lens.erase(it);
                }
            }

            int new_len = 0;
            if (i > 0 && i < n - 1) {
                new_len = getLongest(words[i - 1], words[i + 1]);
                lens.insert(new_len);
            }

            if (lens.empty()) {
                ans[i] = 0;
            } else {
                ans[i] = *lens.rbegin();
            }

            if (i > 0) {
                lens.insert(old1);
            }
            if (i < n - 1) {
                lens.insert(old2);
            }
            if (i > 0 && i < n - 1) {
                auto it = lens.find(new_len);
                if (it != lens.end()) {
                    lens.erase(it);
                }
            }
        }
        return ans;
    }
};