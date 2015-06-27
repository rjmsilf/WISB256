from Symbolische_manipulatie_3 import *

a=Constant(1)
b=Constant(2)
c=Constant(3)
d=Constant(4)
e=Constant(5)
x=Variable('x')
y=Variable('y')
z=Variable('z')

#print(d*x/b)

iets=(-a)**c
print(iets.simplify())