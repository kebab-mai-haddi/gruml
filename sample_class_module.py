from another_module import ABC, DEF


class A:
    i = 10

    def f(self):
        return ('Hello from A!')


class B(A):
    i = 11

    def g(self):
        return('Hello from B!')


class C(B):
    pass


class D(A):
    pass


class E(C, D):
    pass


class F(E, ABC):
    pass


class G(F, DEF, E):
    pass


b = B()
print(b.g())
print(b.f())
print(b.i)
a = A()
b = B()
c = C()
d = D()
e = E()
f = F()
g = G()
abc = ABC()
def_ = DEF()
g = G()
