class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        int size = nums.size();
        for (int i=0; i<size;){
            int k = i;
            int last0 = -1; // 0和0相遇，记住第一个相遇的位置
            int swap = 0; // 避免尾部全是0的时候，死循环
            int j = k+1;
            for (;j<size;++j,++k){
                if (nums[k]==0){
                    if(nums[j]==0){
                        last0=last0==-1?k:last0;
                    }else{
                        nums[k]=nums[j];
                        nums[j]=0;
                        swap=1;
                    }
                } else {
                    continue;
                }
            }
            if (last0==-1){
                i = i+1;
            } else{
                if (swap ==1){
                    i = last0;
                }else{
                    i = j;
                }
            }
            
        }
    }
};