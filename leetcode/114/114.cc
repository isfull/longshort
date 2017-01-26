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
    void flatten(TreeNode* root) {
        if (root == NULL){
            return;
        }
        if (root->left == NULL ){
            if (root->right == NULL){
                return;
            } else {
                flatten(root->right);
                return;
            }
        } else {
            flatten(root->left);
            TreeNode* left_last_node = NULL;
            ShiftToLastNode(root->left, &left_last_node);
            if (root->right == NULL){
                root->right = root->left;
                root->left = NULL;
                return;
            } else {
                flatten(root->right);
                left_last_node->right = root->right;
                root->right = root->left;
                root->left = NULL;
                return;
            }
        }
    }

    // TODO(isfull): maybe we can remove this func
    void ShiftToLastNode(TreeNode* root, TreeNode** p) {
        if (root == NULL){
            return;
        }
        if (root->right == NULL) {
            *p = root;
        } else {
            ShiftToLastNode(root->right, p);
        }
    }

};