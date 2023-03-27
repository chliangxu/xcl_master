
# 封包：1,2   --> (1,2)
#      c=100 --> {'c':100}
def foo(*args, **kwargs):

    print(args)
    print(kwargs)

    # foo2((1, 2), {'c': 100})
    # foo2(args, kwargs)

    # foo2(1, 2, c=100)
    # 解包：*args, **kwargs
    foo2(*args, **kwargs)


def foo2(*args, **kwargs):
    print(args)
    print(kwargs)


if __name__ == '__main__':
    foo(1, 2, c=100)


