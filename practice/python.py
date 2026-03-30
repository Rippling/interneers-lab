mylist = ["List item 1", 2, 3.14]
print(mylist[0:])

byte_data = b"\x31"
print(byte_data.decode("utf-8"))

s = "A🐍"
print(len(s))

st = """hello"""
print(st)

print(
    "Name: %s\
Number: %s\
String: %s"
    % ("Aadi", 3, 3 * "-")
)

print("This %(verb)s a %(noun)s." % {"noun": "test", "verb": "is"})


def some_function():
    try:
        # Division by zero raises an exception
        10 / 0
    except ZeroDivisionError:
        print("Oops, invalid.")
    else:
        # Exception didn't occur, we're good.
        print("All good")
        pass
    finally:
        # This is executed after the code block is run
        # and all exceptions have been handled, even
        # if a new exception is raised while handling.
        print("We're done with that.")
    print("hello")


some_function()
