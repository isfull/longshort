##�ǳ��Ĵ���Ҫ���Ǻܺõģ������ϰ
##��ʹ��python����һ�����㶨��ץȡ��mini_spider.py��ʵ�ֶ��������ӵĹ������ץȡ������URL��������ض�pattern����ҳ���浽�����ϡ�
��������: 
python mini_spider.py -c spider.conf

##�����ļ�spider.conf: 
[spider] 
url_list_file: ./urls ; �����ļ�·�� 
output_directory: ./output ; ץȡ����洢Ŀ¼ 
max_depth: 1 ; ���ץȡ���(����Ϊ0��) 
crawl_interval: 1 ; ץȡ���. ��λ: ��
crawl_timeout: 1 ; ץȡ��ʱ. ��λ: ��
target_url: .*.(gif|png|jpg|bmp)$ ; ��Ҫ�洢��Ŀ����ҳURL pattern(������ʽ) 
thread_count: 8 ; ץȡ�߳��� 

�����ļ�ÿ��һ�����ӣ�����: 
http://www.baidu.com 
http://www.sina.com.cn 

##Ҫ���ע������: 
1.	��Ҫ֧�������в��������������: -h(����)��-v(�汾)��-c(�����ļ�)
2.	��Ҫ���չ�����ȵ�˳��ץȡ��ҳ��
3.	������ҳץȡ�����ʧ�ܣ����ܵ������������˳�����Ҫ����־�м�¼�´���ԭ�򲢼�����
4.	�������������ץȡ����󣬱��������˳���
5.	��HTML��ȡ����ʱ��Ҫ�������·���;���·����
6.	��Ҫ�ܹ�����ͬ�ַ��������ҳ(����utf-8��gbk)��
7.	��ҳ�洢ʱÿ����ҳ������Ϊһ���ļ�����URLΪ�ļ�����ע���URL�е������ַ�����Ҫ��ת�塣
8.	Ҫ��֧�ֶ��̲߳���ץȡ��
9.	�����ϸ�����python����淶
10.	����Ŀɶ��ԺͿ�ά���Ժá�ע��ģ�顢�ࡢ��������ƺͻ���
11.	�����Ӧ�ĵ�Ԫ���Ժ�ʹ��demo�����demo��������У���Ԫ������Ч����ͨ��
12.	ע�����ץȡ���������������Է���վ���IP��

��ʾ(�����python����ܶ�����ɲ������а���): 
##re(������ʽ)
  �ο�: http://docs.python.org/2/library/re.html
  �ο�: http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html
  �ο�: http://blog.csdn.net/jgood/article/details/4277902
##gevent/threading(���߳�)
  �ο�: http://docs.python.org/2/library/threading.html
  �ο�: http://www.cnblogs.com/huxi/archive/2010/06/26/1765808.html
##docopt/getopt/argparse(�����в�������)
  �ο�: https://github.com/docopt/docopt
  �ο�: http://docs.python.org/2/library/getopt.html
  �ο�: http://andylin02.iteye.com/blog/845355
  �ο�: http://docs.python.org/2/howto/argparse.html
  �ο�: http://www.cnblogs.com/jianboqi/archive/2013/01/10/2854726.html
##ConfigParser(�����ļ���ȡ)
  �ο�: http://docs.python.org/2/library/configparser.html
  �ο�: http://blog.chinaunix.net/uid-25890465-id-3312861.html
##urllib/urllib2/httplib(��ҳ����)
  �ο�: http://docs.python.org/2/library/urllib2.html
  �ο�: http://blog.csdn.net/wklken/article/details/7364328
  �ο�: http://www.nowamagic.net/academy/detail/1302872
##pyquery/beautifulsoup4/HTMLParser/SGMLParser(HTML����)
  �ο�: http://docs.python.org/2/library/htmlparser.html
  �ο�: http://cloudaice.com/yong-pythonde-htmlparserfen-xi-htmlye-mian/
  �ο�: http://docs.python.org/2/library/sgmllib.html
  �ο�: http://pako.iteye.com/blog/592009
##urlparse(URL��������)
  �ο�: http://docs.python.org/2/library/urlparse.html
  �ο�: http://blog.sina.com.cn/s/blog_5ff7f94f0100qr3c.html
##logging(��־����)
  �ο�: http://docs.python.org/2/library/logging.html
  �ο�: http://kenby.iteye.com/blog/1162698
  �ο�: http://my.oschina.net/leejun2005/blog/126713