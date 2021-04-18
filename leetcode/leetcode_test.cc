#include <ctime>
#include <iostream>
#include <string>
#include <vector>

#include "gtest/gtest.h"

#include "two_sum.h"

TEST(TwoSum, Case0_P0)
{
    std::vector<int> nums = {3,2,4};
    Solution s;
    std::vector<int> result = s.twoSum(nums, 6);
    cout << "allen test" << result[0] << result[1] << std::endl;
    EXPECT_EQ(result[0], 1);
    EXPECT_EQ(result[1], 2);
    
}
