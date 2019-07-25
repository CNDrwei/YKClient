from core.user import register
from .client_socket import *
from lib import file_tool
from core import admin,user


def login():
    name = input("用户名:").strip()
    pwd = input("密码:").strip()
    req = {"func":"login","name":name,"pwd":file_tool.get_md5_password(pwd)}

    if name and pwd:
        client.send_request(req)
        resp = client.recv_response()
        print(resp)
        if resp["status"]:
            print("登录成功!")
            if resp["usertype"] == 0:
                # get_first_notice()
                user.views(resp["id"])
            else:
                admin.views(resp["id"])
        else:
            print(resp["msg"])
    else:
        print("用户名或密码不能为空。。。")


def get_first_notice():
    req = {"func":"get_first_notice"}
    client.send_request(req)
    resp = client.recv_response() #{"code":200,"notice":{"title":"aa","content:"xxx"}}
    if resp["notice"]:
        print("国际最新消息:[%s:%s]" % (resp["notice"]["title"],resp["notice"]["content"]))
    else:
        print("世界和平,没有消息...")


funcs = {"1":login,"2":register}
def run():
    while True:
        res= input("请选择功能:\n1.统一登录\n2.用户注册\nq.退出\n").strip()
        if res == "q":
            break
        if res in funcs:
            funcs[res]()
        else:
            print("输入错误!")
    print("see you la la...")


