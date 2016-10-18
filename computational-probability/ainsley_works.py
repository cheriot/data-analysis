import math
import numpy as np
import operator as op
from functools import reduce

def float_range(a, b):
    return [float(x) for x in range(a, b)]

S = float_range(1,4+1)
C = float_range(0, 2*len(S)+1)
D = float_range(0, len(S)+1)

def n_choose_r(n, r):
    # print('n_choose_r(n=%s, r=%s)' % (n, r))
    r = int(min(r, n-r))
    if r == 0: return 1
    n = int(n)
    numer = reduce(op.mul, range(n, n-r, -1))
    denom = reduce(op.mul, range(1, r+1))
    return float(numer)/float(denom)

assert(n_choose_r(4,3) == 4)
assert(n_choose_r(3,3) == 1)
assert(n_choose_r(4,2) == 6)
assert(n_choose_r(1,1) == 1)
assert(n_choose_r(2,1) == 2)

def sum(nums):
    return reduce(op.add, nums)

def prob_c_given_s(c, s):
    if c in C and s in S:
        return 1.0 / (2*s + 1)
    else:
        raise ValueError('Illegal arguments for prob_c_given_s(%s, %s)' % (c, s))

def expected_c_given_s(s):
    expected = sum([c * prob_c_given_s(c, s) for c in C])
    print('expected_c_given_s(%s) = %s' % (s, expected))
    return expected

def prob_s(s):
    if s in S:
        return 1/len(S) # Uniform likelihood.
    else:
        raise ValueError('S cannot take the value %s', s)

def prob_d_given_s(d, s, q):
    if d in D and s in S and q >= 0:
        if d <= s:
            prob = n_choose_r(s, d) * (q**d) * ((1-q)**(s-d))
            print('prob_d_given_s(d=%s, s=%s, q=%s) = %s' % (d, s, q, prob))
            return prob
        else:
            print('prob_d_given_s(d=%s, s=%s, q=%s) = %s' % (d, s, q, 0))
            return 0
    else:
        raise ValueError('Illegal arguments for prob_d_given_s(%s, %s, %s)' % (d, s, q))

# (1 choose 1)(.2^1)((1-.2)^(1-1))
assert(prob_d_given_s(1,1,.2) == .2)
# (2 choose 1)(.2^1)((1-.2)^(2-1))
assert(abs(prob_d_given_s(1,2,.2) - .32) < .0000000001)

def prob_d(d, q):
    if d in D and q >= 0:
        return sum([prob_d_given_s(d, s, q) for s in S])
    else:
        raise ValueError('Illegal arguments for prob_d(%s, %s)' % (d, q))

def prob_s_and_d(s, d, q):
    prob = prob_d_given_s(d, s, q) * prob_s(s)
    print('prob_s_and_d(%s, %s, %s) = %s' % (s, d, q, prob))
    return prob

print('S %s' % list(S))
print('C %s' % list(C))
print('D %s' % list(D))

def expected_c_given_d(q, d):
    # for all S, d=1, q
    return sum([expected_c_given_s(s) * prob_s_and_d(s, d, q) for s in S])

def solve(q, d):
    print('Answer q = %s, E[C|D=%s] = %f' % (q, d, expected_c_given_d(q, d)))

def solve_b(q, d):
    prob_c_given_d = reduce(op.add, [(1/(2*s+1)) * prob_d_given_s(d, s, q) * 1/4 for s in S])
    return reduce(op.add, [c*prob_c_given_d for c in C])

def joint_prob(s, c, d, q):
    # P(C|S) * P(D|S) * P(S)
    ps = 1/len(S) # Uniform distribution
    # print('P(s) = %s' % (ps))
    pds = 0
    if d <= s:
        pds = n_choose_r(s,d) * q**d * (1-q)**(s-d)
    # print('P(D=%s|S=%s) = %s from %s * %s * %s' % (d, s, pds, n_choose_r(s,d), q**d, (1-q)**(s-d)))
    pcs = 0
    if c <= 2*s:
        pcs = 1 / (2*s + 1)
    # print('P(C=%s|S=%s) = %s\n' % (c, s, pcs))
    return pds * pcs * ps

def solve_c(q, d):
    total = 0
    for s in S:
        for c in C:
            total += c * joint_prob(s, c, d, q)
    return total

assert(abs(solve_c(.2, 1) - 0.9076) < 0.0001)

def solve_d(q, given_d):
    jp = np.zeros([len(S), len(C), len(D)])
    # print(jp.shape)
    # print(jp)
    for s in S:
        for c in C:
            for d in D:
                jp[s-1][c-1][d-1] = joint_prob(s,c,d,q)
    # print(jp)
    prob_c_and_d = jp.sum(axis=0)
    # print(prob_c_and_d.shape)
    # print(prob_c_and_d)
    prob_c_given_d = prob_c_and_d[:,given_d]
    prob_c_given_d = prob_c_given_d / prob_c_given_d.sum()
    # print(prob_c_given_d.shape)
    print(prob_c_given_d)
    print(prob_c_given_d.sum())
    # print(list(C))
    terms = prob_c_given_d * np.array(list(C))
    # print(terms)
    # print(terms.sum())
    return terms.sum()


# Submitted (incorrectly):
# 2.079, 1.307, 0.853
# 0.9076, 0.781, 0.66885
# 3.597, 3.762, 4

solve(.2, 1)
print('solve_b = %s' % solve_b(.2, 1))
print('solve_c = %s' % solve_c(.2, 1))
print('solve_d = %s' % solve_d(.2, 1))
# print('solve_d = %s' % solve_d(.5, 2))
# print('solve_d = %s' % solve_d(.7, 3))
# solve(.5, 2)
# solve(.7, 3)
