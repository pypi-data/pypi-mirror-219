# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Data methods.
"""


from typing import Any, List, Dict, Iterable, Literal, Optional, NoReturn, overload

from .rbase import is_iterable, check_least_one, check_most_one, to_type


__all__ = (
    "count",
    "flatten",
    "split",
    "unique",
    "ins",
    "mutual_in"
)


def count(
    data: Any,
    _count_value: Dict = {"size": 0, "total": 0, "types": {}},
    _surface: bool = True
) -> Dict[Literal["size", "total", "types"], Any]:
    """
    `Count` data element.

    Parameters
    ----------
    data : Data.
    _count_value : Cumulative Count.
    _surface : Whether is surface recursion.

    Returns
    -------
    Count data.

    Examples
    --------
    >>> count([1, 'b', [3, 4]])
    {'size': 4, 'total': 6, 'types': {<class 'int'>: 3, <class 'list'>: 2, <class 'str'>: 1}}
    """

    # Count Element.
    _count_value["total"] += 1
    _count_value["types"][data.__class__] = _count_value["types"].get(data.__class__, 0) + 1

    # Recursion.
    if data.__class__ == dict:
        for element in data.values():
            count(element, _count_value, False)
    elif is_iterable(data):
        for element in data:
            count(element, _count_value, False)
    else:
        _count_value["size"] = _count_value["size"] + 1

    # End Recursion and return.
    if _surface:

        ## Sort by count.
        sorted_func = lambda key: _count_value["types"][key]
        sorted_key = sorted(_count_value["types"], key=sorted_func, reverse=True)
        _count_value["types"] = {key: _count_value["types"][key] for key in sorted_key}

        return _count_value


def flatten(data: Any, flattern_data: List = []) -> List:
    """
    `Flatten` data.

    Parameters
    ----------
    data : Data.
    flattern_data : Recursion cumulative data.

    Returns
    -------
    Data after flatten.
    """

    # Flatten.

    ## Recursion dict object.
    if data.__class__ == dict:
        for element in data.values():
            _ = flatten(element, flattern_data)

    ## Recursion iterator.
    elif is_iterable(data):
        for element in data:
            _ = flatten(element, flattern_data)

    ## Other.
    else:
        flattern_data.append(data)

    return flattern_data


@overload
def split(data: Iterable, share: None = None, bin_size: None = None) -> NoReturn: ...

@overload
def split(data: Iterable, share: int = None, bin_size: int = None) -> NoReturn: ...

@overload
def split(data: Iterable, share: Optional[int] = None, bin_size: Optional[int] = None) -> List[List]: ...

def split(data: Iterable, share: Optional[int] = None, bin_size: Optional[int] = None) -> List[List]:
    """
    `Split` data into multiple data.

    Parameters
    ----------
    data : Data.
    share : Number of splie share.
    bin_size : Size of each bin.

    Returns
    -------
    Split data.
    """

    # Check parameter.
    check_least_one(share, bin_size)
    check_most_one(share, bin_size)

    # Handle parameter.
    data = list(data)

    # Split.
    data_len = len(data)
    _data = []
    _data_len = 0

    ## by number of share.
    if share is not None:
        average = data_len / share
        for n in range(share):
            bin_size = int(average * (n + 1)) - int(average * n)
            _data = data[_data_len:_data_len + bin_size]
            _data.append(_data)
            _data_len += bin_size

    ## By size of bin.
    elif bin_size is not None:
        while True:
            _data = data[_data_len:_data_len + bin_size]
            _data.append(_data)
            _data_len += bin_size
            if _data_len > data_len:
                break

    return _data


def unique(data: Iterable) -> List:
    """
    `De duplication` of data.

    Parameters
    ----------
    data : Data.

    Returns
    -------
    List after de duplication.
    """

    # Handle parameter.
    data = to_type(data, tuple)

    # Delete duplicate.
    data_unique = list(set(data))
    data_unique.sort(key=data.index)
    return data_unique


def ins(obj: Any, *arrays: Iterable) -> bool:
    """
    `Judge` whether the object is in multiple array.

    Parameters
    ----------
    obj : Judge object.
    arrays : Array.

    Returns
    -------
    Judge result.
    """

    # Judge.
    for array in arrays:
        if obj in array:
            return True

    return False


def mutual_in(*arrays: Iterable) -> bool:
    """
    Whether the same element exists in `multiple` array.

    Parameters
    ----------
    arrays : Array.

    Returns
    -------
    Judge result.
    """

    # Handle parameter.
    arrays = list(arrays)

    # Judge.
    for n, array in enumerate(arrays):
        for after_array in arrays[n+1:]:
            for element in array:
                if ins(element, after_array):
                    return True

    return False