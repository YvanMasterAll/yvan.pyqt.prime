

class BaseBloc:

    @property
    def _parent(self):
        return self.parent()