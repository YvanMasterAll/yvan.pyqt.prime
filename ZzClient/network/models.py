from peewee import *
import datetime
import uuid
import logging
from request import *
from base import logger_err
import traceback
from errors import *

# 数据库

_database = "zzclient.db"
database = SqliteDatabase(_database)

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# Models

class _Model(Model):
    class Meta:
        database = database

def _uuid():
    return uuid.uuid1()

# 用户表
class User(_Model):
    id              = UUIDField(primary_key=True, default=_uuid)
    name            = CharField(unique=True)
    pwd             = CharField()
    email           = CharField()
    create_time     = DateTimeField(default=datetime.datetime.now)

    followed        = False

    def follow_ids(self):
        follows = (User.select(User.id)
                   .join(RelationShip, on=RelationShip.to_user)
                   .where(RelationShip.from_user == self))
        return list(map(lambda x: x.id, follows))

# 关系表
class RelationShip(_Model):
    id              = UUIDField(primary_key=True, default=_uuid)
    from_user       = ForeignKeyField(User, backref='from_user')
    to_user         = ForeignKeyField(User, backref='to_user')

# Service

# 统一查询, 处理异常
def handle_execute(sql):
    try:
        return sql()
    except Exception as e:
        # yLog
        logger_err.error(traceback.format_exc())
        return (ResultCode(ResultCode.sqlException, msg=e), None)

class Service:
    # 用户登录
    def signin(self, name, pwd):
        def _signin():
            try:
                user = User.get(User.name == name, User.pwd == pwd)
                return (ResultSet.success, user)
            except:
                raise SigninError()

        return handle_execute(_signin)

    # 用户列表
    def user_list(self, user):
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

service = Service()