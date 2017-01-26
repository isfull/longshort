//["XXXOXO","OXOXOX","XOXOXO","OXOXOX"]
class Solution {
public:
    void solve(vector<vector<char>>& board) {
        if (board.size() < 1)
        {
            return;
        }
        length_ = board[0].size();
        height_ = board.size();
        // 初始化四周的种子点
        InitSet(board);
        set<pair<int, int> >::const_iterator i_set = init_set_.begin();
        int x = 0;
        int y = 0;
        // BFS增加点
        while (init_set_.size() > 0)
        {
            i_set = init_set_.begin();
            x = i_set->first;
            y = i_set->second;
            init_set_.erase(i_set);
            Check4(x, y, board);
        }
        // 不在集合内的O都改成X
        for (int i = 0; i < height_; ++i)
        {
            for (int j = 0; j < length_; ++j)
            {
                if (board[i][j] = 'O') {
                    if(o_set_.find(CalcKey(i, j)) == o_set_.end()) {
                        board[i][j] = 'X';
                    }
                }
            }
        }
    }
    void Check4(int x, int y, vector<vector<char>>& board) {
        Check1(x - 1, y, board);
        Check1(x, y + 1, board);
        Check1(x + 1, y, board);
        Check1(x, y - 1, board);
    }
    void Check1(int x, int y, vector<vector<char>>& board) {
        if (x >= 0 && y >= 0 && x < height_ && y < length_)
        {
            if (board[x][y] == 'O')
            {
                if(o_set_.find(CalcKey(x, y)) == o_set_.end()) {
                    init_set_.insert(make_pair(x, y));
                    o_set_.insert(CalcKey(x, y));
                }
                
            }
        }
    }
    int CalcKey(int x, int y) {
        return x * length_ + y;
    }
    void InitSet(vector<vector<char>>& board) {
        // top
        for (int i = 0; i < length_; ++i)
        {
            if (board[0][i] == 'O')
            {
                init_set_.insert(make_pair(0, i));
                o_set_.insert(CalcKey(0, i));
            }
        }
        // bottom
        int endx = height_ - 1;
        for (int i = 1; i < length_; ++i)
        {
            if (board[endx][i] == 'O')
            {
                init_set_.insert(make_pair(endx, i));
                o_set_.insert(CalcKey(endx, i));
            }
        }
        // left
        for (int i = 1; i < height_; ++i)
        {
            if (board[i][0] == 'O')
            {
                init_set_.insert(make_pair(i, 0));
                o_set_.insert(CalcKey(i, 0));
            }
        }
        // right
        int end = length_ - 1;
        for (int i = 1; i < height_; ++i)
        {
            if (board[i][end] == 'O')
            {
                init_set_.insert(make_pair(i, end));
                o_set_.insert(CalcKey(i, end));
            }
        }
    }

private:
    int length_;
    int height_;
    set<pair<int, int> > init_set_;
    unordered_set<int> o_set_;
};

