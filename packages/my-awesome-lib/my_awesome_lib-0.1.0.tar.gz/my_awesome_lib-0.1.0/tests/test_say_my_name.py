from my_awesome_lib.say_my_name import say_my_name


def test_say_my_name():
    name = "John"
    assert say_my_name(name) == "Your name is: John"
