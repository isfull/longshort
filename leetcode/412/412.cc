class Solution {
public:
    vector<string> fizzBuzz(int n) {
        std::vector<string> vx;
        vx.reserve(n);
        for (int i = 1; i <= n; ++i) {
            vx[i-1] = "";
            if (i % 3 == 0) {
                vx[i-1] += "Fizz";
            }
            if (i % 5 == 0) {
                vx[i-1] += "Buzz";
            }
            if (vx[i-1] == "") {
                vx[i-1] = to_string(i);
            }
        }
        return vx;
    }
};