small gist, to return a default value if the parameter is None

for mypy type annotation, the parameter usually has the type **Optional[T]**, the returned type will have the type **T**

really not worth a package, just dont know where else to put it.


.. code-block:: python

    # definition
    from typing import TypeVar, Optional

    T = TypeVar('T')

    def get_default_if_none(parameter: Optional[T], default: T) -> T:
        if parameter is None:
            return default
        else:
            return parameter


.. code-block:: python

    # usage
    from typing import Optional
    import lib_parameter

    x: Optional[int] = None

    x = lib_parameter.get_default_if_none(x, default=1)
    # now x is from type int, not Optional[int]
