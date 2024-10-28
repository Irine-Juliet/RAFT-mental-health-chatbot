from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()
import sys
import inspect
from functools import wraps

from mdc.context import new_log_context


def has_argument(func, arg):

    """
    Backwards-compatible method to check if a function has an actual argument (not an *args or **kwargs)
    of the name :param arg:
    """

    try:
        return arg in inspect.signature(func).parameters
    except AttributeError:
        pass

    try:
        spec = inspect.getfullargspec(func)
        return arg in (spec.args + spec.kwonlyargs)
    except AttributeError:
        pass

    return arg in inspect.getargspec(func).args


def bind_argument(func, arg, args, kwargs):

    """
    Backwards-compatible method to get the value of argument :param arg:
    when function :param func: is called as func(*args, **kwargs)
    """

    if not has_argument(func, arg):
        raise ValueError("Function {} has no argument named {}".format(func, arg))

    try:
        signature = inspect.signature(func)
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        return bound.arguments[arg]
    except AttributeError:
        pass

    bound = inspect.getcallargs(func, *args, **kwargs)
    return bound[arg]


def wrap_function_or_generator(func, pass_context_as=None, context_dict=None):

    if pass_context_as is not None:
        if not has_argument(func, pass_context_as):
            raise ValueError(
                "Function {} needs to have a {} argument to be able to recieve the context".format(
                    func, pass_context_as
                )
            )

    if context_dict is None:
        context_dict = {}

    if inspect.isgeneratorfunction(func):

        if pass_context_as is not None:
            raise NotImplementedError(
                "Passing the context object to a generator is not supported"
            )

        @wraps(func)
        def wrapper(*args, **kwargs):

            to_send = None
            generator = func(*args, **kwargs)

            while True:
                try:
                    with new_log_context(**context_dict) as context:
                        to_yield = generator.send(to_send)
                except StopIteration:
                    return
                else:
                    to_send = yield to_yield

    else:

        @wraps(func)
        def wrapper(*args, **kwargs):
            with new_log_context(**context_dict) as context:
                if pass_context_as is None:
                    return func(*args, **kwargs)
                else:
                    new_kwargs = {pass_context_as: context}
                    new_kwargs.update(**kwargs)
                    return func(*args, **new_kwargs)

    return wrapper


def log_value(**mdc_kwargs):

    """Adds constant values to the logging context"""

    def decorator(func):
        return wrap_function_or_generator(func, context_dict=mdc_kwargs)

    return decorator


def log_value_and_pass_context(**mdc_kwargs):

    """Adds constant values to the logging context and
    passes it as an argument to the function under the name 'ctx'"""

    def decorator(func):
        return wrap_function_or_generator(
            func, pass_context_as="ctx", context_dict=mdc_kwargs
        )

    return decorator


with_mdc = log_value_and_pass_context


def pass_context(name):

    """Passes a new context as an argument to the function with the name given"""

    def decorator(func):
        return wrap_function_or_generator(func, pass_context_as=name)

    return decorator


def log_argument(argument, destination="", formatter=None):

    """Adds the argument value passed to the decorated function to the logging context,
    formatted by formatter and under the name given by destination"""

    destination = destination or argument

    if formatter is None:

        def formatter(x):
            return x

    def decorator(func):

        # Raise early if the function does not have said argument
        if not has_argument(func, argument):
            raise ValueError("Function {} has no argument {}".format(func, argument))

        @wraps(func)
        def wrapper(*args, **kwargs):

            raw_argument = bind_argument(func, argument, args, kwargs)

            return wrap_function_or_generator(
                func, context_dict={destination: formatter(raw_argument)}
            )(*args, **kwargs)

        return wrapper

    return decorator
