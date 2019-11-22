
def test(arg1 = 1, arg2 = "hello"):
    print("arg1 %d, arg2 %s" % (arg1, arg2))

test()
test(arg2 = 2)
test(arg2 = "world", arg1 = 2)
