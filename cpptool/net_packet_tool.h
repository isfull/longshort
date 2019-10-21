#ifndef __TEST_
#define __TEST_

#include <arpa/inet.h>
#include <vector>
#include <string>

namespace net
{

/*
协议格式如下：

BEGIN（1byte)+TOTAL_LEN(4byte)+BODY(变长)+END(1byte)

其中：
BEGIN   0x1a
TOTAL_LEN 为整包长度
BODY  业务数据内容
END   0x1b

*/
class NetPacketTool
{
private:
    NetPacketTool() {};
    ~NetPacketTool() {};
public:
    /* @brief: 解析网络包大小
     * @param：
     *    data: buf指针
     *    len: buf长度
     * @return：
     *    =0：未接收完
     *    <0: 出错
     *    >0: 包长度
     */
    static int32_t CheckPacket(const char* data, uint32_t len)
    {
        if (len < 5) return 0;

        uint32_t real_len = ntohl(*(uint32_t*)&data[1]);
        if (real_len > len) {
            return 0;
        }

        if (data[0] != 0x1a || data[real_len - 1] != 0x1b || real_len <= 5) {
            return -1;
        }

        return real_len;
    }
    /* @brief: 从packet中获取应用层数据
     * @param：
     *    packet: packet字符串应用
     * @return：
     *    应用层数据字符串
     */
    static std::string GetPacketData(const std::string& packet)
    {
        return packet.substr(5, packet.size() - 6);
    }
    /* @brief: 打包协议层packet
     * @param：
     *    data: 应用层数据字符串
     * @return：
     *    应用层数据字符串
     */
    static std::string PackPacket(const std::string& data)
    {
        static char head = 0x1a;
        static char end = 0x1b;
        uint32_t size = data.size() + 6;
        size = htonl(size);

        std::string packet = "";
        packet.reserve(size + 1);

        packet = head;
        packet.append((const char*)&size, 4);
        packet += data;
        packet.append(1, end);

        return packet;
    }
};
}

#endif