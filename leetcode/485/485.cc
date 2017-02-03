class Solution {
public:
    int findMaxConsecutiveOnes(vector<int>& nums) {
        vector<int>::iterator i = nums.begin();
        int count = 0;
        int max = 0;
        for (; i != nums.end(); i++) {
            if (*i) {
                count ++;
            } else {
                max = max > count ? max : count;
                count = 0;
            }
        }
        max = max > count ? max : count;
        return max;
    }
};