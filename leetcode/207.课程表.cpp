/*
 * @lc app=leetcode.cn id=207 lang=cpp
 *
 * [207] 课程表
 */

// @lc code=start

class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        // 1 找入度0的
        // 2 移除这类点，然后相关的入度-1
        // 3 循环1、2步，直到所有点都移除
        // 计算入度
        map<int, int> indeg;
        map<int, vector<int> > edges;

        vector<vector<int>>::iterator i_pre = prerequisites.begin();
        for (; i_pre != prerequisites.end(); i_pre++) {
            int course = (*i_pre)[0];
            int pre = (*i_pre)[1];

            // 入度+1
            map<int, int>::iterator i_indeg = indeg.find(course);
            if (i_indeg != indeg.end()){
                i_indeg->second++;
            } else {
                indeg.insert(make_pair(course, 1));
            }
            // 下游列表
            map<int, vector<int> >::iterator i_edge = edges.find(pre);
            if (i_edge != edges.end()){
                i_edge->second.push_back(course);
            } else {
                vector<int> post;
                post.push_back(course);
                edges.insert(make_pair(pre, post));
            }
        }

        // 找到入度0的
        queue<int> q;
        for (int i =0; i < numCourses; ++i){
            if (indeg.find(i) == indeg.end()) {
                q.push(i);
            }
        }
        // 开始递归删除
        while(!q.empty()) {
            int i = q.front();
            // 遍历下游，入度-1，如果为0，入队列
            map<int, vector<int> >::iterator i_edge = edges.find(i);
            if (i_edge != edges.end()){
                vector<int>::iterator i_post = i_edge->second.begin();
                for (; i_post != i_edge->second.end(); i_post++) {
                    int course = *i_post;
                    map<int, int>::iterator i_indeg = indeg.find(course);
                    if (i_indeg != indeg.end()){
                        i_indeg->second--;
                        if (i_indeg->second == 0){
                            q.push(course);
                        }
                    }
                }
            }
            indeg.erase(i);
            edges.erase(i);
            q.pop();
        }
        if (indeg.size() > 0) {
            return false;
        } else {
            return true;
        }        
    }
};
// @lc code=end

