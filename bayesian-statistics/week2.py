from sys import exit
from scipy.stats import poisson, gamma, norm

# Week2's Background from Lesson 5
# Helpful: https://oneau.wordpress.com/2011/02/28/simple-statistics-with-scipy/

def test(expected, found, message, tolerance=0.001):
    diff = abs(expected - found)
    if diff >= tolerance:
        exit('%s, but found %s != %s by %s.' % (message, expected, found, diff))

px1 = poisson(3).pmf(1)
test(0.149, px1, '1. Let X ∼ Pois(3). Find P(X = 1). Answer is (0.149)')

pxlt1 = poisson(3).cdf(1)
test(0.199, pxlt1, '2. Let X ∼ Pois(3). Find P(X ≤ 1). (0.199)')

pxgt1 = 1 - poisson(3).cdf(1)
test(0.801, pxgt1, '3. Let X ∼ Pois(3). Find P(X > 1). (0.801)')
grv = gamma(2, scale=1/(1/3))

py_low = grv.cdf(0.5)
py_high = grv.cdf(1.5)
py_range = py_high - py_low
test(0.078, py_range, '4. Let Y ∼ Gamma(2, 1/3). Find P(0.5 < Y < 1.5). (0.078)')

pltz = norm(0,1).ppf(0.975)
test(1.96, pltz, '5. Let Z ∼ N(0, 1). Find z such that P(Z < z) = 0.975. (1.96)')

rvn = norm(loc=0,scale=1)
zrange = rvn.cdf(1.96) - rvn.cdf(-1.96)
test(0.95, zrange, '6. Let Z ∼ N(0, 1). Find P(−1.96 < Z < 1.96). (0.95)')

zbounds = rvn.ppf([.05,.95])
test(1.64, zbounds[1], '7. Let Z ∼ N(0, 1). Find z such that P(−z < Z < z) = 0.90. (1.64)', 0.01)

print('Success!')
