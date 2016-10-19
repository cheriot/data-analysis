# Question
How does an American's self-described location on the political spectrum correlate with their anger at the direction of the country? Using data from the Outlook on Life Survey, 2012, I'll use logistic regression explore whether a relationship exists. My hypothesis from observing the 2016 presidential election is that there is more anger among the most conservative Americans.

# Data

#### We hear a lot of talk these days about liberals and conservatives. Where would you place YOURSELF on this 7 point scale?

* 1 Extremely liberal
* 2 Liberal
* 3 Slightly liberal
* 4 Moderate; middle of the road
* 5 Slightly conservative
* 6 Conservative
* 7 Extremely conservative
* 1 Refused 2.6%

#### Generally speaking, how angry do you feel about the way things are going in the country these days?
* -1 Refused
* 1  Extremely angry
* 2  Very angry
* 3  Somewhat angry
* 4  A little angry
* 5  Not angry at all"""

I've created a **MOST_ANGRY** binary column where 1 represents Extremely and Very angry. This will be the response variable of our regression. 

# Results
#### MOST_ANGRY ~ C(POLITICAL_SPECTRUM, Treatment(reference=4))
Category 4 represents "Moderate; middle of the road" and will be the baseline that other categories are compared to.

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:             MOST_ANGRY   No. Observations:                 2221
Model:                          Logit   Df Residuals:                     2214
Method:                           MLE   Df Model:                            6
Date:                Wed, 19 Oct 2016   Pseudo R-squ.:                 0.05122
Time:                        17:30:59   Log-Likelihood:                -1285.4
converged:                       True   LL-Null:                       -1354.8
                                        LLR p-value:                 1.820e-27
===========================================================================================================
                                              coef    std err          z      P>|z|      [95.0% Conf. Int.]
-----------------------------------------------------------------------------------------------------------
Intercept                                  -1.0561      0.078    -13.614      0.000        -1.208    -0.904
C(W1_C2, Treatment(reference=4))[T.1.0]     0.1768      0.265      0.667      0.505        -0.343     0.697
C(W1_C2, Treatment(reference=4))[T.2.0]    -0.1577      0.156     -1.012      0.311        -0.463     0.148
C(W1_C2, Treatment(reference=4))[T.3.0]    -0.5160      0.175     -2.947      0.003        -0.859    -0.173
C(W1_C2, Treatment(reference=4))[T.5.0]     0.2439      0.148      1.649      0.099        -0.046     0.534
C(W1_C2, Treatment(reference=4))[T.6.0]     1.0690      0.138      7.771      0.000         0.799     1.339
C(W1_C2, Treatment(reference=4))[T.7.0]     1.7298      0.253      6.833      0.000         1.234     2.226
===========================================================================================================
                                         Lower CI  Upper CI  OddsRatio
Intercept                                    0.30      0.40       0.35
C(W1_C2, Treatment(reference=4))[T.1.0]      0.71      2.01       1.19
C(W1_C2, Treatment(reference=4))[T.2.0]      0.63      1.16       0.85
C(W1_C2, Treatment(reference=4))[T.3.0]      0.42      0.84       0.60
C(W1_C2, Treatment(reference=4))[T.5.0]      0.96      1.71       1.28
C(W1_C2, Treatment(reference=4))[T.6.0]      2.22      3.81       2.91
C(W1_C2, Treatment(reference=4))[T.7.0]      3.43      9.26       5.64
```

Political Spectrum |                      Lower CI |  Upper CI  | OddsRatio | Significant?
:-- | --: | --: | --: | :---:
Intercept                                |   0.30  |   0.40   |   0.35 |
Extremely liberal       |   0.71  |   2.01   |   1.19 |
Liberal                 |   0.63  |   1.16   |   0.85 |
Slightly liberal        |   0.42  |   0.84   |   0.60 | not most angry
Moderate; middle of the road | - | - | - | -
Slightly conservative   |   0.96  |   1.71   |   1.28 |
Conservative            |   2.22  |   3.81   |   2.91 | most angry
Extremely conservative  |   3.43  |   9.26   |   5.64 | most angry

The confidence intervals for Conservative and Extremely conservative are significantly higher than 1 and thus associated with increased levels of anger. The confidence intervals for Extremely liberal, Liberal, and Slightly conservative include 1 and thus, are not significant. Slightly liberal is associated with less anger.

This confirms the hypothesis. Self-described conservatives are more than twice as likely to be among the most angry Americans and self-described extremely conservatives are more than 5 times more likely to be among the most angry Americans.

# Program Output
```
Define MOST_ANGRY as respondents that are Extremely or Very Angry.
Data ready (2221, 7)
   W1_C2  PPETHM  W1_B4  W1_E61_C  PPEDUCAT  PPAGECAT  MOST_ANGRY
0   7.00       4   5.00         4         2         5           0
1   4.00       2   3.00        -1         1         5           0
2   3.00       2   4.00         4         4         3           0
3   2.00       2   3.00         4         4         6           0
4   4.00       1   3.00        -1         4         3           0
--------------------------------------------------------------------------------
Generally speaking, how angry do you feel about the way things are going in the
country these days?
-1 Refused
1  Extremely angry
2  Very angry
3  Somewhat angry
4  A little angry
5  Not angry at all
Response counts:
MOST_ANGRY
0    1557
1     664
dtype: int64
Response percentages:
MOST_ANGRY
0   70.10
1   29.90
dtype: float64
--------------------------------------------------------------------------------
Anger and political spectrum among americans (crosstab W1_C2 * W1_B4).
Counts
W1_B4  1.00  2.00  3.00  4.00  5.00
W1_C2                              
1.00     14     8    21    11    21
2.00     12    59   111    94    34
3.00     10    39   105    96    35
4.00     68   156   287   225   132
5.00     26    65   100    71    34
6.00     71    85    85    45    24
7.00     35    16    13     4     9
Percentages
W1_B4  1.00  2.00  3.00  4.00  5.00
W1_C2                              
1.00  18.67 10.67 28.00 14.67 28.00
2.00   3.87 19.03 35.81 30.32 10.97
3.00   3.51 13.68 36.84 33.68 12.28
4.00   7.83 17.97 33.06 25.92 15.21
5.00   8.78 21.96 33.78 23.99 11.49
6.00  22.90 27.42 27.42 14.52  7.74
7.00  45.45 20.78 16.88  5.19 11.69
Optimization terminated successfully.
         Current function value: 0.578743
         Iterations 5
                           Logit Regression Results                           
==============================================================================
Dep. Variable:             MOST_ANGRY   No. Observations:                 2221
Model:                          Logit   Df Residuals:                     2214
Method:                           MLE   Df Model:                            6
Date:                Wed, 19 Oct 2016   Pseudo R-squ.:                 0.05122
Time:                        17:30:59   Log-Likelihood:                -1285.4
converged:                       True   LL-Null:                       -1354.8
                                        LLR p-value:                 1.820e-27
===========================================================================================================
                                              coef    std err          z      P>|z|      [95.0% Conf. Int.]
-----------------------------------------------------------------------------------------------------------
Intercept                                  -1.0561      0.078    -13.614      0.000        -1.208    -0.904
C(W1_C2, Treatment(reference=4))[T.1.0]     0.1768      0.265      0.667      0.505        -0.343     0.697
C(W1_C2, Treatment(reference=4))[T.2.0]    -0.1577      0.156     -1.012      0.311        -0.463     0.148
C(W1_C2, Treatment(reference=4))[T.3.0]    -0.5160      0.175     -2.947      0.003        -0.859    -0.173
C(W1_C2, Treatment(reference=4))[T.5.0]     0.2439      0.148      1.649      0.099        -0.046     0.534
C(W1_C2, Treatment(reference=4))[T.6.0]     1.0690      0.138      7.771      0.000         0.799     1.339
C(W1_C2, Treatment(reference=4))[T.7.0]     1.7298      0.253      6.833      0.000         1.234     2.226
===========================================================================================================
                                         Lower CI  Upper CI  OddsRatio
Intercept                                    0.30      0.40       0.35
C(W1_C2, Treatment(reference=4))[T.1.0]      0.71      2.01       1.19
C(W1_C2, Treatment(reference=4))[T.2.0]      0.63      1.16       0.85
C(W1_C2, Treatment(reference=4))[T.3.0]      0.42      0.84       0.60
C(W1_C2, Treatment(reference=4))[T.5.0]      0.96      1.71       1.28
C(W1_C2, Treatment(reference=4))[T.6.0]      2.22      3.81       2.91
C(W1_C2, Treatment(reference=4))[T.7.0]      3.43      9.26       5.64
```

# Program
```
import numpy as np
import pandas as pd
import seaborn
import statsmodels.formula.api as smf

# Predict MOST_ANGRY with logistic regression using POLITICAL_SPECTRUM

# Explanatory variable
POLITICAL_SPECTRUM = 'W1_C2'
POLITICAL_SPECTRUM_Q = """We hear a lot of talk these days about liberals and conservatives. Where would you place YOURSELF on this 7 point scale?'
1  Extremely liberal               75      3.3%
2  Liberal                         312    13.6%
3  Slightly liberal                286    12.5%
4  Moderate; middle of the road    874    38.1%
5  Slightly conservative           297    12.9%
6  Conservative                    311    13.6%
7  Extremely conservative          79      3.4%
-1 Refused                         60      2.6%
"""

# Response variable
ANGER = 'W1_B4'
ANGER_Q = """Generally speaking, how angry do you feel about the way things are going in the
country these days?
-1 Refused
1  Extremely angry
2  Very angry
3  Somewhat angry
4  A little angry
5  Not angry at all"""
ANGER_CATEGORIES = [1, 2, 3, 4, 5]


def most_angry(row):
    # Collapse ANGER into a binary categorical value.
    # 1: Extremely or Very Angry
    # 0: Somewhat, A little, or Not Angry
    if row[ANGER] == 1 or row[ANGER] == 2:
        return 1
    else:
        return 0


def prepare_numeric(data, attr):
    data[attr] = pd.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, np.nan)


def print_divider():
    print('-'*80)


def summarize(data, attr, desc):
    counts = data.groupby(attr, sort=False).size()
    relative = counts * 100 / len(data)
    print_divider()
    print(desc)
    print('Response counts:')
    print(counts)
    print('Response percentages:')
    print(relative)


def crosstab_summarize(data, attr1, attr2, title):
    print_divider()
    print('%s (crosstab %s * %s).' % (title, attr1, attr2))
    crosstab = pandas.crosstab(data[attr1], data[attr2])
    relative_crosstab = crosstab.apply(lambda r: 100 * r / r.sum(), axis=1)
    print('Counts')
    print(crosstab)
    print('Percentages')
    print(relative_crosstab)
    return crosstab, relative_crosstab

ool_raw = pd.read_csv('../data/ool_pds.csv')[[POLITICAL_SPECTRUM, ETHNICITY, ANGER, CHILD_BLACK, EDUCATION, AGE]]

print('Define MOST_ANGRY as respondents that are Extremely or Very Angry.')
ool_raw['MOST_ANGRY'] = ool_raw.apply(most_angry, axis=1)

prepare_numeric(ool_raw, 'MOST_ANGRY')
prepare_numeric(ool_raw, POLITICAL_SPECTRUM)
prepare_numeric(ool_raw, ETHNICITY)
prepare_numeric(ool_raw, ANGER)
prepare_numeric(ool_raw, AGE)

# Create CHILD_BLACK_X binary columns
# ool_raw = ool_raw[ ool_raw[CHILD_BLACK] != -1 ]
# racial_outlook = pd.get_dummies(ool_raw[CHILD_BLACK], prefix='CHILD_BLACK')
# ool_raw = pd.concat([ool_raw, racial_outlook], axis=1)

ool = ool_raw.dropna()
print('Data ready %s' % (ool.shape, ))
print(ool.head())

summarize(ool, 'MOST_ANGRY', ANGER_Q)
crosstab_summarize(ool, POLITICAL_SPECTRUM, ANGER, 'Anger and political spectrum among americans')

# Don't use a dummy variable for every single category to avoid the dummy variable trap
# where perfect multicollinearity occurs. Using C() in the formula does this automatically.
# Use category 4, Moderate; middle of the road, as the baseline.
formula = "MOST_ANGRY ~ C(%s, Treatment(reference=4))" % (POLITICAL_SPECTRUM)
regression = smf.logit(formula, data=ool).fit()
print(regression.summary())
conf_int = regression.conf_int()
conf_int['OddsRatio'] = regression.params
conf_int.columns = ['Lower CI', 'Upper CI', 'OddsRatio']
print(numpy.exp(conf_int))
```
