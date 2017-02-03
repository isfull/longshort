/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
        if (head == NULL) return NULL;
        int now_val = head->val;
        ListNode* pfront = head->next;
        ListNode* pback = head;
        while (pfront != NULL) {
            if (pfront->val != pback->val) {
                pback->next = pfront;
                pback = pfront;
                pfront = pback->next;
            } else {
                pfront = pfront->next;
            }
        }
        pback->next = NULL;
        return head;
    }
};