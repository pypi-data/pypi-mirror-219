# Scope

Scope is a Python library inspired by _optics_ from functional programming. The aim of Scope is to make various flavors of _optics_ natural tools for Python programmers without requiring knowledge of the underlying math. Put simply, _optics_ provide an abstraction for focusing on ("getting") and manipulating ("setting") data within larger and potentially nested structures.

This library favors usability over rigor and makes some decisions which increase utility at the expense of overloading and extending established terminology. For example, _traversals_ in the standard usage, provide a means of focusing on multiple parts of a datastructure but do not provide similar setting behavior, whereas instances of the `scope.Traversal` class do provide a way to set multiple parts of a larger datastructure.

## Install

Install by running `pip install scope-py` or by cloning this repo and running `pip install .` in the project root directory.

## Introduction

The Scope library targets manipulation of JSON-like nested structures, which in Python are built from dictionaries, and lists, but custom _optics_ are definable. Scope has a few classes you should be aware of;

- `Lens`: Base class providing get and put methods. Can be composed with other lenses.
- `ParallelLens`: Allows multiple lenses to be used in parallel.
- `Traversal`: Provides functionality for working with sequences of data.
- `ItemLens`: A lens focused on a specific item in an object which implements the `__getitem__` dunder method.
- `CRUDLens`: An extension of a Lens that includes create and delete methods.
- `ParallelCRUDLens`: Allows multiple CRUD lenses to be used in parallel.
- `CRUDTraversal`: Extension of the CRUDLens for working with sequences of data.

Importantly, a `Lens` focuses on one thing and a `Traversals` focuses on many things. A `CRUDLens` extends the get/put functionality of lenses with additional create/delete functionality.

## Usage

### Basic lens composition:

```python
import scope

# create a lens that focuses on item 'b' after item 'a'
lens = scope.id['a']['b']
# lens = scope.compose_lenses(scope.id['a'], scope.id['b']) <-- alt. syntax

data = {'a': {'b': 3}}

# note -- lens(data) is an alias for lens.get(data)
assert lens(data) == 3
assert lens.put(4)(data) == {'a': {'b': 4}}
```

### CRUDTraversal usage:

```python
lens = CRUDTraversal(ItemCRUDLens('a'), ItemCRUDLens('c'))
# lens = ItemCRUDLens('a')[::]['c'] <-- alt. syntax

data = {'a': [{'b': 1}, {'b': 3}]}

# "{'a': [{'b': 1, 'c': 2}, {'b': 3, 'c': 4}]}"
print(lens.create([2, 4])(data))
```

### Create a custom attribute lens:

```python
# create a lens that gets/sets the attribute "my_attr" on an object
my_attr_lens = scope.Lens(lambda data: getattr(data, 'my_attr'),
                          lambda value: lambda data: setattr(data, 'my_attr', value))
```

### Parallel lens usage:

```python
x_lens, y_lens = scope.id['x'], scope.id['y']

# create a lens which focuses on 'x' and 'y' in parallel
parallel_lens = x_lens | y_lens
# parallel_lens = scope.ParallelLens(x_lens, y_lens) <-- alt. syntax

data = {'x': 2, 'y': 3}

assert sum(parallel_lens(data)) == 5
```

## Todo‘s

- [] Clean up unused files leftover from cloned template repo
- [] Tests to achieve 100% code coverage
- [] Add a `filter` method to all classes which accepts a predicate function and applies it to the focus
- [] Add tests passing and code coverage badges using Github Pages

## License

This project is open-sourced under the MIT license. See [LICENSE](https://github.com/fchughes/scope/blob/main/LICENSE) for more information.

## Contact

For questions or issues, please open an issue on GitHub.
