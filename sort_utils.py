"""Sorting utility functions."""

__all__ = [
    "bubble_sort",
    "insertion_sort",
    "is_sorted",
    "merge_sort",
    "nth_largest",
    "selection_sort",
    "top_n",
]


def is_sorted(items, *, key=None, reverse=False):
    """Return True if items is sorted according to key and direction."""
    iterator = iter(items)
    previous = next(iterator, None)
    if key is None:

        def key(x):
            return x

    for current in iterator:
        left = key(previous)
        right = key(current)
        if reverse:
            if left < right:
                return False
        else:
            if left > right:
                return False
        previous = current
    return True


def bubble_sort(items, *, key=None, reverse=False):
    """Return a new list sorted using bubble sort."""
    result = list(items)
    if key is None:

        def key(x):
            return x

    swapped = True
    while swapped:
        swapped = False
        for i in range(len(result) - 1):
            left = key(result[i])
            right = key(result[i + 1])
            cond = left > right if not reverse else left < right
            if cond:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
    return result


def insertion_sort(items, *, key=None, reverse=False):
    """Return a new list sorted using insertion sort.

    A stable, in-place-style insertion sort that returns a new list. Accepts
    an optional ``key`` and ``reverse`` argument like :func:`bubble_sort`.

    Examples:
        >>> insertion_sort([3, 1, 2])
        [1, 2, 3]
        >>> insertion_sort([3, 1, 2], reverse=True)
        [3, 2, 1]
        >>> insertion_sort([1, 2, 3])
        [1, 2, 3]
        >>> insertion_sort([])
        []
        >>> insertion_sort([5])
        [5]
        >>> insertion_sort([3, 1, 2], key=lambda x: -x)
        [3, 2, 1]
        >>> insertion_sort(["banana", "apple", "cherry"])
        ['apple', 'banana', 'cherry']
    """
    if key is None:

        def key(x):
            return x

    result = list(items)
    for i in range(1, len(result)):
        current = result[i]
        current_key = key(current)
        j = i - 1
        while j >= 0:
            left_key = key(result[j])
            cond = left_key > current_key if not reverse else left_key < current_key
            if not cond:
                break
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result


def selection_sort(items, *, key=None, reverse=False):
    """Return a new list sorted using selection sort.

    A selection sort that returns a new list. It repeatedly selects the
    minimum (or maximum, when *reverse* is True) element from the unsorted
    remainder and appends it to the result. Accepts an optional ``key`` and
    ``reverse`` argument like :func:`bubble_sort` and :func:`insertion_sort`.

    Args:
        items: An iterable of comparable elements.
        key: A function that extracts a comparison key from each element.
            Defaults to the identity function.
        reverse: If True, sort in descending order. Defaults to False.

    Returns:
        A new list containing the elements of *items* sorted according to
        *key* and *reverse*.

    Examples:
        >>> selection_sort([3, 1, 2])
        [1, 2, 3]
        >>> selection_sort([3, 1, 2], reverse=True)
        [3, 2, 1]
        >>> selection_sort([1, 2, 3])
        [1, 2, 3]
        >>> selection_sort([])
        []
        >>> selection_sort([5])
        [5]
        >>> selection_sort([3, 1, 2], key=lambda x: -x)
        [3, 2, 1]
        >>> selection_sort(["banana", "apple", "cherry"])
        ['apple', 'banana', 'cherry']
    """
    if key is None:

        def key(x):
            return x

    result = []
    pool = list(items)
    while pool:
        best_index = 0
        best_key = key(pool[0])
        for i in range(1, len(pool)):
            current_key = key(pool[i])
            if reverse:
                if current_key > best_key:
                    best_key = current_key
                    best_index = i
            else:
                if current_key < best_key:
                    best_key = current_key
                    best_index = i
        result.append(pool.pop(best_index))
    return result


def merge_sort(items, *, key=None, reverse=False):
    """Return a new list sorted using merge sort."""
    if key is None:

        def key(x):
            return x

    result = list(items)
    if len(result) <= 1:
        return result

    def merge(left, right):
        out = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparison = key(left[i]) <= key(right[j])
            if reverse:
                if key(left[i]) >= key(right[j]):
                    out.append(left[i])
                    i += 1
                else:
                    out.append(right[j])
                    j += 1
            else:
                if comparison:
                    out.append(left[i])
                    i += 1
                else:
                    out.append(right[j])
                    j += 1
        out.extend(left[i:])
        out.extend(right[j:])
        return out

    mid = len(result) // 2
    left = merge_sort(result[:mid], key=key, reverse=reverse)
    right = merge_sort(result[mid:], key=key, reverse=reverse)
    return merge(left, right)


def nth_largest(items, n, *, key=None):
    """Return the n-th largest element (1-based)."""
    if n < 1:
        raise ValueError("n must be at least 1")
    sorted_items = merge_sort(items, key=key, reverse=True)
    if n > len(sorted_items):
        raise ValueError("n exceeds number of items")
    return sorted_items[n - 1]


def top_n(items, n, *, key=None, reverse=True):
    """Return the top n items sorted by key."""
    return merge_sort(items, key=key, reverse=reverse)[:n]
