import datetime as dt
import inspect
import logging
import warnings
from copy import deepcopy
from typing import Iterable, Optional, Tuple, Union

import builtins
import copy
from abc import ABC, ABCMeta, abstractmethod
from collections import namedtuple
from dataclasses import Field, InitVar, MISSING, dataclass, field, fields, replace
from enum import EnumMeta
from functools import update_wrapper
from typing import Iterable, Mapping, Optional, Union, Tuple

import numpy as np
from dataclasses_json import config, global_config
from dataclasses_json.core import _decode_generic, _is_supported_generic
from inflection import camelize, underscore
# from dataclasses_json import global_config

_logger = logging.getLogger(__name__)

__builtins = set(dir(builtins))
__getattribute__ = object.__getattribute__
__setattr__ = object.__setattr__

_rename_cache = {}

def exclude_none(o):
    return o is None


def exlude_always(_o):
    return True


def is_iterable(o, t):
    return isinstance(o, Iterable) and all(isinstance(it, t) for it in o)


def is_instance_or_iterable(o, t):
    return isinstance(o, t) or is_iterable(o, t)


def _get_underscore(arg):
    if arg not in _rename_cache:
        _rename_cache[arg] = underscore(arg)

    return _rename_cache[arg]

def handle_camel_case_args(cls):
    init = cls.__init__

    def wrapper(self, *args, **kwargs):
        normalised_kwargs = {}

        for arg, value in kwargs.items():
            if not arg.isupper():
                snake_case_arg = _get_underscore(arg)
                if snake_case_arg != arg and snake_case_arg in kwargs:
                    raise ValueError('{} and {} both specified'.format(arg, snake_case_arg))

                arg = snake_case_arg

            arg = cls._field_mappings().get(arg, arg)
            normalised_kwargs[arg] = value

        return init(self, *args, **normalised_kwargs)

    cls.__init__ = update_wrapper(wrapper=wrapper, wrapped=init)

    return cls


field_metadata = config(exclude=exclude_none)
name_metadata = config(exclude=exlude_always)

class HashableDict(dict):

    @staticmethod
    def hashables(in_dict) -> Tuple:
        hashables = []
        for it in in_dict.items():
            if isinstance(it[1], dict):
                hashables.append((it[0], HashableDict.hashables(it[1])))
            else:
                hashables.append(it)
        return tuple(hashables)

    def __hash__(self):
        return hash(HashableDict.hashables(self))


class DictBase(HashableDict):

    _PROPERTIES = set()

    def __init__(self, *args, **kwargs):
        if self._PROPERTIES:
            invalid_arg = next((k for k in kwargs.keys() if k not in self._PROPERTIES), None)
            if invalid_arg is not None:
                raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{invalid_arg}'")

        super().__init__(*args, **{camelize(k, uppercase_first_letter=False): v for k, v in kwargs.items()
                                   if v is not None})

    def __getitem__(self, item):
        return super().__getitem__(camelize(item, uppercase_first_letter=False))

    def __setitem__(self, key, value):
        if value is not None:
            return super().__setitem__(camelize(key, uppercase_first_letter=False), value)

    def __getattr__(self, item):
        if self._PROPERTIES:
            if _get_underscore(item) in self._PROPERTIES:
                return self.get(item)
        elif item in self:
            return self[item]

        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{item}'")

    def __setattr__(self, key, value):
        if key in dir(self):
            return super().__setattr__(key, value)
        elif self._PROPERTIES and _get_underscore(key) not in self._PROPERTIES:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'")

        self[key] = value

    @classmethod
    def properties(cls) -> set:
        return cls._PROPERTIES

class Base(ABC):
    """The base class for all generated classes"""

    __fields_by_name = None
    __field_mappings = None

    def __getattr__(self, item):
        fields_by_name = __getattribute__(self, '_fields_by_name')()

        if item.startswith('_') or item in fields_by_name:
            return __getattribute__(self, item)

        # Handle setting via camelCase names (legacy behaviour) and field mappings from disallowed names
        snake_case_item = _get_underscore(item)
        field_mappings = __getattribute__(self, '_field_mappings')()
        snake_case_item = field_mappings.get(snake_case_item, snake_case_item)

        try:
            return __getattribute__(self, snake_case_item)
        except AttributeError:
            return __getattribute__(self, item)

    def __setattr__(self, key, value):
        # Handle setting via camelCase names (legacy behaviour)
        snake_case_key = _get_underscore(key)
        snake_case_key = self._field_mappings().get(snake_case_key, snake_case_key)
        fld = self._fields_by_name().get(snake_case_key)

        if fld:
            if not fld.init:
                raise ValueError(f'{key} cannot be set')

            key = snake_case_key
            value = self.__coerce_value(fld.type, value)

        __setattr__(self, key, value)

    def __repr__(self):
        if self.name is not None:
            return f'{self.name} ({self.__class__.__name__})'

        return super().__repr__()

    @classmethod
    def __coerce_value(cls, typ: type, value):
        if isinstance(value, np.generic):
            # Handle numpy types
            return value.item()
        elif hasattr(value, 'tolist'):
            # tolist converts scalar or array to native python type if not already native.
            return value()
        elif typ in (DictBase, Optional[DictBase]) and isinstance(value, Base):
            return value.to_dict()
        if _is_supported_generic(typ):
            return _decode_generic(typ, value, False)
        else:
            return value

    @classmethod
    def _fields_by_name(cls) -> Mapping[str, Field]:
        if cls is Base:
            return {}

        if cls.__fields_by_name is None:
            cls.__fields_by_name = {f.name: f for f in fields(cls)}

        return cls.__fields_by_name

    @classmethod
    def _field_mappings(cls) -> Mapping[str, str]:
        if cls is Base:
            return {}

        if cls.__field_mappings is None:
            field_mappings = {}
            for fld in fields(cls):
                config_fn = fld.metadata.get('dataclasses_json', {}).get('letter_case')
                if config_fn:
                    mapped_name = config_fn('field_name')
                    if mapped_name:
                        field_mappings[mapped_name] = fld.name

            cls.__field_mappings = field_mappings
        return cls.__field_mappings

    def clone(self, **kwargs):
        """
            Clone this object, overriding specified values

            :param kwargs: property names and values, e.g. swap.clone(fixed_rate=0.01)

            **Examples**

            To change the market data location of the default context:

            >>> from gs_quant.instrument import IRCap
            >>> cap = IRCap('5y', 'GBP')
            >>>
            >>> new_cap = cap.clone(cap_rate=0.01)
        """
        return replace(self, **kwargs)

    @classmethod
    def properties(cls) -> set:
        """The public property names of this class"""
        return set(f[:-1] if f[-1] == '_' else f for f in cls._fields_by_name().keys())

    @classmethod
    def properties_init(cls) -> set:
        """The public property names of this class"""
        return set(f[:-1] if f[-1] == '_' else f for f, v in cls._fields_by_name().items() if v.init)

    def as_dict(self, as_camel_case: bool = False) -> dict:
        """Dictionary of the public, non-null properties and values"""

        # to_dict() converts all the values to JSON type, does camel case and name mappings
        # asdict() does not convert values or case of the keys or do name mappings

        ret = {}
        field_mappings = {v: k for k, v in self._field_mappings().items()}

        for key in self.__fields_by_name.keys():
            value = __getattribute__(self, key)
            key = field_mappings.get(key, key)

            if value is not None:
                if as_camel_case:
                    key = camelize(key, uppercase_first_letter=False)

                ret[key] = value

        return ret

    @classmethod
    def default_instance(cls):
        """
        Construct a default instance of this type
        """
        required = {f.name: None if f.default == MISSING else f.default for f in fields(cls) if f.init}
        return cls(**required)

    def from_instance(self, instance):
        """
        Copy the values from an existing instance of the same type to our self
        :param instance: from which to copy:
        :return:
        """
        if not isinstance(instance, type(self)):
            raise ValueError('Can only use from_instance with an object of the same type')

        for fld in fields(self.__class__):
            if fld.init:
                __setattr__(self, fld.name, __getattribute__(instance, fld.name))

class InstrumentBase(Base, ABC):

    quantity_: InitVar[float] = field(default=1, init=False)

    @property
    @abstractmethod
    def provider(self):
        ...

    @property
    def instrument_quantity(self) -> float:
        return self.quantity_

"""
    @property
    def resolution_key(self) -> Optional[RiskKey]:
        try:
            return self.__resolution_key
        except AttributeError:
            return None
"""
    @property
    def unresolved(self):
        try:
            return self.__unresolved
        except AttributeError:
            return None

    @property
    def metadata(self):
        try:
            return self.__metadata
        except AttributeError:
            return None

    @metadata.setter
    def metadata(self, value):
        self.__metadata = value

    def from_instance(self, instance):
        self.__resolution_key = None
        super().from_instance(instance)
        self.__unresolved = instance.__unresolved
        self.__resolution_key = instance.__resolution_key

    def resolved(self, values: dict, resolution_key: RiskKey):
        all_values = self.as_dict(True)
        all_values.update(values)
        new_instrument = self.from_dict(all_values)
        new_instrument.name = self.name
        new_instrument.__unresolved = copy.copy(self)
        new_instrument.__resolution_key = resolution_key
        return new_instrument

    def clone(self, **kwargs):
        new_instrument = super().clone(**kwargs)
        new_instrument.__unresolved = self.unresolved
        new_instrument.metadata = self.metadata
        new_instrument.__resolution_key = self.resolution_key
        return new_instrument


class Instrument(object):
    PROVIDER = 'local'

    __instrument_mappings = {}

