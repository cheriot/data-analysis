import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
import sklearn.metrics
from sklearn.ensemble import ExtraTreesClassifier

# HISPANIC OR LATINO ORIGIN
# 1. Yes
# 2.  No
HISPANIC = 'S1Q1C'

# "BLACK OR AFRICAN AMERICAN" CHECKED IN MULTIRACE CODE
# 1. Yes
# 2.  No
BLACK = 'S1Q1D3'

# "AMERICAN INDIAN OR ALASKA NATIVE" CHECKED IN MULTIRACE CODE
# 1. Yes
# 2.  No
AM_INDIAN = 'S1Q1D1'

# "WHITE" CHECKED IN MULTIRACE CODE
# 1. Yes
# 2.  No
WHITE = 'S1Q1D5'

# "ASIAN" CHECKED IN MULTIRACE CODE
# 1. Yes
# 2.  No
ASIAN = 'S1Q1D2'

# SEX
# 1. Male
# 2. Femail
GENDER = 'SEX'

# DATE OF BIRTH: YEAR
# 1895-1984.  Year
BIRTH_YEAR = 'DOBY'

# MSA TYPE
# 1.  In MSA - in central city
# 2.  In MSA - not in central city
# 3.  Not in MSA
URBAN_DENSITY = 'CCS'

# PRESENT SITUATION INCLUDES RETIRED
# 1. Yes
# 2.  No
RETIRED = 'S1Q7A9'

# PRESENT SITUATION INCLUDES IN SCHOOL FULL TIME
# 1. Yes
# 2.  No
STUDENT = 'S1Q7A10'

# TOTAL PERSONAL INCOME IN LAST 12 MONTHS: CATEGORY
#  0.  $0 (No personal income)
#  1.  $1 to $4,999
#  2.  $5,000 to $7,999
#  3.  $8,000 to $9,999
#  4.  $10,000 to $12,999
#  5.  $13,000 to $14,999
#  6.  $15,000 to $19,999
#  7.  $20,000 to $24,999
#  8.  $25,000 to $29,999
#  9.  $30,000 to $34,999
# 10.  $35,000 to $39,999
# 11.  $40,000 to $49,999
# 12.  $50,000 to $59,999
# 13.  $60,000 to $69,999
# 14.  $70,000 to $79,999
# 15.  $80,000 to $89,999
# 16.  $90,000 to $99,999
# 17.  $100,000 or more
INCOME = 'S1Q10B'

# DRINKING STATUS
#  1.  Current drinker
#  2.  Ex-drinker
#  3.  Lifetime Abstainer
DRINK_STATUS = 'CONSUMER'

# MAIN TYPE OF ALCOHOL CONSUMED DURING PERIOD OF HEAVIEST DRINKING
# 1.  Coolers
# 2.  Beer
# 3.  Wine
# 4.  Liquor
# 9.  Unknown
# BL.  NA, lifetime abstainer
DRINK_PREF = 'S2AQ23'

predictor_columns = [DRINK_STATUS, INCOME, HISPANIC, WHITE, BLACK, ASIAN, AM_INDIAN, GENDER, BIRTH_YEAR, RETIRED, STUDENT]
target_column = DRINK_PREF

nesarc = pd.read_csv("../data/nesarc.csv")
nesarc = nesarc[predictor_columns + [target_column]].dropna()
nesarc[DRINK_PREF].describe()

print(nesarc.dtypes)
print(nesarc.describe())

# Try to predict a person's type of drink
predictors = nesarc[predictor_columns]
targets = nesarc[target_column]
pred_train, pred_test, tar_train, tar_test  = train_test_split(predictors, targets, test_size=.4)

print('training and test shapes:')
print(pred_train.shape)
print(pred_test.shape)
print(tar_train.shape)
print(tar_test.shape)

# Learn!
classifier=RandomForestClassifier(n_estimators=25)
classifier=classifier.fit(pred_train,tar_train)
predictions=classifier.predict(pred_test)

# Evaluate learning
print('Confusion matrix:')
print(sklearn.metrics.confusion_matrix(tar_test,predictions))
print('Accuracy score:')
print(sklearn.metrics.accuracy_score(tar_test, predictions))

model = ExtraTreesClassifier()
model.fit(pred_train,tar_train)
print('Feature importance:')
print(model.feature_importances_)


"""
Running a different number of trees and see the effect
 of that on the accuracy of the prediction
"""

trees=range(25)
accuracy=np.zeros(25)

for idx in range(len(trees)):
    classifier=RandomForestClassifier(n_estimators=idx + 1)
    classifier=classifier.fit(pred_train,tar_train)
    predictions=classifier.predict(pred_test)
    accuracy[idx]=sklearn.metrics.accuracy_score(tar_test, predictions)

fig = plt.figure()
plt.cla()
plt.xlabel('Trees in Forest')
plt.ylabel('Accuracy Score')
plt.plot(trees, accuracy)
fig.savefig('accuracy-trees.png')
