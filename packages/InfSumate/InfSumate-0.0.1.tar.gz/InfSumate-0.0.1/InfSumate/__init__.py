def geoMet(a, r):
    return (a/(1-r))


def geoMetPartial(a, r, n, i):
    sum = 0
    term = 0
    while n <= i:
        term = a*(r**n)
        sum = term+sum
        n = n + 1
    return sum
