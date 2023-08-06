# -*- encoding:utf-8 -*-
import copy, hashlib, json, inspect, pdb
import pandas as pd
import six as six
from abc import ABCMeta, abstractmethod
from jdwdata.RetrievalAPI import get_data_by_map
from alchemevent.kdutils.create_id import create_id
from alchemevent.kdutils.lazy import LazyFunc
from alchemevent.kdutils.base import ParamBase, FreezeAttrMixin


def _weighted(data):
    weighted = data / data.sum()
    return weighted


class LongCallMixin(FreezeAttrMixin):
    """
        混入类，混入代表多头，不完全是期权中buy call的概念，
    """

    @LazyFunc
    def long_type_str(self):
        """用来区别多头类型unique 值为call"""
        return "long"

    @LazyFunc
    def expect_direction(self):
        """期望收益方向，1.0即正向期望"""
        return 1.0


class ShortCallMixin(FreezeAttrMixin):
    """
        混入类，混入代表空头，应用场景在于期权，期货策略中，
        不完全是期权中buy put的概念，只代看跌反向操作，
        即期望买入后交易目标价格下跌，下跌带来收益
    """

    @LazyFunc
    def short_type_str(self):
        """用来区别买入类型unique 值为put"""
        return "short"

    @LazyFunc
    def expect_direction(self):
        """期望收益方向，1.0即反向期望"""
        return -1.0


class EventBase(six.with_metaclass(ABCMeta, ParamBase)):

    def __init__(self, **kwargs):
        # 子类继续完成自有的构造
        self._init_self(**kwargs)
        self.data_client = get_data_by_map
        self.dummy_name = 'dummy120_fst' if 'dummy_name' not in kwargs else kwargs['dummy_name']
        self.method = 'ddb' if 'method' not in kwargs else kwargs['method']
        self.begin_date = kwargs['begin_date']
        self.end_date = kwargs['end_date']
        self.dummy_data = self.data_client([self.dummy_name],
                                           begin_date=self.begin_date,
                                           end_date=self.end_date,
                                           method=self.method)
        self.dummy_data = self.dummy_data[self.dummy_name]

    @abstractmethod
    def _init_self(self, **kwargs):
        """子类因子针对可扩展参数的初始化"""
        pass

    def _create_id(self, **kwargs):
        feature = copy.deepcopy(kwargs)
        s = hashlib.md5(
            json.dumps(feature).encode(encoding="utf-8")).hexdigest()
        return "{0}".format(create_id(original=s, digit=10))

    def _format(self, data, **kwargs):
        data = data / data
        data = data.stack()
        weighted = data.groupby(
            level='trade_date').apply(lambda x: _weighted(x))
        weighted.name = self.name
        weighted.id = self._create_id(name=self.name, **kwargs)
        return weighted