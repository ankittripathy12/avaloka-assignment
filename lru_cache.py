"""LRU Cache: hash map + doubly linked list, O(1) get and put."""
import threading


class Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self.capacity = capacity
        self.map = {}            # key -> Node
        self.head = Node()       # sentinel: most-recent side
        self.tail = Node()       # sentinel: least-recent side
        self.head.next = self.tail
        self.tail.prev = self.head

    # internal helpers, all O(1)
    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    # public API
    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._add_to_front(node)  # mark as recently used
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        node = self.map.get(key)
        if node is not None:      # update existing key
            node.value = value
            self._remove(node)
            self._add_to_front(node)
            return
        if len(self.map) >= self.capacity:  # evict LRU item
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
        new_node = Node(key, value)
        self.map[key] = new_node
        self._add_to_front(new_node)


class ThreadSafeLRUCache(LRUCache):
    """Same cache, with one mutex held for the whole body of get/put."""

    def __init__(self, capacity):
        super().__init__(capacity)
        self._lock = threading.Lock()

    def get(self, key):
        with self._lock:
            return super().get(key)

    def put(self, key, value):
        with self._lock:
            super().put(key, value)
