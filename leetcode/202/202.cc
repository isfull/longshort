class Solution {
public:
    bool isHappy(int n) {
        if (happy_set_.find(n) != happy_set_.end()) {
            return true;
        }
        if (unhappy_set_.find(n) != unhappy_set_.end()) {
            return false;
        }
        int temp = 0;
        while (n != 1 && n != 4) {
            int t = 0;
            while (n) {
                temp = n % 10;
                t += temp * temp;
                n /= 10;
            }
            n = t;
        }
        bool rt = (n == 1);
        if (rt)
        {
            happy_set_.insert(n);
        }
        else
        {
            unhappy_set_.insert(n);
        }
        return rt;
    }
private:
    unordered_set<int> happy_set_;
    unordered_set<int> unhappy_set_;
};
