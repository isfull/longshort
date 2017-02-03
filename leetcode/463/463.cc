class Solution {
public:
    int islandPerimeter(vector<vector<int>>& grid) {
        int i = 0;
        int j = 0;
        int count = 0; // grid num 
        int connect = 0; // grid connect count
        int hsize = grid.size();
        int vsize = grid[0].size();
        for (; i < hsize; ++i) {
            j = 0;
            for (; j < vsize; ++j) {
                if ( grid[i][j] ) {
                    ++count;
                    // right
                    if (j + 1 < vsize) {
                        if (grid[i][j + 1]) connect++;
                    }
                    //down
                    if (i + 1 < hsize) {
                        if (grid[i + 1][j]) connect++;
                    }
                }
            }
        }
        return count * 4 - connect * 2;
    }
};