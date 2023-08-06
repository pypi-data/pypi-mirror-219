from __future__ import annotations

import scope


def test_id():
    d = 1
    id = scope.id
    assert id.put(id.get(d))(d) == 1
    assert id.get(id.put(3)(d)) == 3
    assert id.put(3)(id.put(2)(d)) == 3

def test_item_lens_0():
    d = {'a': 1}
    lens = scope.ItemLens('a')
    assert lens.put(lens.get(d))(d) == {'a': 1}
    assert lens.get(lens.put(3)(d)) == 3
    assert lens.put(3)(lens.put(2)(d)) == {'a': 3}

def test_item_lens_1():
    d = {'a': 1}
    lens = scope.id['a']
    assert lens.put(lens.get(d))(d) == {'a': 1}
    assert lens.get(lens.put(3)(d)) == 3
    assert lens.put(3)(lens.put(2)(d)) == {'a': 3}

def test_function_lens_0():
    d = 0
    f = lambda x: x + 1
    f_inv = lambda x: x - 1
    lens = scope.id.call(f, f_inv)

    assert lens.put(lens.get(d))(d) == 0
    assert lens.get(lens.put(11)(d)) == 11
    assert lens.put(33)(lens.put(11)(d)) == 32

def test_item_function_lens():
    d = {'a': 0}
    f = lambda x: x + 1
    f_inv = lambda x: x - 1
    lens = scope.id['a'].call(f, f_inv)

    assert lens.put(lens.get(d))(d) == {'a': 0}
    assert lens.get(lens.put(11)(d)) == 11
    assert lens.put(33)(lens.put(11)(d)) == {'a': 32}