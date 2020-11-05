from peewee import *
import datetime
import uuid
import logging
from util.http import *
from ZzClient.common.util.logger import logger_err
import traceback
from ZzClient.config.error import *

'''
数据库
'''

database = SqliteDatabase("zzclient.db")

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

'''
数据模型
'''

class BaseModel(Model):
    class Meta:
        database = database

def uuid():
    return uuid.uuid1()

'''
用户表
'''

class User(BaseModel):
    id              = UUIDField(primary_key=True, default=uuid)
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

'''
关系表
'''

class RelationShip(BaseModel):
    id              = UUIDField(primary_key=True, default=uuid)
    from_user       = ForeignKeyField(User, backref='from_user')
    to_user         = ForeignKeyField(User, backref='to_user')