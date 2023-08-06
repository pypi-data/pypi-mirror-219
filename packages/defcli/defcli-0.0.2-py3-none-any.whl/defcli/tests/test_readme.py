from ..defcli import subcommand, run


@subcommand
def positional_integer(num: int):
    print(f"I like to add five: {num + 5}")
    return num + 5


def test_positional_int():
    assert run(["positional_integer", "7"]) == 12


@subcommand
def named_string(*, name):
    msg = f"Hello, {name}!"
    print(msg)
    return msg


def test_named_string():
    assert run(["named_string", "--name", "Fred"]) == "Hello, Fred!"


@subcommand
def named_bool(*, has_something: bool):
    if has_something:
        print("Got it!")
    else:
        print("We're empty-handed")
    
    return has_something


@subcommand
def other_named_bool(has_other_thing=False):
    if has_other_thing:
        print("We have it!")
    else:
        print("The other thing is missing...")
    
    return has_other_thing


@subcommand
def nb3(bool_3=True):
    return bool_3


def test_named_bool():
    assert run(["named_bool", "--has_something"])
    assert not run(["named_bool"])
    
    assert run(["other_named_bool", "--has_other_thing"])
    assert not run(["other_named_bool"])
    
    assert not run(["nb3", "--bool_3"])
    assert run(["nb3"])
