X = [1, 2, 3, 4]
Y = [1, 2, 3]

def f(x,y):
    if x in [1, 2, 4] and y in [1, 3]:
        return x**2 + y**2
    else:
        return 0

from collections import defaultdict
probs = defaultdict(dict)
total = 0
for x in X:
    for y in Y:
        fxy = f(x,y)
        probs[x][y] = fxy
        total += fxy
        print("f(%s, %s) = %s" % (x, y, f(x,y)))

print('Answer a: 1/%s' % total)

big_y_numerator = 0
big_x_numerator = 0
same_xy_numerator = 0
y_3_numerator = 0
for x in X:
    for y in Y:
        if y < x:
            big_y_numerator += probs[x][y]
        if x < y:
            big_x_numerator += probs[x][y]
        if x == y:
            same_xy_numerator += probs[x][y]
        if y == 3:
            y_3_numerator += probs[x][y]

print('Answer b: %s/%s' % (big_y_numerator, total))
print('Answer c: %s/%s' % (big_x_numerator, total))
print('Answer d: %s/%s' % (same_xy_numerator, total))
print('Answer e: %s/%s' % (y_3_numerator, total))

x_probs = defaultdict(lambda: 0)
y_probs = defaultdict(lambda: 0)
for x in X:
    for y in Y:
        x_probs[x] += (probs[x][y] / total)
        y_probs[y] += (probs[x][y] / total)
print('Answer f x_probs: %s' % x_probs)
print('Answer f y_probs: %s' % y_probs)
print(probs)
print(total)
