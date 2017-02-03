class Solution {
public:
    string reverseString(string s) {
        unsigned int size = s.size();
        for (unsigned int i = 0; i < size/2; ++i) {
            swap(s[i], s[size - 1 -i]);
        }
        return s;
    }
};