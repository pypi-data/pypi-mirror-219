from ..defcli import run, subcommand


@subcommand
def sub1():
    '''
    A simple test subcommand
    '''
    print("sub1()")
    return "sub1"


@subcommand
def pos_args(arg1: int):
    '''
    Give me an argument
    '''
    print(f"pos_args({arg1})")
    return arg1


@subcommand
def pos_args_default(arg1=84):
    '''
    Give something other than 84
    '''
    print(f"pos_args_default({arg1})")
    return arg1


@subcommand
def kw_args(*, arg1=True):
    '''
    A keyword arg
    '''
    print(f"kw_args({arg1})")
    return arg1


@subcommand
def var_args(*args):
    '''
    Give me many arguments
    '''
    print(f"var_args({args})")
    return args


@subcommand
def var_kw_args(*varargs, kwarg1=True):
    '''
    
    '''
    print(f"var_kw_args({varargs}, {kwarg1})")
    return kwarg1


def test_misc():
    assert run(["sub1"]) == "sub1"
    assert run(["pos_args", "467"]) == 467
    assert run(["pos_args_default"]) == 84
    assert run(["pos_args_default", "83"]) == 83
    assert run(["kw_args"]) is True
    assert run(["kw_args", "--arg1"]) is False
    assert run(["var_args"]) == ()
    assert run(["var_args", "Hello,", "world!"]) == ("Hello,", "world!")
    assert run(["var_kw_args"]) is True
    assert run(["var_kw_args", "Hello,", "world!"]) is True
    assert run(["var_kw_args", "hi", "--kwarg1"]) is False
