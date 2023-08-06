import os
import sys
import logging


class Logger:

    envDebug = bool(os.environ.get("MASTER_DEBUG"))
    # print(f"--> envDebug: {envDebug}")

    @classmethod
    def trace(cls, *dargs, **dkwargs):
        cls.debug(f"Decor args: {dargs}")
        cls.debug(f"Decor kwargs: {dkwargs}")
        def inner(func):
            cls.debug(f"Running func: {func}")
            def wrap(*args,**kwargs):
                cls.debug(f"Function args: {args}")
                cls.debug(f"Function kwargs: {kwargs}")
                result = func(*args, **kwargs)
                cls.debug(f"Function result: {result}")

                return result
            return wrap
        return inner


    @classmethod
    def debug(cls, text: str):
        if not cls.envDebug: return
        print(f"\033[38;5;242m==> {text}\033[0m", file=sys.stderr)


    @classmethod
    def warn(cls, text: str):
        print(f"\033[33;1m==> {text}\033[0m", file=sys.stderr)
