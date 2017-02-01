
/**
You are given coins of different denominations and a total amount of money amount. Write a function 
to compute the fewest number of coins that you need to make up that amount. If that amount of money 
cannot be made up by any combination of the coins, return -1.

Example 1:
coins = [1, 2, 5], amount = 11
return 3 (11 = 5 + 5 + 1)

Example 2:
coins = [2], amount = 3
return -1.

Note:
You may assume that you have an infinite number of each kind of coin.
*/
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        // 初始化为amount+1更好，参见https://discuss.leetcode.com/topic/32517/c-10-lines-solution-easy-understanding
        std::vector<int> steps(amount + 1,-1);
        steps[0] = 0;
        for (int i = 0; i <= amount; ++i) {
            for (unsigned int k = 0; k < coins.size(); ++k) {
                if (coins[k] <= i) {
                    if (steps[i - coins[k]] != -1) {
                        if (steps[i] != -1) {
                            steps[i] = min(steps[i], steps[i - coins[k]] + 1);
                        } else {
                            steps[i] = steps[i - coins[k]] + 1;
                        }
                    }
                }
            }
        }
        return steps[amount];
    }
};

// 失败的map查表方法
/**
You are given coins of different denominations and a total amount of money amount. Write a function 
to compute the fewest number of coins that you need to make up that amount. If that amount of money 
cannot be made up by any combination of the coins, return -1.

Example 1:
coins = [1, 2, 5], amount = 11
return 3 (11 = 5 + 5 + 1)

Example 2:
coins = [2], amount = 3
return -1.

Note:
You may assume that you have an infinite number of each kind of coin.
*/
//class Solution {
//
//public:
//    Solution() {
//        known_amount.clear();
//    }
//    int coinChange(vector<int>& coins, int amount) {
//        if (amount == 0) {
//            return 0;
//        }
//        int result = -1;
//
//        map<int,int>::iterator i_hash = known_amount.find(amount);
//        if (i_hash != known_amount.end()) {
//            return i_hash->second;
//        }
//
//        // if amount in coins
//        std::vector<int>::iterator i = coins.begin();
//        for (; i != coins.end(); i++) {
//            if (amount == *i) {
//                known_amount.insert(make_pair(amount, 1));
//                return 1;
//            }
//        }
//        // dp search
//        i = coins.begin();
//        for (; i != coins.end(); i++) {
//            if (amount > *i) {
//                // if hash
//                int k = -1;
//                i_hash = known_amount.find(amount - *i);
//                if (i_hash != known_amount.end()) {
//                    k = i_hash->second;
//                } else {
//                    k = coinChange(coins, amount - *i);
//                }
//                // get min
//                if ( k != -1) {
//                    if (result != -1) {
//                        k = k + 1;
//                        result = k < result ? k : result;
//                    } else {
//                        result = k + 1;
//                    }
//                }
//            }
//        }
//        known_amount.insert(make_pair(amount, result));
//        return result;
//    }
//private:
//    std::map<int,int> known_amount;
//};//