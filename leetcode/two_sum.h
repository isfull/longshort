/*
 * @lc app=leetcode id=1 lang=cpp
 *
 * [1] Two Sum
 */

// @lc code=start
#include <string>
#include <vector>

using namespace std;

class Solution
{
public:
    vector<int> twoSum(vector<int> &nums, int target)
    {
        vector<int> result;
        for (int i = 0; i < nums.size() - 1; ++i)
        {
            int gap = target - nums[i];
            for (int k = i + 1; k < nums.size(); ++k)
            {
                if (nums[k] == gap)
                {
                    result.push_back(i);
                    result.push_back(k);
                    return result;
                }
            }
        }
        return result;
    }
};
// @lc code=end
