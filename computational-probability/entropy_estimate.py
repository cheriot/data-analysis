import math

for n in range(1, 11):
    x = n/10
    print('%s = %s' % (x, x*math.log(1/x,2)))
