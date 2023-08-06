"""
Sequences lifted from finite difference weight calculation in
ZachLib to serve more general purposes
"""

__all__ = [
    "StirlingS1",
    "Binomial",
    "GammaBinomial",
    "Factorial"
]

import numpy as np

def StirlingS1(n):
    """Computes the Stirling numbers

    :param n:
    :type n:
    :return:
    :rtype:
    """
    stirlings = np.eye(n)
    for i in range(n):
        for j in range(i+1):
            stirlings[i, j] = (-1)**(i-j) *( (i-1)*abs(stirlings[i-1, j]) + abs(stirlings[i-1, j-1]))
    return stirlings

def Binomial(n):
    """
    Fast recursion to calculate all
    binomial coefficients up to binom(n, n)

    :param n:
    :type n:
    :return:
    :rtype:
    """
    binomials = np.eye(n)
    binomials[:, 0] = 1
    for i in range(2, n):
        if i%2 == 0:
            k = i/2 + 1
        else:
            k = (i+1)/2
        for j in range(int(k)):
            binomials[i, j] = binomials[i, i-j] = binomials[i-1, j-1] + binomials[i-1, j]
    return binomials

def GammaBinomial(s, n):
    """Generalized binomial gamma function

    :param s:
    :type s:
    :param n:
    :type n:
    :return:
    :rtype:
    """
    g = np.math.gamma
    g1 = g(s+1)
    g2 = np.array([g(m+1)*g(s-m+1) for m in range(n)])
    g3 = g1/g2
    return g3

def Factorial(n):
    """I was hoping to do this in some built in way with numpy...but I guess it's not possible?
    looks like by default things don't vectorize and just call math.factorial

    :param n:
    :type n:
    :return:
    :rtype:
    """

    base = np.arange(n, dtype=np.int64)
    base[0] = 1
    for i in range(1, n):
        base[i] = base[i]*base[i-1]
    return base