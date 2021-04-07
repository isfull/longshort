/*
 * @lc app=leetcode id=7 lang=cpp
 *
 * [7] Reverse Integer
 */

// @lc code=start
class Solution
{
public:
    int reverse(int x)
    {
        int max = 0x7FFFFFFF;
        int max_10 = max / 10;
        int min = 0x80000000;
        int min_10 = min / 10;

        if (x == min)
        {
            return 0;
        }

        bool sign = true;
        if (x < 0)
        {
            x = 0 - x;
            sign = false;
        }
        int result = x % 10;
        x /= 10;
        while (x != 0)
        {
            if (result > max_10)
            {
                return 0;
            }
            result *= 10;
            result += x % 10;
            x /= 10;
        }
        if (sign)
        {
            return result;
        }
        else
        {
            return 0 - result;
        }
    }
};
// @lc code=end
