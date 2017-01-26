class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        unsigned int size = nums.size();
        if (size < 1) {
            return -1;
        }
        if (size == 1) {
            return nums[0];
        }

        int k1 = 0;
        int k2 = 0;
        while ( k2 < size && nums[k2] < size )
        {
            k1 = nums[k1];
            k2 = nums[nums[k2]];
            if (k1 == k2) {
                k2 = 0;
                while (k1 != k2) {
                    k1 = nums[k1];
                    k2 = nums[k2];
                }
                return k1;
            }
        }
        return -1;
    }
};