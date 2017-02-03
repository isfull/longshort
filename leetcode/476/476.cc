class Solution {
public:
    int findComplement(int num) {
        int temp = num;
        int count  = 0;
        while (temp) {
            ++count;
            temp = temp >> 1;
        }
        return ((1<<count)-1) ^ num;
    }
};