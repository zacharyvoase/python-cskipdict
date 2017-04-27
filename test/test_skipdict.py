from nose.tools import assert_raises

from cskipdict import SkipDict


def check_dict(skip_dict, expected):
    assert len(skip_dict) == len(expected)
    assert len(skip_dict._SkipDict__pointers) == len(set(expected.values()))
    for k in expected:
        assert k in skip_dict
        assert skip_dict[k] == expected[k]
        assert skip_dict.get(k) == expected[k]
        assert skip_dict.get(k + 1000) is None
        assert skip_dict.get(k + 1000, None) is None
        assert skip_dict.get(k + 1000, 'Hello') == 'Hello'
    # Ensure iteration order is always increasing
    last_k = None
    for k in skip_dict:
        assert k in expected
        if last_k is not None:
            assert k > last_k
            last_k = k

    if expected:
        min_key = min(expected.keys())
        assert skip_dict.minimum() == (min_key, expected[min_key])

        max_key = max(expected.keys())
        assert skip_dict.maximum() == (max_key, expected[max_key])
    else:
        assert skip_dict.minimum() is None
        assert skip_dict.maximum() is None


def test_smoke():
    sd = SkipDict()
    check_dict(sd, {})
    sd[123] = 'foo'
    check_dict(sd, {123: 'foo'})
    sd[456] = 'bar'
    check_dict(sd, {123: 'foo', 456: 'bar'})
    sd[123] = 'baz'
    check_dict(sd, {123: 'baz', 456: 'bar'})
    assert sd.pop(456) == 'bar'
    check_dict(sd, {123: 'baz'})
    with assert_raises(KeyError):
        sd.pop(456)
    assert sd.pop(456, None) is None
    assert sd.pop(456, 'Hello') == 'Hello'
