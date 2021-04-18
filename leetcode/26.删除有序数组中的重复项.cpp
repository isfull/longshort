/*
 * @lc app=leetcode.cn id=26 lang=cpp
 *
 * [26] 删除有序数组中的重复项
 */

// @lc code=start
class Solution
{
public:
    int removeDuplicates(vector<int> &nums)
    {
        int size = nums.size();
        if (size < 2)
        {
            return size;
        }
        // 双指针，重复指针，不重复指针
        int single = 0;
        int duplicate = 1;
        while (duplicate < size)
        {
            // 找到不一样的位置
            if (nums[single] == nums[duplicate])
            {
                duplicate++;
                continue;
            }
            single++;
            nums[single] = nums[duplicate];
            duplicate++;
        } 
        return single + 1;
    }
};
// @lc code=end