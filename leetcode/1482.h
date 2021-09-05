/*
 * @lc app=leetcode.cn id=1482 lang=cpp
 *
 * [1482] 制作 m 束花所需的最少天数
 */
#include <string>
#include <vector>
using namespace std;

// @lc code=start
class Solution
{
public:
    bool CanMake(const vector<int> &bloomDay, int day, int m, int k)
    {
        // 遍历数据，找到连续的比d小的数量
        int need_m = m;
        int count = 0;
        for (auto &f : bloomDay)
        {
            if (f <= day)
            {
                count++;
            }
            else
            {
                need_m -= count / k;
                count = 0;
            }
        }
        // 循环边界处理
        need_m -= count / k;
        return (need_m < 1);
    }

    int minDays(vector<int> &bloomDay, int m, int k)
    {
        int size = bloomDay.size();
        // m*k > size
        if (m * k > size)
        {
            return -1;
        }
        // 花期排序 set是红黑树，自带排序
        set<int> datex;
        for (auto &b : bloomDay)
        {
            datex.insert(b);
        }
        vector<int> date;
        date.reserve(size);
        for (auto &d : datex)
        {
            date.push_back(d);
        }
        // 按花期数组二分判断
        int low = 0;
        int high = date.size() - 1;
        while (low < high)
        {
            int mid = (low + high) / 2;
            if (CanMake(bloomDay, date[mid], m, k))
            {
                high = mid;
            }
            else
            {
                low = mid + 1;
            }
            cout << low << " " << high << endl;
        }
        return date[low];
    }
};
// @lc code=end
