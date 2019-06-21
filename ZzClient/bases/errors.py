
# 自定义异常

class SigninError(Exception):
    def __init__(self,err='用户或密码错误'):
        Exception.__init__(self,err)

class NoDataError(Exception):
    def __init__(self,err='没有发现数据'):
        Exception.__init__(self,err)