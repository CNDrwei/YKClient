from lib import file_tool
from .client_socket import *

current_id = None

def register():
    name = input("用户名:").strip()
    pwd = input("密码:").strip()

    req = {"func": "register", "name": name, "pwd": file_tool.get_md5_password(pwd)}
    # print(file_tool.get_md5_password(1))
    if name and pwd:
        client.send_request(req)
        resp = client.recv_response()
        print(resp)
    else:
        print("用户名或密码不能为空。。。")

"""
1、登录(成功后立即展示最新的公告) 2、注册 3、查看所有视频
		4、下载视频 5、查看公告 6、查看观影记录,7开通会员,8充值
"""

def show_movies():
    req = {"func":"get_movie_list"}
    client.send_request(req)
    resp = client.recv_response()
    movies = resp["movies"]
    if not movies:
        print("还没有电影,管理员小哥哥正在加班上传...")
        return

    for i in movies:
        print("%-6s`%s`" % (i["id"], i["name"]))

    return movies

def download_movie():
    print("电影列表如下:")
    ms = show_movies()
    if not ms:
        return
    id = input("请输入电影的ID:").strip()
    if id in [str(m["id"]) for m in ms]:
        req = {"func":"download","id":id,"uid":current_id}
        client.send_request(req)
        res = client.recv_file()
        # 下载成功了! 要上传下载记录
        if res:
            req = {"func":"up_history","uid":current_id,"mid":id}
            client.send_request(req)
            client.recv_response() # 请求响应模型  一次请求必须对应一次响应 否则会粘包问题

    else:
        print("id 不存在!")

def show_notices():
    req = {"func":"get_notices"}
    client.send_request(req)
    resp = client.recv_response()# {"notices":[{time,content},{}}
    if not resp["notices"]:
        print("没有公告!")
        return
    print("========notices=========")
    for i in resp["notices"]:
        print("title:%s\ncontent:%s" % (i["title"],i["content"]))
    print("==========end===========")


def download_history():
    req = {"func":"download_history","uid":current_id}
    client.send_request(req)
    resp = client.recv_response() #{"histories":[{downtime,mname},{}]}
    if not resp["histories"]:
        print("没有记录!")
        return
    print("========下载历史=======")
    for i in resp["histories"]:
        print("%s : %s" % (i["downtime"],i["mname"]))
    print("==========end=========")


def open_vip():
    """
    假设会员费用为30,
    传递用户的id给服务器
    服务器判断这个用户当前是否已经是会员
    如果不是,则判断余额是否足够
    如果如果足够则扣钱 并将vip改为1
    如果不足则返回提示信息
    """
    req = {"func":"openvip","uid":current_id}
    client.send_request(req)
    resp = client.recv_response()
    print(resp["msg"])


def recharge():
    """
    输入充值金额
    将金额与uid传给服务器
    服务器修改用户余额字段
    并返回后充值后的余额信息
    """
    money = input("请输入充值金额:").strip()
    try:
        float(money)
        money = float(money)
    except:
        print("输入不正确,必须是数字!")
        return

    req = {"func":"recharge","money":money,"uid":current_id}
    client.send_request(req)
    resp = client.recv_response()
    print(resp["msg"])






funcs = {"1":show_movies,"2":download_movie,"3":show_notices,"4":download_history,"5":open_vip,"6":recharge}

def views(id):
    global current_id
    current_id = id
    print("欢迎进入优酷系统....")
    while True:
        res= input("请选择功能:\n1.查看视频\n2.下载视频\n3.查看公告\n4.下载历史\n5.开通会员\n6.充值\nq.返回\n").strip()
        if res == "q":
            break
        if res in funcs:
            funcs[res]()
        else:
            print("输入错误!")
    print("返回上一级...")
