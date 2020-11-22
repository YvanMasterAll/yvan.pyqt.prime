
'''
数据块基类
'''

class BaseBloc:

    @property
    def _parent(self):
        return self.parent()