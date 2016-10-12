import numpy as np
import math

joint_prob_XY = np.array([[0.10, 0.09, 0.11], [0.08, 0.07, 0.07], [0.18, 0.13, 0.17]])
# Marginal distributions
prob_X = joint_prob_XY.sum(axis=1)
prob_Y = joint_prob_XY.sum(axis=0)

# IF they were independent:
joint_prob_XY_indep = np.outer(prob_X, prob_Y)

# What is I(X;Y)?
mutual = 0
for x in range(joint_prob_XY.shape[0]):
    for y in range(joint_prob_XY.shape[1]):
        actual = joint_prob_XY[x][y]
        independent = joint_prob_XY_indep[x][y]
        delta = actual * math.log((actual / independent), 2)
        mutual += delta
        print('%s, %s = %s' % (x, y, delta))

print('Answer = %s' % mutual)
