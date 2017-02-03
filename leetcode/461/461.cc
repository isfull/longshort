class Solution {
public:
    int hammingDistance(int x, int y) {
        int xy = x ^ y;
        int count = 0;
        while (xy > 0) {
            if (xy % 2 > 0) {
                ++count;
            }
            xy >> 1;
        }
        return count;
    }
};