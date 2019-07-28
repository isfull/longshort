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
    ListNode* reverseList(ListNode* head) {
        if (head == NULL){return NULL;}
        ListNode* p = head;
        ListNode* p_next = p->next;
        p->next = NULL;
        if(p_next->next==NULL){p_next->next = p; return p_next;}
        while(p_next->next!=NULL){
            ListNode* p_next_next = p_next->next;
            p->next  = NULL;

            p_next->next = p;
            p=p_next;
            p_next = p_next_next;
            p->next = 
        }
    }
};