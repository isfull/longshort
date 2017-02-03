Given an array of integers where 1 ≤ a[i] ≤ n (n = size of array), some elements appear twice and others appear once.

Find all the elements of [1, n] inclusive that do not appear in this array.

Could you do it without extra space and in O(n) runtime? You may assume the returned list does not count as extra space.

Example:

Input:
[4,3,2,7,8,2,3,1]

Output:
[5,6]  


关键是标记谁出现了，谁没有，所以得2N   
不使用额外空间？ 除了另开数组，还有就是对num[num[i]]取负就能保存这个信息