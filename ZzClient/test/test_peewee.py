from db.model import *

if __name__ == "__main__":

    # # 创建User表
    User.drop_table()
    RelationShip.drop_table()
    User.create_table()
    RelationShip.create_table()
    # 插入数据
    user1 = User.create(name="yi", pwd="123", email="")
    user2 = User.create(name="vi", pwd="123", email="")
    user3 = User.create(name="ti", pwd="123", email="")
    RelationShip.create(from_user=user1, to_user=user2)
    RelationShip.create(from_user=user1, to_user=user3)
    try:
        users = User.select().where(User.name is not None)
        for user in users:
            print(user.name)
    except Exception as e:
        print(e)
    print("----------------------------------------")
    # 测试登录
    res1 = service.signin(name="yi", pwd="123")
    result1 = res1[0]
    data1 = res1[1]
    if result1.valid:
        print(data1.name)
    else:
        print(result1.msg)
    print("----------------------------------------")
    # 测试联表查询
    "select u2.id from user u2 join relationship r1 on u2.id = r1.to_user where r1.from_user = '3abf000c93f311e99b7528cfe9127877';" # 查询关注的用户
    res2 = service.user_list(user1)
    result2 = res2[0]
    data2 = res2[1]
    if result2.valid:
        for user in data2:
            print(user.followed)
    else:
        print(result2.msg)
    # 测试事务
    # with database.atomic() as transaction:
    #     User.create(name="ti2", pwd="123", email="")
    #     User.create(name="ti", pwd="123", email="")
