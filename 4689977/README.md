###文件说明
config.ini: 程序配置文件  
config_test.ini: 测试用程序配置文件  
crawer_config.py: 解析config.ini的工具模块  
crawer_html_parser.py: HTML文本内容解析器  
crawer_log.py: 日志logging模块设置模块  
crawer_logic.py: 爬虫逻辑实现  
crawer_main.py: 程序入口，加载配置，初始化参数  
crawer_page_util.py: 工具模块，主要功能是完成web请求和数据接收  
input.txt: 种子地址列表  

###执行方式
默认参数执行: python crawer_main.py  
参看帮助: python crawer_main.py -h  