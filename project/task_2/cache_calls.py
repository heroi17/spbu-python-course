from typing import Callable, Any, Union, Generator
from inspect import getfullargspec, FullArgSpec
from functools import lru_cache, wraps


def make_key(
    args: tuple[Any, ...], kwds: dict[str, Any], kwd_mark: tuple[Any, ...] = (object(),)
) -> tuple[Any]:
    """
    Make tuple from args and kwds, because dict is not hasheble type.

    ----------
    Params:
    ----------
    args: tuple
        Unnamed param.

    kwds: dict
        Named param.

    ----------
    Returns:
    ----------
    tuple
        The hashable equivalent of the parameters
    """
    key: tuple[Any, ...] = args
    if kwds:
        sorted_items: list[Any] = sorted(kwds.items())
        key += kwd_mark
        for item in sorted_items:
            key += item
    return key


def get_new_id() -> Generator[int, None, None]:
    """
    Simple generater of number. Always return new numbers.
    """
    ind_counter: int = 0
    while True:
        ind_counter += 1
        yield ind_counter


class LinkedList:
    """
    LinkedList is a support class for cache_calls.

    ----------
    Methods:
    ----------
    __init__(self) -> None
        Just init internall data.

    delete(self, id_to_del: int) -> int
        Pop the node with id: id_to_del from data structure.
        Return the data into the node.

    push_back(self, value: Any) -> int
        Push at the end of linked list new node and set there value.
        Return id of a new node.

    pop_front(self) -> Any
        Delete first elem.
        Retern lost value.
    """

    def __init__(self) -> None:
        """
        Init internal data.
        """
        self._id_generator: Generator[int, None, None] = get_new_id()
        self._head: int = next(self._id_generator)
        self._tail: int = next(self._id_generator)
        self._data: dict[int, list[Any]] = {
            self._head: [None, self._tail, None],
            self._tail: [self._head, None, None],
        }

    def _insert_after(self, id_before: int, value: Any) -> int:
        """
        ----------
        INTERNAL METHOD
        ----------
        Insert new node with value after node with id: id_before.

        ----------
        Params:
        ----------
        id_before: int
            id of the node before new one.

        value: Any
            Value of node is main data that contain this structer.
            Can be any type, but here we use it as tuple.

        ----------
        Returns:
        ----------
        int
            Id of new inserted node.
        """
        new_id: int = next(self._id_generator)
        id_after: int = self._data[id_before][1]
        self._data[new_id] = [id_before, id_after, value]
        self._data[id_before][1] = new_id
        self._data[id_after][0] = new_id
        return new_id

    def _detuch(self, id_to_detuch: int) -> None:
        """
        ----------
        INTERNAL METHOD
        ----------
        Detuch node with id, but not delete it.
        After call nodes do not point on node with id: id_to_del

        ----------
        Params:
        ----------
        id_to_detuch: int
            id of the node
        """
        self._data[self._data[id_to_detuch][0]][1] = self._data[id_to_detuch][1]
        self._data[self._data[id_to_detuch][1]][0] = self._data[id_to_detuch][0]

    def delete(self, id_to_del: int) -> Any:
        """
        Detuch and delete node with id: id_to_del

        ----------
        Params:
        ----------
        id_to_del: int
            id of the node we should to delete.

        ----------
        Returns:
        ----------
        Any
            The data that our structure just contained at node with id: id_to_del.
        """
        self._detuch(id_to_del)
        value: Any = self._data[id_to_del][2]
        del self._data[id_to_del]
        return value

    def push_back(self, value: Any) -> int:
        """
        Push at the end of Linked List new one node and return it''s id.

        ----------
        Params:
        ----------
        value: Any
            The data that our structure should contain at new node.

        ----------
        Returns:
        ----------
        int
            Id of new node.
        """
        return self._insert_after(self._data[self._tail][0], value)

    def pop_front(self) -> Any:
        """
        pop the firxt elem of Linked List.

        ----------
        Returns:
        ----------
        Any
            Value that node just contained.
        """
        return self.delete(self._data[self._head][1])


class DictCache:
    """
    Structure that contain data like dict, but remove oldest (in term of use) elem after overflow.
    Problem: when overflow, should find the oldest elem.
    To solwe it i use LinkedList as timeline.
    LinkedList is a support class for cache_calls.

    ----------
    Methods:
    ----------
    __init__(self, *, maxcount: int) -> None
        Just init internall data.

    add(self, id_to_del: int) -> int
        Pop the node with id: id_to_del from data structure.
        Return the data into the node.

    push_back(self, value: Any) -> int
        Push at the end of linked list new node and set there value.
        Return id of a new node.

    pop_front(self) -> Any
        Delete first elem.
        Retern lost value.
    """

    def __init__(self, *, maxcount: int) -> None:
        self._data: dict[tuple[Any], Any] = {}
        self._linked_list = LinkedList()
        self.maxcount = maxcount
        self.count = 0

    def _update_key(self, key: tuple[Any]) -> None:
        """
        ----------
        INTERNAL METHOD
        ----------
        Make value with this key hier then others values.

        ----------
        Params:
        ----------
        key: Any
            Key for sucsessing to value.
        """
        self._linked_list.delete(self._data[key][1])
        self._data[key][1] = self._linked_list.push_back(key)

    def add(self, key: tuple[Any], value: Any) -> None:
        """
        Add new answer into the cache.

        ----------
        Params:
        ----------
        key: Any
            Key for sucsessing to value.

        value: Any
            The data that this structure containing under the key.
        """

        if self.count >= self.maxcount:
            key_to_del = self._linked_list.pop_front()
            del self._data[key_to_del]
        else:
            self.count += 1
        if key in self:
            raise ValueError("Cannot add the value, it's already there")
        ptr_on_node = self._linked_list.push_back(key)
        self._data[key] = [value, ptr_on_node]

    def __contains__(self, key: tuple[Any]) -> bool:
        """
        Return true if key into the DictCache.

        ----------
        Params:
        ----------
        key: Any
            Key we are checking for in structure.

        ----------
        Returns:
        ----------
        bool
            True if key here.
            Else - otherwise.
        """
        return key in self._data

    def __getitem__(self, key: tuple[Any]) -> Any:
        """
        return data under key if it exist, otherwise throow error.
        +Apdate the priorety.

        ----------
        Params:
        ----------
        key: Any
            Key for the value.

        ----------
        Returns:
        ----------
        Any
            Value under the key
        """
        self._update_key(key)
        return self._data[key][0]


def cache_calls(
    function: Union[Callable[..., Any], None] = None, *, capacity: int = 0
) -> Callable[..., Any]:
    """
    Analog of lru_cache from itertools.

    ----------
    Params:
    ----------
    function:
        Func that we decorate to cache calls.

    capacity: int
        The max count of answers that this struct can contain.
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")

    if function is None:
        return lambda func: cache_calls(function=func, capacity=capacity)

    if capacity == 0:
        return function

    hashed_data: DictCache = DictCache(maxcount=capacity)

    @wraps(function)
    def inner(*args: Any, **kwds: Any) -> Any:
        nonlocal hashed_data
        nonlocal function
        nonlocal capacity
        key: tuple[Any] = make_key(args, kwds)
        if not (key in hashed_data):
            hashed_data.add(key, function(*args, **kwds))
        return hashed_data[key]

    return inner
