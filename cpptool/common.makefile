# 打开一些宏
XXX_VER = true

LFLAGS += -ldl -lz -pthread

# 测试文件目录
TEST_DIR = ./test

CPPFLAGS += -isystem

CXXFLAGS += -g -Wall -Wextra -Wno-unused-parameter -pthread -std=c++11 -fPIC

# 工程目录下的所有文件
ALL_FILE = $(wildcard $(TEST_DIR)/*)     \

# 测试目录下的所有文件
CCTEST_FILE = $(wildcard $(TEST_DIR)/*)    \

# 工程代码（cpp文件）
c_file = $(filter %.c , $(ALL_FILE))
cpp_file = $(filter %.cpp , $(ALL_FILE))
h_file = $(filter %.h , $(ALL_FILE))

# 测试代码（cc文件）
cctest_file = $(filter %.cc , $(CCTEST_FILE))
            
c_o_file = $(patsubst %.c, %.o, $(c_file))    
cpp_o_file = $(patsubst %.cpp, %.o, $(cpp_file))
cc_o_file =  $(patsubst %.cc, %.o, $(cctest_file))

$(warning $(cc_o_file))

########## @TODO 增加库依赖

INC += \
    
LIB += \
    
###########


# 增加你的test执行程序名
TESTS = xxx_test

# 目标文件
TARGET_FILE = $(TEST_DIR)/$(TESTS)

.PHONY: all clean test init

all : $(TARGET_FILE)
    $(warning "target file:"$(TARGET_FILE))

clean :
    rm -f $(TEST_DIR)/$(TESTS) $(TEST_DIR)/*.o *.o


$(c_o_file) : $(c_file) $(h_file)
    $(CXX) $(CPPFLAGS) $(CXXFLAGS) $(INC) -c $(c_file)

$(cpp_o_file) : $(cpp_file) $(h_file)
    $(CXX) $(CPPFLAGS) $(CXXFLAGS) $(INC) -c $(cpp_file)

$(cc_o_file) : $(cctest_file) $(h_file)
    $(CXX) $(CPPFLAGS) $(CXXFLAGS) $(INC) -c -o $@  $<

$(TARGET_FILE) : $(cpp_o_file) $(c_o_file) $(cc_o_file)
    ./compile.sh
    $(CXX) $(CPPFLAGS) $(CXXFLAGS)  -o $@  $^  $(LIB) $(LFLAGS)

# 执行一些前置操作
init:
    ./xxx.sh

all: init $(TARGET_FILE)
    @echo -e "\033[1;32m\nSuccess!\033[0m"
    ldd -r $(TARGET_FILE)

# 执行你的unittest程序执行
test :
    $(TEST_DIR)/$(TESTS)
