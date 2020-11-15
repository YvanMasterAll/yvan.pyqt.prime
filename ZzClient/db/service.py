from .model import User
from common.util.http import *
import traceback
from config.error import *
from common.util.logger import logger_err

'''
服务类
'''

class Service:
    @staticmethod
    def signin(self, name, pwd):
        '''
        用户登录
        '''
        def _signin():
            try:
                user = User.get(User.name == name, User.pwd == pwd)
                return (ResultSet.success, user)
            except:
                raise SigninError()

        return handle_execute(_signin)

    @staticmethod
    def user_list(self, user):
        '''
        用户列表
        '''
        def _list():
            follow_ids = user.follow_ids()
            users = list(User.select())
            for _user in users:
                if _user.id in follow_ids:
                    _user.followed = True
            if len(users) == 0:
                raise NoDataError()
            return (ResultSet.success, users)

        return handle_execute(_list)

'''
统一异常处理
'''

def handle_execute(sql):
    try:
        return sql()
    except Exception as e:
        logger_err.error(traceback.format_exc())
        return (ResultCode(ResultCode.sqlException, msg=e), None)