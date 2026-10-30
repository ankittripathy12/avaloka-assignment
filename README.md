# Avaloka Assignment

**Author:** Ankit Kumar Tripathy

Two problems, implemented in Python 3 with tests. The full write-up is in
[`Ankit_Tripathy_Avaloka_Assignment.pdf`](./Ankit_Tripathy_Avaloka_Assignment.pdf).

## Structure

```
.
├── lru_cache.py          # Node, LRUCache, ThreadSafeLRUCache
├── event_scheduler.py    # can_attend_all, min_rooms_required, room_name, assign_rooms
├── tests/
│   ├── test_lru_cache.py
│   └── test_scheduler.py
├── requirements.txt
└── Ankit_Tripathy_Avaloka_Assignment.pdf
```

## Run the tests

```bash
pip install -r requirements.txt
pytest -v
```

## Problem 1: LRU Cache

**Approach.** A hash map (key -> node) combined with a doubly linked list ordered by
recency. The node next to the head is the most recently used; the node next to the
tail is the least recently used. Sentinel head and tail nodes remove all
empty-list and end-of-list special cases.

- The map gives O(1) lookup of any node.
- The doubly linked list lets a node be unlinked using only its own `prev`/`next`,
  so moving it to the front or evicting the oldest is O(1).

**Thread safety.** `ThreadSafeLRUCache` holds a single mutex for the whole body of
`get` and `put`. Even `get` mutates the list, so a read-write lock would not help.
For higher throughput: lock striping (shard by `hash(key) % N`) or buffered recency
updates.

## Problem 2: Event Scheduler

Events are `(start, end)` tuples. Adjacent events (`end == start`) do **not** overlap.

- `can_attend_all`: sort by start; fail if any event starts strictly before the
  previous one ends (`start < prev_end`).
- `min_rooms_required`: sort by start and keep a min-heap of end times, one per room
  in use. If `heap[0] <= start`, reuse that room. The maximum heap size is the answer,
  which equals the maximum number of simultaneous events.
- `assign_rooms` (extension): two heaps, a busy heap of `(end_time, room_id)` and a free
  heap of room ids. Room names follow spreadsheet style (Room A ... Room Z, Room AA, ...),
  so there is no cap on room count.

## Complexity

Let `n` = number of events and `C` = cache capacity.

| Function | Time | Space |
|---|---|---|
| `LRUCache.get` | O(1) | O(1) extra |
| `LRUCache.put` | O(1) | O(1) extra |
| LRU cache overall | - | O(C) |
| `can_attend_all` | O(n log n) | O(n) for sorted copy |
| `min_rooms_required` | O(n log n) | O(n) |
| `assign_rooms` | O(n log n) | O(n) |

## Trade-offs

A hash map alone has no ordering, so finding the LRU item is O(n). A list or array
alone tracks order but finding a key is O(n). Combined, every operation is O(1). The
cost is extra memory (two pointers per node) and weaker cache locality. In production
Python, `collections.OrderedDict` gives the same behavior with less code; this
implementation shows the underlying mechanism.
