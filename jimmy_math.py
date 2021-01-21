from math import sqrt

zijde3 = sqrt(zijde1 * zijde1 + zijde2 * zijde2)
print("De lengte van de diagonaal is {:.3f}.".format(zijde3))



def pytagoras(a, b):
    c = sqrt(a**2 + b**2)
    return c



pytagoras(4,9)