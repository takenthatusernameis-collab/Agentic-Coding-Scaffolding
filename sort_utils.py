"""Sorting utility functions."""


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
