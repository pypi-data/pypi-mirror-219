#!/usr/bin/python3
# -*- coding: utf-8 -*-


class PlistItem:
    def __init__(self, item_index_tuple, item, data=None, item_index_head=''):
        """

        :param item_index_tuple:
        :param item: 当前节点在 .plist 中的名称 (key值)
        :param data: 当前节点的数据
        :param item_index_head: 当前节点的 前缀头数据 在  __pos__ __neg__ __invert__ 中引用拼接 节点路径前缀
        """
        self.item_index_tuple = item_index_tuple
        self.item = item
        self.item_index_head = item_index_head
        self.data = data
        self.dict = None
        self.dict_index = None
        self.path = None
        self.path_tuple = None
        self.update()

    def update(self, item_index_tuple=None, item=None, data=None, item_index_head=None):
        """
        更新实例属性 也相当于更新节点属性
        :param item_index_tuple:
        :param item: 当前节点在 .plist 中的名称 (key值)
        :param data: 当前节点的数据
        :param item_index_head: 当前节点的 前缀头数据 在  __pos__ __neg__ __invert__ 中引用拼接 节点路径前缀
        :return:
        """
        item_index_tuple = self.item_index_tuple if item_index_tuple == None else item_index_tuple
        item = self.item if item == None else item
        item_index_head = self.item_index_head if item_index_head == None else item_index_head

        dict_index = None
        path = None
        dict_ = {}
        index_ = dict_
        tuple_item = item_index_tuple + (item,)
        tuple_item_last = len(tuple_item) - 1
        for item_ in tuple_item:
            dict_index = f'{dict_index}["{item_}"]' if dict_index != None else f'["{item_}"]'
            path = f'{path}.{item_}' if path != None else f'{item_}'
            index_[item_] = {} if tuple_item.index(item_) < tuple_item_last else data
            index_ = index_[item_]
        dict_index, path, path_tuple = (
                                            f'{item_index_head}{dict_index}',
                                            f'{item_index_head}.{path}',
                                            item_index_tuple + (item,)
                                        ) if item_index_head else (
                                            dict_index,
                                            path,
                                            item_index_tuple + (item,)
                                        )

        self.item_index_tuple = item_index_tuple
        self.item = item
        self.item_index_head = item_index_head
        self.data = data
        self.dict = dict_
        self.dict_index = dict_index
        self.path = path
        self.path_tuple = path_tuple
        return (self.item_index_tuple,
                self.item,
                self.item_index_head,
                self.dict_index,
                self.path,
                self.path_tuple,
                )

    def simplification_dict(self, plist_dict=None):
        """
        将当前节点以及下级节点 转换为 PlistParser 解析器 接受的 dict
        :param plist_dict: 指定该参数 则 会将 解析的dict数据更新在 指定的 plist_dict 中
        :return: 完成解析的 dict
        """
        plist_dict = {} if plist_dict == None else plist_dict
        for self_item,  self_item_value in self.__dict__.items():
            if isinstance(self_item_value, PlistItem):
                item = self_item_value.item
                index_tuple = self_item_value.item_index_tuple
                data = self_item_value.data
                item_item = {} if item in index_tuple else data
                plist_dict[item] = item_item if item in index_tuple else data
                if type(item_item) == dict:
                    self_item_value.simplification_dict(item_item)
        return plist_dict

    def __pos__(self):
        """
        重载 单目运算符 +
        :return:
        """
        return self.dict_index

    def __neg__(self):
        """
        重载 单目运算符 -
        :return:
        """
        return self.simplification_dict()

    def __invert__(self):
        """
        重载 单目运算符 ~
        :return:
        """
        return self.path_tuple


class PlistCacheExtraItem(PlistItem):
    pass


class PlistCacheExtra(PlistItem):
    def __init__(self, item_index_tuple, item, item_index_head=''):
        super().__init__(item_index_tuple, item, item_index_head=item_index_head)
        self.device_category = PlistCacheExtraItem(item_index_tuple, 'VuGdqp8UBpi9vPWHlPluVQ',
                                                   item_index_head=item_index_head)  #: ['iPhone15,3'],
        self.device_issuance = PlistCacheExtraItem(item_index_tuple, 'zHeENZu+wbg7PUprwNwBWg',
                                                   item_index_head=item_index_head)  # : 'CH/A',
        self.device_model = PlistCacheExtraItem(item_index_tuple, 'Z/dqyWS6OZTRy10UcmUAhw',
                                                item_index_head=item_index_head)  # : 'iPhone14 Pro Max',
        self.device_system = PlistCacheExtraItem(item_index_tuple, 'ivIu8YTDnBSrYv/SN4G8Ag',
                                                 item_index_head=item_index_head)  # : 'iPhone OS',


class Plist(PlistItem):
    def __init__(self, item_index_tuple=None, item='Plist', data=None, item_index_head=''):
        item_index_tuple = () if item_index_tuple == None else item_index_tuple
        super().__init__(item_index_tuple, item, item_index_head=item_index_head)
        self.CacheUUID = PlistItem(item_index_tuple, 'CacheUUID')
        self.CacheData = PlistItem(item_index_tuple, 'CacheData')
        self.CacheVersion = PlistItem(item_index_tuple, 'CacheVersion')
        self.CacheExtra = PlistCacheExtra(('CacheExtra',), 'CacheExtra')
