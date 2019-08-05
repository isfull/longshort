/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 * 重点是划分好 左右，就能理清楚循环变量是哪个
 */
class Solution
{
public:
    ListNode *reverseList(ListNode *head)
    {
        if (head == NULL)
        {
            return NULL;
        }
        ListNode *left = NULL;

        ListNode *right = head;
        

        while (right != NULL)
        {
            ListNode *right_next = right->next;
            right->next = left;
            left = right;

            right = right_next;
        }
        return left;
    }
};