
# Results
**y = -27.4772x + 75.8890** where y is the respondent's rating of President Obama and x is the categorization of their anger.
The p-value is less than 0.0001.

The results of the linear regression model indicate that anger in politics is significantly and negatively associated
with ratings of President Obama. Specifically, this model indicates that increased anger in politics is associated with
a 27 point drop in the respondent's rating of the President.

# Background
All data is from the Outlook on Life survey, 2012.

* **W1_B4** Generally speaking, how angry do you feel about the way things are going in the country these days?
  * -1 Refused
  * 1  Extremely angry
  * 2  Very angry
  * 3  Somewhat angry
  * 4  A little angry
  * 5  Not angry at all
* **MOST_ANGRY** Divides **W1_B4** into two groups.
  * 0 for Not angry at all, A little angry, and Somewhat angry
  * 1 for Extremely angry and Very angry
  * The **explanatory variable**.
* **W1_D1** How would you rate [Barack Obama]
  * Scale from 0 to 100.
  * The **response variable**.

# Program Output

```
Outlook on Life Surveys, 2012
Data is 2294 rows, 436 columns
Define MOST_ANGRY as respondants that are Extremely or Very Angry.
Data is ready!
After prep, data is 2176 rows, 3 columns
   W1_B4  W1_D1  MOST_ANGRY
0    5.0    0.0           0
1    3.0   85.0           0
2    4.0   75.0           0
3    3.0   70.0           0
4    3.0   60.0           0
                            OLS Regression Results
==============================================================================
Dep. Variable:                  W1_D1   R-squared:                       0.144
Model:                            OLS   Adj. R-squared:                  0.144
Method:                 Least Squares   F-statistic:                     366.1
Date:                Wed, 05 Oct 2016   Prob (F-statistic):           1.52e-75
Time:                        19:05:55   Log-Likelihood:                -10547.
No. Observations:                2176   AIC:                         2.110e+04
Df Residuals:                    2174   BIC:                         2.111e+04
Df Model:                           1
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          t      P>|t|      [95.0% Conf. Int.]
------------------------------------------------------------------------------
Intercept     75.8890      0.793     95.735      0.000        74.334    77.443
MOST_ANGRY   -27.4772      1.436    -19.133      0.000       -30.293   -24.661
==============================================================================
Omnibus:                      147.791   Durbin-Watson:                   1.941
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              127.639
Skew:                          -0.520   Prob(JB):                     1.92e-28
Kurtosis:                       2.427   Cond. No.                         2.42
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

# Program
```
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ool = pd.read_csv('../data/ool_pds.csv', low_memory=False)

print('Outlook on Life Surveys, 2012')
print('Data is %d rows, %d columns' % ool.shape)

ANGER = 'W1_B4'
ANGER_Q = """Generally speaking, how angry do you feel about the way things are going in the
country these days?
-1 Refused
1  Extremely angry
2  Very angry
3  Somewhat angry
4  A little angry
5  Not angry at all"""

RATE_BARACK = 'W1_D1'
RATE_BARACK_Q = '[Barack Obama] How would you rate'


def prepare_numeric(data, attr):
    data[attr] = pd.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, np.nan)


def prepare_rate(data, attr):
    data[attr] = pd.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, np.nan)
    data[attr] = data[attr].replace(998, np.nan)

prepare_numeric(ool, ANGER)
prepare_rate(ool, RATE_BARACK)

ool = ool.loc[:,[ANGER, RATE_BARACK]]
ool = ool.dropna()


def most_angry(row):
    # 1: Extremely or Very Angry
    # 0: Somewhat, A little, or Not Angry
    if row[ANGER] == 1 or row[ANGER] == 2:
        return 1
    else:
        return 0

print('Define MOST_ANGRY as respondants that are Extremely or Very Angry.')
ool['MOST_ANGRY'] = ool.apply(most_angry, axis=1)

print('Data is ready!')
print('After prep, data is %d rows, %d columns' % ool.shape)
print(ool.head())

regression = smf.ols('%s ~ MOST_ANGRY' % RATE_BARACK, data=ool).fit()
print(regression.summary())
```
