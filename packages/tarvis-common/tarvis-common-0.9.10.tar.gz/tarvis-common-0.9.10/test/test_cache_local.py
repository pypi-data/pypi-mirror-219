from objsize import get_deep_size
from tarvis.common import time
from tarvis.common.cache.local import LocalCache, LocalCacheEntry


def test_cache_local_entry_is_expired():
    _ENTRY_TIME = 1000
    _ENTRY_TTL = 10
    time.set_artificial_time(_ENTRY_TIME, allow_reset=True)
    entry = LocalCacheEntry("something", _ENTRY_TTL, 0)
    assert not entry.is_expired()
    time.set_artificial_time(_ENTRY_TIME + _ENTRY_TTL + 1, allow_reset=True)
    assert entry.is_expired()


def test_cache_local_default_ttl():
    _ENTRY_TIME = 1000
    _ENTRY_TTL = 10
    _TEST_ITEMS = 3
    _TEST_TRIES = 5
    cache = LocalCache(default_ttl=_ENTRY_TTL)
    time.set_artificial_time(_ENTRY_TIME, allow_reset=True)
    for i in range(_TEST_ITEMS):
        cache.set(str(i), i)
    for test_try in range(_TEST_TRIES):
        for i in range(_TEST_ITEMS):
            assert cache.get(str(i)) == i
    time.set_artificial_time(_ENTRY_TIME + _ENTRY_TTL + 1, allow_reset=True)
    for i in range(_TEST_ITEMS):
        assert cache.get(str(i)) is None


def test_cache_local_max_size_bytes():
    _MAX_SIZE = 16384
    _TEST_ITEMS = 1000
    cache = LocalCache(max_size_bytes=_MAX_SIZE)
    cache_entries_size = 0
    for i in range(_TEST_ITEMS):
        key = str(i)
        value = f"foobar{key}snafu"
        key_size = get_deep_size(key)
        value_size = get_deep_size(value)
        entry_size = key_size + value_size
        cache.set(key, value)
        cache_entries_size += entry_size
    assert cache._size < cache_entries_size
    assert cache._size < _MAX_SIZE
    assert len(cache._cache) < _TEST_ITEMS


def test_cache_local_max_items():
    _MAX_ITEMS = 100
    _TEST_ITEMS = 1000
    cache = LocalCache(max_items=_MAX_ITEMS)
    for i in range(_TEST_ITEMS):
        cache.set(i, i)
    assert len(cache._cache) == _MAX_ITEMS
    for i in range(_TEST_ITEMS - 1, _TEST_ITEMS - _MAX_ITEMS, -1):
        assert cache.get(i) == i


def test_cache_local_delete_purge():
    _TEST_ITEMS = 33
    _DELETE_ITEMS = 11
    cache = LocalCache()
    for i in range(_TEST_ITEMS):
        cache.set(i, i)
    for i in range(_DELETE_ITEMS):
        cache.delete(i)
    assert len(cache._cache) == (_TEST_ITEMS - _DELETE_ITEMS)
    cache.purge()
    assert len(cache._cache) == 0
    assert cache._size == 0
    assert cache._item_count == 0
    for i in range(_TEST_ITEMS):
        cache.set(i, i)
    for i in range(_TEST_ITEMS):
        assert cache.get(i) == i
