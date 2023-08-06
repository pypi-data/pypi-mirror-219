__version__ = "0.1.1"
from contextlib import suppress as _suppress


class Lens:
    def __init__(self, get, put):
        self.get = get
        self.put = put

    def call(self, f, f_inv=None):
        with _suppress(Exception):
            f_inv = f_inv or ~f

        getter = lambda data: f(self.get(data))
        setter = lambda value: self.put(f_inv(value))
        if not f_inv:
            return getter

        return Lens(getter, setter)

    def pcall(self, f, f_inv=None):
        with _suppress(Exception):
            f_inv = f_inv or ~f

        return lambda data: self.put(f(self.get(data)))(data)

    def __call__(self, data):
        return self.get(data)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return Traversal(self)
        else:
            return compose_lenses(self, ItemLens(item))

    def __rmul__(self, other):
        return compose_lenses(other, self)

    def __mul__(self, other):
        if isinstance(other, Traversal):
            return other.__rmul__(self)
        return compose_lenses(self, other)

    def __add__(self, other):
        return ParallelLens(self, other)

    def __or__(self, other):
        return ParallelLens(self, other)

    def __lshift__(self, other):
        return ParallelLens(self, other)

id = Lens(lambda data: data, lambda value: lambda data: value)


def compose_lenses(pre, post):
    if isinstance(pre, CRUDLens) and isinstance(post, CRUDLens):
        return CRUDLens(lambda data: post.get(pre.get(data)),
                    lambda value: lambda data: pre.put(post.put(value)(pre.get(data)))(data),
                    lambda value: lambda data: pre.create(post.create(value)(pre.get(data)))(data),
                    lambda data: pre.put(post.delete(pre.get(data)))(data))
    return Lens(lambda data: post.get(pre.get(data)),
                lambda value: lambda data: pre.put(post.put(value)(pre.get(data)))(data))


class ParallelLens(Lens):
    def __init__(self, *lenses):
        self.lenses = list(lenses)
        getter = lambda data: tuple(lens.get(data) for lens in self.lenses)
        setter = lambda value: lambda data: tuple(lens.put(value)(data) for lens in self.lenses)
        super().__init__(getter, setter)

    def __or__(self, other):
        self.lenses.append(other)
        return self

    def __lshift__(self, other):
        if isinstance(other, ParallelLens):
            self.lenses.extend(other.lenses)
            return self
        self.lenses.append(other)
        return self


class Traversal(Lens):
    def __init__(self, pre, post=None, flatten=False):
        if flatten:
            def setter(values):
                def inner(data):
                    it = iter(values)
                    return pre.put([[next(it) for x in el] for el in pre.get(data)])(data)
                return inner
            getter = lambda data: [x for el in pre.get(data) for x in el]
            super().__init__(getter, setter)
            return
        elif not post:
            super().__init__(pre.get, pre.put)
            return
        else:
            def setter(values):
                def inner(data):
                    it = iter(values)
                    return pre.put([post.put(next(it))(el) for el in pre.get(data)])(data)
                return inner
            getter = lambda data: [post.get(el) for el in pre.get(data)]
            super().__init__(getter, setter)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return Traversal(self, flatten=True)
        else:
            return Traversal(self, ItemLens(item))

    def call(self, f, f_inv=None):
        with _suppress(Exception):
            f_inv = f_inv or ~f

        return lambda data: [f(d) for d in self.get(data)]

    def pcall(self, f, f_inv=None):
        with _suppress(Exception):
            f_inv = f_inv or ~f

        return lambda data: self.put([f(d) for d in self.get(data)])(data)

    def __rmul__(self, other):
        return Traversal(compose_lenses(other, self))

    def __mul__(self, other):
        return Traversal(compose_lenses(self, other))


class ItemLens(Lens):
    def __init__(self, item):
        super().__init__(self.getter(item), self.setter(item))

    @staticmethod
    def getter(item):
        return lambda data: data.get(item)

    @staticmethod
    def setter(item):
        return lambda value: lambda data: {**data, item: value}


class CRUDLens(Lens):
    def __init__(self, get, put, create, delete):
        self.get = get
        self.put = put
        self.create = create
        self.delete = delete

    def call(self, f, f_inv=None):
        with _suppress(Exception):
            f_inv = f_inv or ~f

        getter = lambda data: f(self.get(data))
        setter = lambda value: self.put(f_inv(value))
        creator = lambda value: self.create(f_inv(value))
        # c(g(data))(d(data)) = data
        deleter = self.delete
        if not f_inv:
            return getter

        return CRUDLens(getter, setter, creator, deleter)

    def ccall(self, f):
        return lambda data: self.create(f(self.get(data)))(data)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return CRUDTraversal(self)
        else:
            return compose_lenses(self, ItemCRUDLens(item))

    def __mul__(self, other):
        if isinstance(other, Traversal) or isinstance(other, CRUDTraversal):
            return other.__rmul__(self)
        return compose_lenses(self, other)

    def __add__(self, other):
        if isinstance(other, CRUDLens):
            return ParallelCRUDLens(self, other)
        return ParallelLens(self, other)

    def __or__(self, other):
        if isinstance(other, CRUDLens):
            return ParallelCRUDLens(self, other)
        return ParallelLens(self, other)

    def __lshift__(self, other):
        if isinstance(other, CRUDLens):
            return ParallelCRUDLens(self, other)
        return ParallelLens(self, other)


class ItemCRUDLens(CRUDLens):
    def __init__(self, key):
        self.key = key
        super().__init__(self.getter(key), self.setter(key), self.creator(key), self.deleter(key))

    @staticmethod
    def getter(key):
        return lambda data: data.get(key)

    @staticmethod
    def setter(key):
        return lambda value: lambda data: key in data and {**data, key: value} or data

    @staticmethod
    def creator(key):
        return lambda value: lambda data: {**data, key: value} if data else {key: value}

    @staticmethod
    def deleter(key):
        return lambda data: {k: v for k, v in data.items() if k != key}


class ParallelCRUDLens(CRUDLens):
    def __init__(self, *crud_lenses):
        self.crud_lenses = list(crud_lenses)
        getter = lambda data: tuple(lens.get(data) for lens in self.crud_lenses)
        setter = lambda value: lambda data: tuple(lens.put(value)(data) for lens in self.crud_lenses)
        creator = lambda value: lambda data: tuple(lens.create(value)(data) for lens in self.crud_lenses)
        deleter = lambda data: tuple(lens.delete(data) for lens in self.crud_lenses)

        super().__init__(getter, setter, creator, deleter)

    def __or__(self, other):
        self.crud_lenses.append(other)
        if isinstance(other, CRUDLens):
            return self
        return ParallelLens(*self.crud_lenses)

    def __lshift__(self, other):
        if isinstance(other, ParallelCRUDLens):
            self.crud_lenses.extend(other.lenses)
            return self
        if isinstance(other, ParallelLens):
            self.crud_lenses.extend(other.lenses)
            return ParallelLens(*self.crud_lenses)
        return self.__or__(other)


class CRUDTraversal(CRUDLens):
    def __init__(self, pre, post=None, flatten=False):
        if flatten:
            def setter(values):
                def inner(data):
                    it = iter(values)
                    return pre.put([[next(it) for x in el] for el in pre.get(data)])(data)
                return inner
            def creator(values):
                def inner(data):
                    it = iter(values)
                    return pre.create([[next(it) for x in el] for el in pre.get(data)])(data)
                return inner
            getter = lambda data: [x for el in pre.get(data) for x in el]
            deleter = lambda data: [x for el in pre.get(data) for x in post.delete(el)]
            super().__init__(getter, setter, creator, deleter)
            return
        elif not post:
            super().__init__(pre.get, pre.put, pre.create, pre.delete)
            return
        else:
            def setter(values):
                def inner(data):
                    it = iter(values)
                    return pre.put([post.put(next(it))(el) for el in pre.get(data)])(data)
                return inner
            def creator(values):
                def inner(data):
                    it = iter(values)
                    return pre.create([post.create(next(it))(el) for el in pre.get(data)])(data)
                return inner
            getter = lambda data: [post.get(el) for el in pre.get(data)]
            deleter = lambda data: pre.put([post.delete(el) for el in pre.get(data)])(data)
            super().__init__(getter, setter, creator, deleter)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return CRUDTraversal(self, flatten=True)
        else:
            return CRUDTraversal(self, ItemCRUDLens(item))

    def call(self, f, f_inv=None):
        with _suppress(Exception):
            f_inv = f_inv or ~f

        return lambda data: [f(d) for d in self.get(data)]

    def pcall(self, f, f_inv=None):
        return lambda data: self.put([f(d) for d in self.get(data)])(data)

    def ccall(self, f, f_inv=None):
        return lambda data: self.create([f(d) for d in self.get(data)])(data)

    def __rmul__(self, other):
        if isinstance(other, CRUDLens):
            return CRUDTraversal(compose_lenses(other, self))
        return Traversal(compose_lenses(other, self))

    def __mul__(self, other):
        if isinstance(other, CRUDLens):
            return CRUDTraversal(compose_lenses(self, other))
        return Traversal(compose_lenses(self, other))