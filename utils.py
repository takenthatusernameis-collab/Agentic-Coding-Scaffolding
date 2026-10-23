"""Utility helper functions."""

from typing import Any, Callable, Dict, List, Optional, Protocol, Set, TypeVar, Union


class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...


T = TypeVar("T")
CT = TypeVar("CT", bound=Comparable)
U = TypeVar("U")
K = TypeVar("K")
V = TypeVar("V")


def flatten(lst: List[List[T]]) -> List[T]:
    """Flatten a list of lists into a single list."""
    result: List[T] = []
    for item in lst:
        result.extend(item)
    return result


def chunk(lst: List[T], size: int) -> List[List[T]]:
    """Split a list into chunks of the specified size."""
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def unique(lst: List[T]) -> List[T]:
    """Return a list of unique elements preserving order."""
    seen: Set[Any] = set()
    result: List[T] = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def is_empty(value: Any) -> bool:
    """Check if a value is considered empty."""
    if value is None:
        return True
    if isinstance(value, (str, list, tuple, set, dict)):
        return len(value) == 0
    return False


def remove_none(lst: List[Any]) -> List[Any]:
    """Return a copy of lst with None values removed."""
    return [item for item in lst if item is not None]


def last(lst: List[T]) -> T:
    """Return the last element of a non-empty list."""
    if not lst:
        raise ValueError("List must not be empty")
    return lst[-1]


def first(lst: List[T]) -> T:
    """Return the first element of a non-empty list."""
    if not lst:
        raise ValueError("List must not be empty")
    return lst[0]


def second(lst: List[T]) -> T:
    """Return the second element of a non-empty list."""
    if len(lst) < 2:
        raise ValueError("List must have at least two elements")
    return lst[1]


def compact(lst: List[T]) -> List[T]:
    """Return a copy of lst with falsy values removed."""
    return [item for item in lst if item]


def take(lst: List[T], n: int) -> List[T]:
    """Return the first n elements of a list."""
    if n <= 0:
        return []
    return lst[:n]


def drop(lst: List[T], n: int) -> List[T]:
    """Return a list with the first n elements removed."""
    if n <= 0:
        return list(lst)
    return lst[n:]


def tail(lst: List[T], n: int) -> List[T]:
    """Return the last n elements of a list."""
    if n <= 0:
        return []
    if n >= len(lst):
        return list(lst)
    return lst[-n:]


def head(lst: List[T], n: int) -> List[T]:
    """Return the first n elements of a list (alias for take)."""
    return take(lst, n)


def rest(lst: List[T]) -> List[T]:
    """Return a list with the first element removed."""
    if not lst:
        return []
    return lst[1:]


def initial(lst: List[T]) -> List[T]:
    """Return all elements except the last."""
    if not lst:
        return []
    return lst[:-1]


def partition(lst: List[T], predicate: Callable[[T], bool]) -> List[List[T]]:
    """Split a list into two lists based on a predicate."""
    truthy: List[T] = []
    falsy: List[T] = []
    for item in lst:
        if predicate(item):
            truthy.append(item)
        else:
            falsy.append(item)
    return [truthy, falsy]


def group_by(lst: List[T], key: Callable[[T], K]) -> Dict[K, List[T]]:
    """Group elements by the result of a key function."""
    result: Dict[K, List[T]] = {}
    for item in lst:
        k = key(item)
        if k not in result:
            result[k] = []
        result[k].append(item)
    return result


def index_by(lst: List[T], key: Callable[[T], K]) -> Dict[K, T]:
    """Index elements by the result of a key function."""
    result: Dict[K, T] = {}
    for item in lst:
        result[key(item)] = item
    return result


def zip_with(lst1: List[T], lst2: List[U], fn: Callable[[T, U], V]) -> List[V]:
    """Zip two lists together using a combining function."""
    result: List[V] = []
    for a, b in zip(lst1, lst2):
        result.append(fn(a, b))
    return result


def concat(*lists: List[T]) -> List[T]:
    """Concatenate multiple lists into one."""
    result: List[T] = []
    for lst in lists:
        result.extend(lst)
    return result


def intersection(lst1: List[T], lst2: List[T]) -> List[T]:
    """Return elements that appear in both lists preserving order from lst1."""
    set2 = set(lst2)
    seen: Set[T] = set()
    result: List[T] = []
    for item in lst1:
        if item in set2 and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def difference(lst1: List[T], lst2: List[T]) -> List[T]:
    """Return elements in lst1 that are not in lst2 preserving order."""
    set2 = set(lst2)
    result: List[T] = []
    for item in lst1:
        if item not in set2:
            result.append(item)
    return result


def union(lst1: List[T], lst2: List[T]) -> List[T]:
    """Return unique elements from both lists preserving order."""
    return unique(concat(lst1, lst2))


def pluck(lst: List[Dict[K, V]], key: K) -> List[V]:
    """Extract values for a key from a list of dictionaries."""
    result: List[V] = []
    for item in lst:
        if isinstance(item, dict) and key in item:
            result.append(item[key])
    return result


def pick(d: Dict[K, V], keys: List[K]) -> Dict[K, V]:
    """Pick specific keys from a dictionary."""
    result: Dict[K, V] = {}
    for key in keys:
        if key in d:
            result[key] = d[key]
    return result


def omit(d: Dict[K, V], keys: List[K]) -> Dict[K, V]:
    """Omit specific keys from a dictionary."""
    keys_set = set(keys)
    result: Dict[K, V] = {}
    for key, value in d.items():
        if key not in keys_set:
            result[key] = value
    return result


def merge(*dicts: Dict[K, V]) -> Dict[K, V]:
    """Merge multiple dictionaries, with later dicts taking precedence."""
    result: Dict[K, V] = {}
    for d in dicts:
        result.update(d)
    return result


def get(d: Dict[K, Any], key: K, default: Any = None) -> Any:
    """Get a value from a dictionary with a default."""
    if not isinstance(d, dict):
        return default
    return d.get(key, default)


def has_key(d: Dict[K, Any], key: K) -> bool:
    """Check if a dictionary has a key."""
    return isinstance(d, dict) and key in d


def range_list(start: int, stop: Optional[int] = None, step: int = 1) -> List[int]:
    """Create a list from a range."""
    if stop is None:
        return list(range(start))
    return list(range(start, stop, step))


def repeat(item: T, n: int) -> List[T]:
    """Repeat an item n times."""
    if n <= 0:
        return []
    return [item] * n


def sample(lst: List[T], n: int = 1) -> List[T]:
    """Return n random samples from a list (without replacement if possible)."""
    import random

    if n <= 0:
        return []
    if n >= len(lst):
        result = list(lst)
        random.shuffle(result)
        return result
    return random.sample(lst, n)


def shuffle(lst: List[T]) -> List[T]:
    """Return a shuffled copy of a list."""
    import random

    result = list(lst)
    random.shuffle(result)
    return result


def map_list(fn: Callable[[T], U], lst: List[T]) -> List[U]:
    """Map a function over a list (alias for list(map(...)))."""
    return [fn(item) for item in lst]


def filter_list(fn: Callable[[T], bool], lst: List[T]) -> List[T]:
    """Filter a list using a predicate (alias for list(filter(...)))."""
    return [item for item in lst if fn(item)]


def reduce_list(fn: Callable[[U, T], U], lst: List[T], initial: U) -> U:
    """Reduce a list using a function."""
    result = initial
    for item in lst:
        result = fn(result, item)
    return result


def for_each(fn: Callable[[T], Any], lst: List[T]) -> None:
    """Apply a function to each element of a list."""
    for item in lst:
        fn(item)


def find(lst: List[T], predicate: Callable[[T], bool]) -> Optional[T]:
    """Find the first element matching a predicate."""
    for item in lst:
        if predicate(item):
            return item
    return None


def find_index(lst: List[T], predicate: Callable[[T], bool]) -> int:
    """Find the index of the first element matching a predicate. Returns -1 if not found."""
    for i, item in enumerate(lst):
        if predicate(item):
            return i
    return -1


def some(lst: List[T], predicate: Callable[[T], bool]) -> bool:
    """Check if any element matches a predicate."""
    for item in lst:
        if predicate(item):
            return True
    return False


def every(lst: List[T], predicate: Callable[[T], bool]) -> bool:
    """Check if all elements match a predicate."""
    for item in lst:
        if not predicate(item):
            return False
    return True


def includes(lst: List[T], item: T) -> bool:
    """Check if a list contains an item."""
    return item in lst


def sum_list(lst: List[Union[int, float]]) -> Union[int, float]:
    """Sum all elements in a list."""
    return sum(lst)


def product(lst: List[Union[int, float]]) -> Union[int, float]:
    """Return the product of all elements in a list."""
    if not lst:
        raise ValueError("List must not be empty")
    result: Union[int, float] = 1
    for item in lst:
        result *= item
    return result


def take_while(lst: List[T], predicate: Callable[[T], bool]) -> List[T]:
    """Take elements from the beginning while predicate is true."""
    result: List[T] = []
    for item in lst:
        if predicate(item):
            result.append(item)
        else:
            break
    return result


def drop_while(lst: List[T], predicate: Callable[[T], bool]) -> List[T]:
    """Drop elements from the beginning while predicate is true."""
    result: List[T] = []
    dropping = True
    for item in lst:
        if dropping and predicate(item):
            continue
        dropping = False
        result.append(item)
    return result


def average(lst: List[Union[int, float]]) -> float:
    """Calculate the average of a list."""
    if not lst:
        raise ValueError("List must not be empty")
    return sum(lst) / len(lst)


def max_list(lst: List[CT]) -> CT:
    """Return the maximum element in a list."""
    if not lst:
        raise ValueError("List must not be empty")
    return max(lst)


def min_list(lst: List[CT]) -> CT:
    """Return the minimum element in a list."""
    if not lst:
        raise ValueError("List must not be empty")
    return min(lst)


def reverse(lst: List[T]) -> List[T]:
    """Return a reversed copy of a list."""
    return list(reversed(lst))


def count(lst: List[T], item: T) -> int:
    """Count occurrences of an item in a list."""
    return lst.count(item)


def count_by(lst: List[T], predicate: Callable[[T], bool]) -> int:
    """Count elements matching a predicate."""
    count_result = 0
    for item in lst:
        if predicate(item):
            count_result += 1
    return count_result


def to_dict(pairs: List[List[Any]]) -> Dict[Any, Any]:
    """Convert a list of pairs to a dictionary."""
    result: Dict[Any, Any] = {}
    for pair in pairs:
        if len(pair) >= 2:
            result[pair[0]] = pair[1]
    return result


def from_pairs(pairs: List[tuple]) -> Dict[Any, Any]:
    """Convert a list of tuples to a dictionary."""
    return dict(pairs)


def keys(d: Dict[K, V]) -> List[K]:
    """Return all keys of a dictionary as a list."""
    return list(d.keys())


def values(d: Dict[K, V]) -> List[V]:
    """Return all values of a dictionary as a list."""
    return list(d.values())


def items(d: Dict[K, V]) -> List[tuple]:
    """Return all items of a dictionary as a list of tuples."""
    return list(d.items())
