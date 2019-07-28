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
    int maxDepth(TreeNode* root) {
        if (root==NULL){
            return 0;
        }
        int left_level = maxDepth(root->left);
        int right_level = maxDepth(root->right);
        return left_level>right_level?left_level+1:right_level+1;
    }
};