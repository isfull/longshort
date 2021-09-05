/*
 * @lc app=leetcode.cn id=35 lang=cpp
 *
 * [35] 搜索插入位置
 */

// @lc code=start
class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        int size = nums.size();
        if (size == 0) {
            return 0;
        }
        int left = 0;
        int right = size - 1;
        int mid = (left + right) / 2;
        while (left <= right) {
            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
                mid = (left + right) / 2;
            } else {
                right = mid - 1;
                mid = (left + right) / 2;
            }
        }
        return left;
    }
};
// @lc code=end

