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

        if (root->left == NULL && root->right == NULL)
        {
            return true;
        } else if (root->left != NULL && root->right == NULL) {
            if (root->left->val < root->val)
            {
                return isValidBST(root->left);
            }
            return false;
        } else if (root->left == NULL && root->right != NULL) {
            if (root->right->val > root->val)
            {
                return isValidBST(root->right);
            }
            return false;
        } else {
            if (root->left->val < root->val && root->right->val > root->val)
            {
                return isValidBST(root->left) && isValidBST(root->right);
            }
            return false;
        }

    }
};