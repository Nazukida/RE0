// #include <bits/stdc++.h>

// using namespace std;
// // 计算数组中相邻元素差值绝对值之和
// int valueDefine(vector<int> &nums)
// {
//     int count = 0;
//     for (int i = 0; i < nums.size() - 1; i++)
//     {
//         count += abs(nums[i + 1] - nums[i]);
//     }
//     return count; // 新增返回语句
// }

// // 反转数组中 [l, r] 区间的元素，并打印该区间元素
// void re(vector<int> &nums, int l, int r)
// {
//     reverse(nums.begin() + l, nums.begin() + r + 1); // 修正反转范围
//     // for (int i = l; i <= r ; i++) // 修正遍历范围
//     // {
//     //     cout<< nums[i] << endl;
//     // }
// }

// int main()
// {
//     int t;
//     cin >> t;
//     vector<int> ans(t);
//     int index = 0; // 新增索引变量
//     while (t--)
//     {
//         // cout <<1;
//         int n;
//         cin >> n;
//         vector<int> nums(n);
//         for (int i = 0; i < n; i++)
//         {
//             cin >> nums[i];
//         }
//         vector<int>minusXL(n, 0);
//         vector<int>minusCurT(n, 0);
//         int minusminus = INT_MIN;
//         int flag;
//         for(int j = 0; j < nums.size() - 1; j++)
//         {
//             minusXL[j + 1] = abs(nums[j] - nums[j + 1]);
//             minusCurT[j +1] = abs(nums[j + 1] - nums[0]);
//             int temp = max(abs(minusXL[j + 1] - minusCurT[j + 1]), minusminus);
//             if (temp > minusminus)
//             {
//                 flag = j;
//                 minusminus = temp;
//             }
            
//         }
//         re(nums, 0, flag);
//         for(int j = nums.size() - 1; j >= 0; j--)
//         {
//             minusXL[j + 1] = abs(nums[j] - nums[j + 1]);
//             minusCurT[j +1] = abs(nums[j + 1] - nums[nums.size() - 1]);
//             int temp = max(abs(minusXL[j + 1] - minusCurT[j + 1]), minusminus);
//             if (temp > minusminus)
//             {
//                 flag = j;
//                 minusminus = temp;
//             }
//         }
//         re(nums, flag, nums.size() - 1);
//         ans[index++] = valueDefine(nums); // 使用新索引存储结果
//     }
//     for (int i = 0; i < ans.size(); i++)
//     {
//         cout<< ans[i] << endl;
//     }
//     return 0;
// }

#include <bits/stdc++.h>

using namespace std;
long long valueDefine(const vector<int> &nums)
{
    long long count = 0;
    for (int i = 0; i < nums.size() - 1; i++)
    {
        count += abs(static_cast<long long>(nums[i + 1]) - nums[i]);
    }
    return count;
}

void re(vector<int> &nums, int l, int r)
{
    if (l < 0 || r >= nums.size() || l > r) {
        return;
    }
    reverse(nums.begin() + l, nums.begin() + r + 1);
}

int main()
{
    int t;
    cin >> t;
    vector<long long> ans(t);
    for (int test_case_idx = 0; test_case_idx < t; ++test_case_idx)
    {
        int n;
        cin >> n;
        vector<int> nums(n);
        for (int i = 0; i < n; i++)
        {
            cin >> nums[i];
        }
        if (n == 1)
        {
            ans[test_case_idx] = 0;
            continue;
        }
        long long max_total_value = valueDefine(nums);

        // 遍历所有可能的非空前缀翻转的结束位置 r1 (0 到 n-1)
        for (int r1 = 0; r1 < n; ++r1)
        {
            // 复制原始数组进行第一次翻转
            vector<int> nums_after_prefix_reversal = nums;
            re(nums_after_prefix_reversal, 0, r1);

            // 遍历所有可能的非空后缀翻转的起始位置 l2 (0 到 n-1)
            for (int l2 = 0; l2 < n; ++l2)
            {
                // 在第一次翻转后的数组基础上进行第二次翻转
                vector<int> final_nums = nums_after_prefix_reversal;
                re(final_nums, l2, n - 1);

                // 计算当前排列的价值并更新最大值
                max_total_value = max(max_total_value, valueDefine(final_nums));
            }
        }
        ans[test_case_idx] = max_total_value;
    }

    for (long long res : ans)
    {
        cout << res << endl;
    }

    return 0;
}