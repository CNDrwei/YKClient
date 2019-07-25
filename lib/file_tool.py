import hashlib

salt = "com.oldboy.www"


def get_md5(path):
    md5 = hashlib.md5()
    f = open(path, "rb")
    while True:
        data = f.read(1024)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()


def get_md5_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode("UTF-8"))
    md5.update(salt.encode("GBK"))
    pwd = md5.hexdigest()
    return pwd
