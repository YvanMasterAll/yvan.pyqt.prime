# class Person(object):
#     country = '中国'
#     @classmethod
#     def countryinfo(cls):
#         print(cls.country)
#
#     @classmethod
#     def changecountry(cls,newcountry):
#         cls.country = newcountry
#         # print('此时的国籍是:',cls.country)
#
#     def init(self,name,age,gender):
#         self.name = name
#         self.age = age
#         self.gender = gender
#
# if __name__ == '__main__':
#     # 通过类对象进行调用
#     Person.countryinfo()
#     Person().changecountry('USA')
#     Person.countryinfo()
#     Person().countryinfo()
#     # # 通过实例对象进行调用
#     # zhang = Person
#     # Person.countryinfo()
#     # Person.changecountry('法国')

# import sys
# from PyQt5.QtWidgets import QLabel, QApplication
# from ZzClient.widget.view import BaseView
#
# class DeviceList(BaseView):
#     def __init__(self, *args, **kwargs):
#         super(DeviceList, self).__init__(*args, **kwargs)
#
#         self.procedure()
#
#     def set_ui(self):
#         label = QLabel(self)
#         label.setText("这是设备列表页面")
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = DeviceList()
#     window.show()
#
#     sys.exit(app.exec_())
