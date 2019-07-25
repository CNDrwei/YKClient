"""
3、上传视频 4、删除视频 5、发布公告, 6.用户管理
"""
import os
from lib.file_tool import get_md5
from core.client_socket import client

current_id = None


def upload_movie():

    path = input("请输入文件路径:\n").strip()
    if os.path.exists(path) and os.path.isfile(path):
        file_info = {"func": "upload",
                     "filename": os.path.basename(path),
                     "filesize": os.path.getsize(path),
                     "md5": get_md5(path),
                     "uid":current_id}


        free = input("是否收费(y:收费)").strip()
        if free == "y":
            file_info["is_free"] = "1"
        else:
            file_info["is_free"] = "0"


        resp = client.send_file(path,file_info)
        print(resp)
    else:
        print("路径错误,必须存在的文件!")


def delete_movie():
    """
    1.获取电影的id和名字列表
    2.选择一个要删除的
    3.将id传给服务器
    4.接收响应结果
    """
    req = {"func":"get_movie_list"}
    client.send_request(req)
    resp = client.recv_response()#  {"code":200,"movies":[{"id":"123","name":"十面埋伏"}]}
    if not resp["movies"]:
        print("没有电影....")
        return

    for m_dic in resp["movies"]:
        print(m_dic)

    res = input("请输入要删除电影id:\n").strip()
    if res.isdigit():
        res = int(res)

    if res in [d["id"] for d in resp["movies"]]:
        req2 = {"func":"delete","id":res}
        print(req2)
        client.send_request(req2)
        resp2 = client.recv_response()
        print(resp2)
    else:
        print("id错误!")


def publish_notice():
    """
    1.输入标题
    2.输入内容
    3.发送给服务器 必须包含func uid
    4.接收响应
    """
    title = input("请输入标题:").strip()
    content = input("请输入内容:").strip()
    if title and content:
        req = {"func":"publish_notice","title":title,"content":content,"uid":current_id}
        client.send_request(req)
        response = client.recv_response()
        print(response)
    else:
        print("标题或内容不能为空!")


def user_manage():
    """
    1.获取所有的用户信息 展示
    2.选择需要处理的用户id
    3.询问解锁还是锁定
    4.发送请求 包含 func 用户id  锁定状态
    5.接收响应
    """
    req = {"func":"get_users"}
    client.send_request(req)
    resp = client.recv_response() #{"users":[{"id":"123","name":"张三","is_lock":0}]}
    print("当前用户数量%s" % len(resp["users"]))
    for u in resp["users"]:
        print(u)

    id = input("请输入要操作的id:\n").strip()
    if id.isdigit():
        id = int(id)

    if id in [u["id"] for u in resp["users"]]:
        lock = input("解锁输入:0 锁定输入:1").strip()
        if lock == "0" or lock == "1":
            req2 = {"func":"lock","id":id,"is_lock":int(lock)}
            client.send_request(req2)
            resp2 = client.recv_response()
            print(resp2)
        else:
            print("输入错误")







funcs = {"1":upload_movie,"2":delete_movie,"3":publish_notice,"4":user_manage}

def views(id):
    global current_id
    current_id = id
    print("尊敬的管理员,欢迎登陆...")
    while True:
        res = input("请选择功能:\n1.上传视频\n2.删除视频\n3.发布公告\n4.用户管理\nq.返回\n").strip()
        if res == "q":
            break
        if res in funcs:
            funcs[res]()
        else:
            print("输入错误!")
    print("返回上一级.....")