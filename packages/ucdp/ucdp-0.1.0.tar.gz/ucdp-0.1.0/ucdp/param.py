#
# MIT License
#
# Copyright (c) 2023 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
Module Parameter .

Usage:

>>> from tabulate import tabulate
>>> import ucdp
>>> ucdp.Param(ucdp.UintType(6), "param_p")
Param(UintType(6), 'param_p')

Also complex types can simply be used:

>>> class AType(ucdp.AStructType):
...     def _build(self):
...         self._add("req", ucdp.BitType())
...         self._add("data", ucdp.ArrayType(ucdp.UintType(16), 5))
...         self._add("ack", ucdp.BitType(), ucdp.BWD)
...         self._add("error", ucdp.BitType(), ucdp.BIDIR)
>>> class MType(ucdp.AEnumType):
...     keytype = ucdp.UintType(2)
...     def _build(self):
...         self._add(0, "Linear")
...         self._add(1, "Cyclic")
>>> class BType(ucdp.AStructType):
...     def _build(self):
...         self._add("foo", AType())
...         self._add("mode", MType())
...         self._add("bar", ucdp.ArrayType(AType(), 3), ucdp.BWD)

These types are automatically resolved by iterating over the parameter:

>>> param = ucdp.Param(BType(), "param_p")
>>> for item in param:
...     print(repr(item))
Param(BType(), 'param_p')
Param(AType(), 'param_foo_p', level=1)
Param(BitType(), 'param_foo_req_p', level=2)
Param(UintType(16), 'param_foo_data_p', level=2, dims=(Slice('0:4'),))
Param(BitType(), 'param_foo_ack_p', level=2)
Param(BitType(), 'param_foo_error_p', level=2)
Param(MType(), 'param_mode_p', level=1)
Param(AType(), 'param_bar_p', level=1, dims=(Slice('0:2'),))
Param(BitType(), 'param_bar_req_p', level=2, dims=(Slice('0:2'),))
Param(UintType(16), 'param_bar_data_p', level=2, dims=(Slice('0:2'), Slice('0:4')))
Param(BitType(), 'param_bar_ack_p', level=2, dims=(Slice('0:2'),))
Param(BitType(), 'param_bar_error_p', level=2, dims=(Slice('0:2'),))
"""

from typing import Iterator, Tuple

from .attrs import field, frozen
from .ident import Ident


@frozen(cmp=False, hash=True)
class Param(Ident):
    """
    Module Parameter.

    Args:
        type_ (AType): Type.
        name (Name()): Name.

    Keyword Args:
        doc (Doc): Documentation Container
        value: Value.

    Parameter names should end with '_p', but must not.

    >>> import ucdp
    >>> cnt = ucdp.Param(ucdp.UintType(6), "cnt_p")
    >>> cnt
    Param(UintType(6), 'cnt_p')
    >>> cnt.type_
    UintType(6)
    >>> cnt.name
    'cnt_p'
    >>> cnt.basename
    'cnt'
    >>> cnt.suffix
    '_p'
    >>> cnt.doc
    Doc()
    >>> cnt.value

    If the parameter is casted via `int()` it returns `value` if set, other `type_.default`.

    >>> int(ucdp.Param(ucdp.UintType(6, default=2), "cnt_p"))
    2
    >>> int(ucdp.Param(ucdp.UintType(6, default=2), "cnt_p", value=4))
    4

    Parameter are Singleton:

    >>> ucdp.Param(ucdp.UintType(6), "cnt_p") is ucdp.Param(ucdp.UintType(6), "cnt_p")
    True
    """

    _suffixes: Tuple[str, ...] = ("_p",)

    value = field(default=None, kw_only=True)

    @value.validator
    def _value_validator(self, attribute, value):
        # pylint: disable=unused-argument
        if value is not None:
            self.type_.check(value)

    def __int__(self):
        value = self.value
        if value is None:
            value = self.type_.default
        return int(value or 0)

    def iter(self, filter_=None, stop=None, maxlevel=None, value=None) -> Iterator:
        """Iterate over Parameter Hierarchy."""
        # if value is None:
        #     value = self.value
        return super().iter(filter_=filter_, stop=stop, maxlevel=maxlevel, value=value)

    def get(self, name, value=None) -> Iterator:
        """Get a specific member in the Parameter Hierarchy."""
        # if value is None:
        #     value = self.value
        return super().get(name, value=value)
