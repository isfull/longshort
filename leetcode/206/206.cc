/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
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