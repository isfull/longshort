class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int rs = 0;
        vector<int>::const_iterator i = nums.begin();
        for (;i!=nums.end();i++){
            rs ^= *i;
        }
        return rs;
    }
};

class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int rs = 0;
        int* p = nums.data();
        int i = 0;
        int size = nums.size();
        for (;i<size;p++,i++){
            rs ^= *p;
        }
        return rs;
    }
};