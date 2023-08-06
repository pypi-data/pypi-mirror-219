
import json
import sys
import functools
import collections
from collections.abc import MutableSet
# from collections.abc import MutableMapping

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)

class OrderedSet(MutableSet):
    """
    Order set class to created a Ordered set list.
    """

    def __init__(self, iterable=None):
        """
        initialization of OrderSet
        """
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        """
        magic method for length of set
        """
        return len(self.map)

    def __contains__(self, key):
        """
        return Key from the map
        """
        return key in self.map

    def add(self, key):
        """
        Add method of OrderedSet
        """
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        """
        Discard Method
        """
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        """
        Magic Method Iter to iterate over Set
        """
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        """
        magic method reversed
        """
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        """
        Pop method for OrderSet
        """
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        """
        repr method for OrderedSet
        """
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        """
        """
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

old_set = set
set = OrderedSet

def intersection(list1, list2):
    """
    Returns intersections of two list.
    """
    
    L1 = list1
    L2 = list2
    L = list()
    for v1 in L1:
        for v2 in L2:
            if v1 == v2 and v1 not in L:
                L.append(v1)
    return L
   
def union(list1, list2):
    """
    Returns union of two lists.
    """
    
    mapped_list1, mapped_list2 = mapped_list(list1, list2)
    set_union = set(mapped_list1) | set(mapped_list2)
    result = result_set(set_union)
    return result

def symmetric_difference(list1, list2):
    """
    Returns symmetric difference of two lists.
    """
    mapped_list1, mapped_list2 = mapped_list(list1, list2)
    set_difference = set(mapped_list1) ^ set(mapped_list2)
    result = result_set(set_difference)
    return result

def complement(list1, list2):
    """
    Returns Complement of two lists.
    """
    mapped_list1, mapped_list2 = mapped_list(list1, list2)
    set_list1, set_list2 = set(mapped_list1), set(mapped_list2)
    set_complement = set_list1 - set_list2
    result = result_set(set_complement)
    return result

def cartisan_product(list1, list2):
    """
    Returns cartisan product of two lists.
    """
    result = [[x, y]  for x in list1 for y in list2]
    if PY2:
        cartisan_product_list = _byteify(result)
    elif PY3 or PY34:
        cartisan_product_list = result
    cartisan_product_result_list = list(map(functools.partial(
        json.dumps, sort_keys=True), cartisan_product_list))
    cartisan_product_set = set(cartisan_product_result_list)
    if PY3 or PY34:
        # cartisan_product_result = list(map(functools.partial(
        #     json.loads, encoding="utf-8"), cartisan_product_set))
        cartisan_product_result = list(map(json.loads, cartisan_product_set))
    elif PY2:
        cartisan_product_result = list(map(json_loads_byteified, cartisan_product_set))
    return cartisan_product_result

def mapped_list(list1, list2):
    """
    Returns list mapped in json string.
    """
    mapped_list1 = list(map(functools.partial(json.dumps, sort_keys=True), list1))
    mapped_list2 = list(map(functools.partial(json.dumps, sort_keys=True), list2))
    return mapped_list1, mapped_list2

def result_set(set_obj):
    """
    Take set object as argument and return a list object for the given set
    """
    # breakpoint()
    # a = map(functools.partial(json.loads, encoding="utf-8"), set_obj)

    if PY3 or PY34:
        result = list(map(json.loads, set_obj))
    elif PY2:
        result = list(map(json_loads_byteified, set_obj))
    return result
    

def json_loads_byteified(json_text):
    """
    returns byteified of the give data in json representation of data
    """
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True)

def _byteify(data, ignore_dicts=False):
    """
    byteify the unicode in python2.
    """
    # if this is a unicode string, return its string representation
    if isinstance(data, str):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=False) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=False): _byteify(value, ignore_dicts=False)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data
