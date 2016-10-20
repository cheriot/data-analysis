import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

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
INCOME_CAT = 'S1Q10B'

# TOTAL HOUSEHOLD INCOME IN LAST 12 MONTHS
# 24-3000000.  Household income in dollars
HOUSEHOLD_INCOME = 'S1Q12A'

# TOTAL PERSONAL INCOME IN LAST 12 MONTHS
# 24-3000000.  Income in dollars
PERSONAL_INCOME = 'S1Q10A'

# NUMBER OF DAYS SINCE LAST DRINK (RESPONDENTS WHO DRANK IN LAST MONTH)
# ---------------------------------------------------------------------
# 0.  Less than one day
# 1-28.  Number of days
# BL.  NA, did not drink or unknow if drank within last month
DAYS_SINCE_DRINK = 'S2AQ15R2'

# DRINKING STATUS
# 1.  Current drinker
# 2.  Ex-drinker
# 3.  Lifetime Abstainer
DRINK_STATUS = 'CONSUMER'

# MAIN TYPE OF ALCOHOL CONSUMED DURING PERIOD OF HEAVIEST DRINKING
# 1.  Coolers
# 2.  Beer
# 3.  Wine
# 4.  Liquor
# 9.  Unknown
# BL.  NA, lifetime abstainer
DRINK_PREF = 'S2AQ23'

def clean_drink_pref(row):
    drink_pref = row[DRINK_PREF]
    if drink_pref is 9:
        return np.nan
    return drink_pref

# NUMBER OF DRINKS OF ANY ALCOHOL USUALLY CONSUMED ON DAYS WHEN DRANK ALCOHOL
# IN LAST 12 MONTHS
# ---------------------------------------------------------------------------
# 1-98. Number of drinks
# 99.   Unknown
# BL.   NA, former drinker or lifetime abstainer
USUAL_DRINKS = 'S2AQ8B'

source_columns = [DRINK_STATUS, PERSONAL_INCOME, HISPANIC, WHITE, BLACK, ASIAN, AM_INDIAN, GENDER, BIRTH_YEAR, RETIRED, STUDENT, DRINK_PREF]
discard_columns = [DRINK_PREF]
generate_columns = ['DRINK_PREF_coolers', 'DRINK_PREF_beer', 'DRINK_PREF_wine', 'DRINK_PREF_liquor']
target_column = USUAL_DRINKS

nesarc = pd.read_csv('../data/nesarc.csv', low_memory=False)
nesarc = nesarc[ nesarc[DRINK_STATUS] != 3 ]

# Make these columns numeric.
def to_numeric(data, *attrs):
    for attr in attrs:
      data[attr] = pd.to_numeric(data[attr], errors='coerce')
to_numeric(nesarc, USUAL_DRINKS, PERSONAL_INCOME, DRINK_PREF)

# Make dummy columns for the DRINK_PREF options
nesarc[DRINK_PREF] = nesarc[DRINK_PREF].map(
        { 1: 'coolers', 2: 'beer', 3: 'wine', 4: 'liquor'})
drink_pref_dummies = pd.get_dummies(nesarc[DRINK_PREF], prefix='DRINK_PREF')
nesarc = pd.concat([nesarc, drink_pref_dummies], axis=1)

# Scale everything to mean 0, stdev 1
def to_normal_scale(data, *attrs):
    for attr in attrs:
        data[attr] = preprocessing.scale(data[attr].astype('float64'))
to_normal_scale(nesarc, DRINK_STATUS, PERSONAL_INCOME, HISPANIC, WHITE, BLACK, ASIAN, AM_INDIAN, GENDER, BIRTH_YEAR, RETIRED, STUDENT)

predictor_columns = [col for col in source_columns + generate_columns if col not in discard_columns]
print('predictor_columns %s' % predictor_columns)
nesarc = nesarc[predictor_columns + [target_column]].dropna()

print('Data read!')
print(nesarc.shape)
print(nesarc.dtypes)
print(nesarc.head())
print(nesarc.describe())

# Try to predict how many drinks a person will have.
predictors = nesarc[predictor_columns]
targets = nesarc[target_column]
pred_train, pred_test, tar_train, tar_test = train_test_split(
        predictors, targets, test_size=.3, random_state=215)

print('training and test shapes:')
print(pred_train.shape)
print(pred_test.shape)
print(tar_train.shape)
print(tar_test.shape)

# Learn!
model = LassoLarsCV(cv=10, precompute=False).fit(pred_train,tar_train)

# print variable names and regression coefficients
print(dict(zip(predictors.columns, model.coef_)))

# plot coefficient progression
coefficient_progression_fig = plt.figure()
m_log_alphas = -np.log10(model.alphas_)
ax = plt.gca()
plt.plot(m_log_alphas, model.coef_path_.T)
plt.axvline(-np.log10(model.alpha_), linestyle='--', color='k', label='alpha CV')
plt.ylabel('Regression Coefficients')
plt.xlabel('-log(alpha)')
plt.title('Regression Coefficients Progression for Lasso Paths')
coefficient_progression_fig.savefig('week3_coefficient_progression.png')

# plot mean square error for each fold
m_log_alphascv = -np.log10(model.cv_alphas_)
mse_fig = plt.figure()
plt.plot(m_log_alphascv, model.cv_mse_path_, ':')
plt.plot(m_log_alphascv, model.cv_mse_path_.mean(axis=-1), 'k',
         label='Average across the folds', linewidth=2)
plt.axvline(-np.log10(model.alpha_), linestyle='--', color='k', label='alpha CV')
plt.legend()
plt.xlabel('-log(alpha)')
plt.ylabel('Mean squared error')
plt.title('Mean squared error on each fold')
mse_fig.savefig('week3_mse.png')

# MSE from training and test data
from sklearn.metrics import mean_squared_error
train_error = mean_squared_error(tar_train, model.predict(pred_train))
test_error = mean_squared_error(tar_test, model.predict(pred_test))
print('training data MSE')
print(train_error)
print('test data MSE')
print(test_error)

# R-square from training and test data
rsquared_train=model.score(pred_train,tar_train)
rsquared_test=model.score(pred_test,tar_test)
print('training data R-square')
print(rsquared_train)
print('test data R-square')
print(rsquared_test)
