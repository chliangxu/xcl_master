# 装饰器装饰的过程：离待装饰函数近的装饰器先装饰，然后再装饰离函数远的装饰器

def make_div(fn):   # fn=p_inner=0x22

    print("make_div 装饰器被调用装饰了")

    def div_inner():    # 0x33
        print("div_inner 内层函数被调用了")
        return "<div>" + fn() + "</div>"    # fn() --> 0x22() --> p_inner()

    return div_inner


def make_p(fn): # fn=0x11

    print("make_p 装饰器被调用装饰了")

    def p_inner():  # 0x22
        print("p_inner 内层函数被调用了")
        return "<p>" + fn() + "</p>"        # fn() --> 0x11() --> foo()

    return p_inner


@make_div   # foo=make_div(foo)  --> foo = div_inner = 0x33
@make_p     # foo=make_p(foo)   --> foo = p_inner = 0x22
def foo():  # 0x11
    print("源函数被调用")
    return "人生苦短"

if __name__ == '__main__':
    print()
    print()

    result = foo()      # 0x33()

    print(result)
    # pass