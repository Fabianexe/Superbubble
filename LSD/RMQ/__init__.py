"""
Thise source code is from
https://codereview.stackexchange.com/questions/154047/dynamic-programming-based-range-minimum-query
And stands so under Creative Commons Licensing
"""

from itertools import product


class RangeQuery(object):
    """Data structure providing efficient range queries."""

    def __init__(self, items, fn):
        """Build a RangeQuery object for a sequence of items.

        fn -- function taking two items and returning their query
        result, for example "min" to query the range-minimum. It must be
        associative, commutative, and idempotent.

        """
        # Mapping from (start, step) to reduce(fn, items[start:start + 2**step])
        self._rq = rq = {(i, 0): item for i, item in enumerate(items)}
        self._fn = fn
        n = len(items)
        for step, i in product(range(1, n.bit_length()), range(n)):
            j = i + 2 ** (step-1)
            if j < n:
                rq[i, step] = fn(rq[i, step-1], rq[j, step-1])
            else:
                rq[i, step] = rq[i, step-1]

    def query(self, start, stop):
        """Return reduce(fn, items[start:stop])."""
        j = (stop - start).bit_length() - 1
        x = self._rq[start, j]
        y = self._rq[stop - 2 ** j, j]
        return self._fn(x, y)
