class AbstractMenu(object):
    is_title = False
    name = ''
    url = ''
    key = ''
    icon = ''
    submenu = []

    def __init__(self, name, url, icon):
        super(AbstractMenu, self).__init__()
        self.is_title = True
        self.submenu = []
        self.name = name
        self.url = url
        self.icon = icon

    def add(self, *args):
        self.submenu += list(args)
        return self

    @property
    def str_hassub_class(self):
        if self.submenu:
            return ' has-sub'
        else:
            return ''


class TitleMenu(AbstractMenu):

    def __init__(self, name):
        super(TitleMenu, self).__init__(name=name, url=None, icon=None)
        self.is_title = False


class ItemMenu(AbstractMenu):

    def __init__(self, name, url, icon):
        super(ItemMenu, self).__init__(name=name, url=url, icon=icon)
        self.is_title = False


class ItemSubMenu(AbstractMenu):

    def __init__(self, name, url, icon):
        super(ItemSubMenu, self).__init__(name=name, url=url, icon=icon)
        self.is_title = False
