from dataclasses import dataclass
from cffi import FFI

class Mocker:
    @dataclass
    class Entry:
        name: str
        args: list
        ret: object

    @dataclass
    class Call:
        args: list
        ret: object

    def __init__(self):
        self.called = {}

    def capture_decorator(self, func, key):
        def decorate(*args, **kwargs):
            # print(f'capture_decorator key: {key}')

            ret = func(*args)

            self.called[key].append(Mocker.Call(args, ret))

            return ret
        return decorate

    def clear(self):
        self.called = {}

    def print_all(self):
        for b in self.called:
            print(b, self.called[b])

    def get_number_of_calls(self, key):
        # print(f'called: {self.called}')
        if isinstance(key, int):
            if key >= len(self.called):
                raise ValueError(f'invalid mock id {key}')
        else:
            key = key.__name__

            if not key in self.called:
                raise ValueError(f'invalid mock id {key}')

        return len(self.called[key])

def mock_binder(state, binding_point_name, target=None, rv=None):
    # print(f'mock_binder {binding_point_name} target {target}')

    if target is None:
        func = lambda *args: rv
        key = len(state.mocker.called)
    elif callable(target):
        func = target
        key = target.__name__

    def_extern_decorator = state.tube._ffi.def_extern(name=binding_point_name)
    def_extern_decorator(state.mocker.capture_decorator(func, key))

    binding = getattr(state.tube._lib, binding_point_name)

    state.mocker.called[key] = []

    return binding
