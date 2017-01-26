/**
 * AAAA
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 * 
 * BBBB
 * L: distance of head -> cycle_start
 * N: distance of cycle_start -> two point meet
 * M: cycle length
 * 
 * 1. L+N = 2L+2N-xM
 * 2. xM = N + L
 * from 2 we can know: we leave cycle_start N step, after L step we will go xM step, then we at the beginning.
 *
 */
class Solution {
public:
    ListNode *detectCycle(ListNode *head) {
        ListNode* p1 = head;
        ListNode* p2 = head;
        while (p2 && p2->next){
            p1 = p1->next;
            p2 = p2->next->next;
            if (p1 == p2) {
                p2 = head;
                while (p2 != p1) {
                    p1= p1->next;
                    p2= p2->next;
                }
                return p1;
            }
        }
        return NULL;
    }
};