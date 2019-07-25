import json
import socket
import struct
from lib import file_tool

from conf.settings import *
class Client:

    def __init__(self):
        soc = socket.socket()
        soc.connect((IP,PORT))
        self.__soc = soc
        print("连接服务器成功!")

    def recv_response(self):
        """接收响应数据"""
        len_bytes = self.__soc.recv(4)
        head_len = struct.unpack("i", len_bytes)[0]

        data_bytes = self.__soc.recv(head_len)
        json_data = json.loads(data_bytes.decode("utf-8"))

        return json_data

    def send_request(self,req):
        "发送请求"
        json_bytes = json.dumps(req).encode("utf-8")
        len_bytes = struct.pack("i", len(json_bytes))

        self.__soc.send(len_bytes)
        self.__soc.send(json_bytes)

    def send_file(self,path,info):
        self.send_request(info)
        # 发送文件数据
        f = open(path, "rb")
        while True:
            data = f.read(1024)
            if not data:
                break
            self.__soc.send(data)
        return self.recv_response()

    def recv_file(self):
        file_info = self.recv_response()
        # 两种情况 1.可以开始下载 将会收到文件信息
        #         2. 余额不足
        # 判断 是哪一种情况 如果status为False意味着余额不足  提示并结束函数
        if file_info.get("status") == False:
            print(file_info["msg"])
            return

        #如果没有结束函数 则开始接收文件
        file_size = file_info["filesize"]
        filename = file_info["filename"]
        origin_md5 = file_info["MD5"]
        path = os.path.join(DOWNLOAD_DIR,filename)

        f = open(path,"wb")
        recv_size = 0
        while recv_size < file_size:
            if file_size - recv_size > 1024:
                data = self.__soc.recv(1024)
            else:
                data = self.__soc.recv(file_size - recv_size)
            f.write(data)
            recv_size += len(data)
        f.close()
        md5 = file_tool.get_md5(path)

        if md5 == origin_md5:
            #需要在下载成功后,记录下载历史 所以返回了一个状态值
            print("下载成功!")
            return True
        else:
            print("数据校验失败!请重新下载;")





# 创建客户端连接对象
client = Client()