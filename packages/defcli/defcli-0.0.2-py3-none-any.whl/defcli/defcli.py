"""
defcli is a quick and dirty tool for building CLI interfaces using python
functions (with a decorator) instead of using argparse directly.

Simply define a function, with or without parameters, and decorate it with
@subcommand. Each function creates a new argparse subcommand; the function's
parameters define the subcommand's options.

Call `defcli.run()` to parse sys.argv and call the appropriate function.
"""

import argparse
import inspect
from inspect import Parameter


_PARSER = argparse.ArgumentParser()
_SUBPARSERS = _PARSER.add_subparsers(
    required=True,
    dest="subcommand",
)

_SUBCMDS = {}


def subcommand(cmd_func):
    sig = inspect.signature(cmd_func)
    parser = _SUBPARSERS.add_parser(cmd_func.__name__, help=cmd_func.__doc__)
    
    if __name__ == "__main__":
        print(cmd_func.__name__, sig)
    
    vararg = None
    
    for _, param in sig.parameters.items():
        
        if param.default is not Parameter.empty:
            default = param.default
        else:
            default = None
        
        if param.annotation is not Parameter.empty:
            typ = param.annotation
        elif default is not None:
            typ = type(default)
        else:
            typ = None
        
        if param.kind is Parameter.VAR_POSITIONAL or param.kind is Parameter.VAR_KEYWORD:
            vararg = param.name
            nargs = "*"
        elif default is not None:
            nargs = "?"
        else:
            nargs = None
        
        # Only used for boolean or keyword-only arguments
        argname = f"--{param.name}"
        
        if typ is bool:
            if default is None or default is False:
                action = "store_true"
            elif default is True:
                action = "store_false"
            else:
                action = "store"  # Hopefully unreachable...
            
            parser.add_argument(
                argname,
                default=default,
                action=action,
            )
        elif param.kind is Parameter.KEYWORD_ONLY:
            parser.add_argument(
                argname,
                default=default,
                required=default is None,
                type=typ,
                action="store",
            )
            # TODO: Keyword varargs?
        else:
            parser.add_argument(
                param.name,
                default=default,
                nargs=nargs,
                type=typ,
            )
    
    _SUBCMDS[cmd_func.__name__] = (cmd_func, vararg)
    
    return cmd_func


def run(args=None):
    args = _PARSER.parse_args(args).__dict__
    (func, vararg) = _SUBCMDS[args["subcommand"]]
    
    del args["subcommand"]  # Don't pass the name of the function
    if __name__ == "__main__":
        print(f"{func.__name__} with {args}")
    
    if vararg is not None:
        varargs = args[vararg]
        del args[vararg]
        
        return func(*varargs, **args)
    else:
        return func(**args)
