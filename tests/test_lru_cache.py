import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from lru_cache import LRUCache, ThreadSafeLRUCache


def test_basic_get_put():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1


def test_eviction_of_least_recently_used():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.get(1)          # 2 is now least recently used
    c.put(3, 3)       # evicts 2
    assert c.get(2) == -1
    assert c.get(1) == 1
    assert c.get(3) == 3


def test_update_existing_key_refreshes_recency():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)      # update, 2 becomes LRU
    c.put(3, 3)       # evicts 2
    assert c.get(1) == 10
    assert c.get(2) == -1


def test_missing_key():
    assert LRUCache(1).get(42) == -1


def test_zero_capacity_stores_nothing():
    c = LRUCache(0)
    c.put(1, 100)
    assert c.get(1) == -1


def test_capacity_one():
    c = LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1
    assert c.get(2) == 2


def test_negative_capacity_raises():
    try:
        LRUCache(-1)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_thread_safe_cache_never_exceeds_capacity():
    c = ThreadSafeLRUCache(50)

    def worker(offset):
        for i in range(2000):
            c.put(offset * 10000 + i, i)
            c.get(offset * 10000 + i // 2)

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(c.map) <= 50
