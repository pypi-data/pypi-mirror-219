# dropstackframe
A python library for dropping stack frames.

This can be useful for removing decorators from stack traces, when using a framework with a lot of
decorators.

## Example

Let's us write a small decorator for measuring the time it takes to call a function:

```python
from time import perf_counter


def measure_time(func):
    def wrapper(*args, **kwargs):
        before = perf_counter()
        result = func(*args, **kwargs)
        after = perf_counter()
        print(f"{func.__name__} took {after - before}s.")
        return result

    return wrapper
```

We can use it like this:

```python
@measure_time
def foo(should_raise):
    assert not should_raise
    return 42


@measure_time
def bar(should_raise):
    return foo(should_raise)


@measure_time
def baz(should_raise):
    return bar(should_raise)


baz(False)
```

On my computer this prints:

```
foo took 2.2800122678745538e-07s.
bar took 3.576500057533849e-05s.
baz took 4.227000135870185e-05s.
```

Great. But what happens if we raise an error?

```python
baz(True)
```

yields:

```
Traceback (most recent call last):
  File "example.py", line 32, in <module>
    baz(True)
  File "example.py", line 7, in wrapper
    result = func(*args, **kwargs)
  File "example.py", line 28, in baz
    return bar(should_raise)
  File "example.py", line 7, in wrapper
    result = func(*args, **kwargs)
  File "example.py", line 23, in bar
    return foo(should_raise)
  File "example.py", line 7, in wrapper
    result = func(*args, **kwargs)
  File "example.py", line 17, in foo
    assert not should_raise
AssertionError
```

Notice how every other line is the `wrapper` from our decorator? If we have large codebase and it is
using a framework with a lot of decorators, this can make the stack traces hard to read, because
most of the frames are irrelevant decorators.

We can use the `dropstackframe` library to rewrite our decorator:

```python
from time import perf_counter
from dropstackframe import drop_stack_frame


def measure_time(func):
    def wrapper(*args, **kwargs):
        before = perf_counter()
        try:
            result = func(*args, **kwargs)
        except Exception:
            drop_stack_frame()
            raise
        after = perf_counter()
        print(f"{func.__name__} took {after - before}s.")
        return result

    return wrapper
```

Now, if we get an error:

```python
baz(True)
```

we get:

```
Traceback (most recent call last):
  File "example2.py", line 37, in <module>
    baz(True)
  File "example2.py", line 33, in baz
    return bar(should_raise)
  File "example2.py", line 28, in bar
    return foo(should_raise)
  File "example2.py", line 22, in foo
    assert not should_raise
AssertionError
```

and all the annoying `wrapper` stack frames have been removed.

## Disabling `dropstackframe`

Let's say you have a large codebase that uses `dropstackframe` and one day you have a bug that is
really hard to find. In fact you start suspecting that the bug might be hidden by
`drop_stack_frame`. You can use `set_enable_drop_stack_frame` to disable `drop_stack_frame`:

```python
from dropstackframe import set_enable_drop_stack_frame

set_enable_drop_stack_frame(False)
baz(True)
```

`set_enable_drop_stack_frame` can also be used as a context manager, if you only want to disable
`drop_stack_frame` in a limited region of your code:

```python
from dropstackframe import set_enable_drop_stack_frame

with set_enable_drop_stack_frame(False):
    baz(True)
```