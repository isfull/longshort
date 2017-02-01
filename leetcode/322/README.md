动态规划,遍历可能性空间   
dp[i] = min(dp[i], dp[i - coins[j]] + 1);   
http://www.cnblogs.com/grandyang/p/5138186.html   
https://discuss.leetcode.com/topic/32517/c-10-lines-solution-easy-understanding   
尝试过map查表方式，不可以，因为你查不到就要去递归，最后全都递归了   
还是要预先建立好整张表