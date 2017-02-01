/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    bool isValidBST(TreeNode* root) {
        if (root == NULL) {
            return true;
        }
        return isValidBST(root->left) && CheckPrev(root) && isValidBST(root->right);
    }

    bool CheckPrev(TreeNode* root) {
        if (prev == NULL) {
            prev = root;
            return true;
        }
        if (prev->val >= root->val) {
            return false;
        } else {
            prev = root;
            return true;
        }
    }

private:
    static TreeNode* prev = NULL;

};