/*
 * @lc app=leetcode.cn id=278 lang=cpp
 *
 * [278] 第一个错误的版本
 */

// @lc code=start
// The API isBadVersion is defined for you.
// bool isBadVersion(int version);

class Solution {
public:
    int Mid(int left, int right){
        return (right - left) /2 + left;
    }
    int firstBadVersion(int n) {
        if (n == 0) {
            return -1;
        }
        int left = 1;
        int right = n;
        int mid = Mid(left, right);
        while (left < right) {
            if (isBadVersion(mid)) {
                right = mid;
                mid = Mid(left, right);
            } else {
                left = mid + 1;
                mid = Mid(left, right); 
            }
        }
        return right;
    }
};
// @lc code=end

