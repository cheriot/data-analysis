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

I've created a **MOST_ANGRY** binary column where 1 represents Extremely and Very angry. This will be the response variable of our regression. Because the survey oversampled black Americans, I've included a binary variable **BLACK** to make sure this does not confound the relationship.

# Results
#### MOST_ANGRY ~ C(POLITICAL_SPECTRUM, Treatment(reference=4)) + BLACK
```
Category 4 represents "Moderate; middle of the road" and will be the baseline that other categories are compared to.

                           Logit Regression Results
==============================================================================
Dep. Variable:             MOST_ANGRY   No. Observations:                 2221
Model:                          Logit   Df Residuals:                     2213
Method:                           MLE   Df Model:                            7
Date:                Wed, 19 Oct 2016   Pseudo R-squ.:                 0.07333
Time:                        17:58:38   Log-Likelihood:                -1255.4
converged:                       True   LL-Null:                       -1354.8
                                        LLR p-value:                 2.177e-39
===========================================================================================================
                                              coef    std err          z      P>|z|      [95.0% Conf. Int.]
-----------------------------------------------------------------------------------------------------------
Intercept                                  -0.6265      0.094     -6.662      0.000        -0.811    -0.442
C(W1_C2, Treatment(reference=4))[T.1.0]     0.2288      0.269      0.850      0.395        -0.299     0.756
C(W1_C2, Treatment(reference=4))[T.2.0]    -0.1324      0.158     -0.838      0.402        -0.442     0.177
C(W1_C2, Treatment(reference=4))[T.3.0]    -0.5409      0.177     -3.053      0.002        -0.888    -0.194
C(W1_C2, Treatment(reference=4))[T.5.0]     0.1612      0.150      1.071      0.284        -0.134     0.456
C(W1_C2, Treatment(reference=4))[T.6.0]     0.9196      0.141      6.539      0.000         0.644     1.195
C(W1_C2, Treatment(reference=4))[T.7.0]     1.5132      0.258      5.874      0.000         1.008     2.018
BLACK                                      -0.7601      0.099     -7.706      0.000        -0.953    -0.567
===========================================================================================================
                                         Lower CI  Upper CI  OddsRatio
Intercept                                0.444514  0.642655   0.534480
C(W1_C2, Treatment(reference=4))[T.1.0]  0.741729  2.130490   1.257079
C(W1_C2, Treatment(reference=4))[T.2.0]  0.642820  1.193749   0.875994
C(W1_C2, Treatment(reference=4))[T.3.0]  0.411467  0.823926   0.582253
C(W1_C2, Treatment(reference=4))[T.5.0]  0.874824  1.577921   1.174906
C(W1_C2, Treatment(reference=4))[T.6.0]  1.904023  3.304199   2.508240
C(W1_C2, Treatment(reference=4))[T.7.0]  2.740974  7.523493   4.541112
BLACK                                    0.385396  0.567331   0.467597
```

Results |                      Lower CI |  Upper CI  | OddsRatio | Association?
:-- | --: | --: | --: | :---:
Intercept              | 0.444514  | 0.642655  | 0.534480 |
Extremely liberal      | 0.741729  | 2.130490  | 1.257079 |
Liberal                | 0.642820  | 1.193749  | 0.875994 |
Slightly liberal       | 0.411467  | 0.823926  | 0.582253 | less than most angry
Moderate; middle of the road | - | - | - | -
Slightly conservative  | 0.874824  | 1.577921  | 1.174906 | 
Conservative           | 1.904023  | 3.304199  | 2.508240 | most angry
Extremely conservative | 2.740974  | 7.523493  | 4.541112 | most angry
BLACK                  | 0.385396  | 0.567331  | 0.467597 | less than most angry

The confidence intervals for Conservative and Extremely conservative are significantly higher than 1 and thus associated with increased levels of anger. The confidence intervals for Extremely liberal, Liberal, and Slightly conservative include 1 and thus, are not significant. Slightly liberal is associated with less anger.

This confirms the hypothesis. Self-described conservatives are more than twice as likely to be among the most angry Americans and self-described extremely conservatives are more than 4 times more likely to be among the most angry Americans.

The oversampling of black Americans in the survey does not confound the relationship. The findings are the same direction and similar magnitude with and without including the ethnicity in regression.

# Program Output
```
Define MOST_ANGRY as respondents that are Extremely or Very Angry.
Data ready (2221, 5)
   W1_C2  PPETHM  W1_B4  MOST_ANGRY  BLACK
0    7.0       4    5.0           0      0
1    4.0       2    3.0           0      1
2    3.0       2    4.0           0      1
3    2.0       2    3.0           0      1
4    4.0       1    3.0           0      0
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
0    70.103557
1    29.896443
dtype: float64
--------------------------------------------------------------------------------
Anger and political spectrum among americans (crosstab W1_C2 * W1_B4).
Counts
W1_B4  1.0  2.0  3.0  4.0  5.0
W1_C2
1.0     14    8   21   11   21
2.0     12   59  111   94   34
3.0     10   39  105   96   35
4.0     68  156  287  225  132
5.0     26   65  100   71   34
6.0     71   85   85   45   24
7.0     35   16   13    4    9
Percentages
W1_B4        1.0        2.0        3.0        4.0        5.0
W1_C2
1.0    18.666667  10.666667  28.000000  14.666667  28.000000
2.0     3.870968  19.032258  35.806452  30.322581  10.967742
3.0     3.508772  13.684211  36.842105  33.684211  12.280702
4.0     7.834101  17.972350  33.064516  25.921659  15.207373
5.0     8.783784  21.959459  33.783784  23.986486  11.486486
6.0    22.903226  27.419355  27.419355  14.516129   7.741935
7.0    45.454545  20.779221  16.883117   5.194805  11.688312
Logistic regression formula: MOST_ANGRY ~ C(W1_C2, Treatment(reference=4))
Optimization terminated successfully.
         Current function value: 0.578743
         Iterations 5
                           Logit Regression Results
==============================================================================
Dep. Variable:             MOST_ANGRY   No. Observations:                 2221
Model:                          Logit   Df Residuals:                     2214
Method:                           MLE   Df Model:                            6
Date:                Wed, 19 Oct 2016   Pseudo R-squ.:                 0.05122
Time:                        17:58:38   Log-Likelihood:                -1285.4
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
Intercept                                0.298768  0.404939   0.347826
C(W1_C2, Treatment(reference=4))[T.1.0]  0.709631  2.006952   1.193396
C(W1_C2, Treatment(reference=4))[T.2.0]  0.629286  1.159173   0.854079
C(W1_C2, Treatment(reference=4))[T.3.0]  0.423517  0.841344   0.596928
C(W1_C2, Treatment(reference=4))[T.5.0]  0.955003  1.705478   1.276220
C(W1_C2, Treatment(reference=4))[T.6.0]  2.224110  3.813529   2.912338
C(W1_C2, Treatment(reference=4))[T.7.0]  3.433606  9.262302   5.639423
Logistic regression formula: MOST_ANGRY ~ C(W1_C2, Treatment(reference=4)) + BLACK
Optimization terminated successfully.
         Current function value: 0.565255
         Iterations 6
                           Logit Regression Results
==============================================================================
Dep. Variable:             MOST_ANGRY   No. Observations:                 2221
Model:                          Logit   Df Residuals:                     2213
Method:                           MLE   Df Model:                            7
Date:                Wed, 19 Oct 2016   Pseudo R-squ.:                 0.07333
Time:                        17:58:38   Log-Likelihood:                -1255.4
converged:                       True   LL-Null:                       -1354.8
                                        LLR p-value:                 2.177e-39
===========================================================================================================
                                              coef    std err          z      P>|z|      [95.0% Conf. Int.]
-----------------------------------------------------------------------------------------------------------
Intercept                                  -0.6265      0.094     -6.662      0.000        -0.811    -0.442
C(W1_C2, Treatment(reference=4))[T.1.0]     0.2288      0.269      0.850      0.395        -0.299     0.756
C(W1_C2, Treatment(reference=4))[T.2.0]    -0.1324      0.158     -0.838      0.402        -0.442     0.177
C(W1_C2, Treatment(reference=4))[T.3.0]    -0.5409      0.177     -3.053      0.002        -0.888    -0.194
C(W1_C2, Treatment(reference=4))[T.5.0]     0.1612      0.150      1.071      0.284        -0.134     0.456
C(W1_C2, Treatment(reference=4))[T.6.0]     0.9196      0.141      6.539      0.000         0.644     1.195
C(W1_C2, Treatment(reference=4))[T.7.0]     1.5132      0.258      5.874      0.000         1.008     2.018
BLACK                                      -0.7601      0.099     -7.706      0.000        -0.953    -0.567
===========================================================================================================
                                         Lower CI  Upper CI  OddsRatio
Intercept                                0.444514  0.642655   0.534480
C(W1_C2, Treatment(reference=4))[T.1.0]  0.741729  2.130490   1.257079
C(W1_C2, Treatment(reference=4))[T.2.0]  0.642820  1.193749   0.875994
C(W1_C2, Treatment(reference=4))[T.3.0]  0.411467  0.823926   0.582253
C(W1_C2, Treatment(reference=4))[T.5.0]  0.874824  1.577921   1.174906
C(W1_C2, Treatment(reference=4))[T.6.0]  1.904023  3.304199   2.508240
C(W1_C2, Treatment(reference=4))[T.7.0]  2.740974  7.523493   4.541112
BLACK                                    0.385396  0.567331   0.467597
```

# Program
```
import numpy as np
import pandas as pd
import seaborn
import statsmodels.formula.api as smf

# Predict MOST_ANGRY with logistic regression using POLITICAL_SPECTRUM and ETHNICITY

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

# Explanatory variable
ETHNICITY = 'PPETHM'
ETHNICITY_Q = """Race / Ethnicity
1 White, Non-Hispanic
2 Black, Non-Hispanic
3 Other, Non-Hispanic
4 Hispanic
5 2+ Races, Non-Hispanic"""

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
    crosstab = pd.crosstab(data[attr1], data[attr2])
    relative_crosstab = crosstab.apply(lambda r: 100 * r / r.sum(), axis=1)
    print('Counts')
    print(crosstab)
    print('Percentages')
    print(relative_crosstab)
    return crosstab, relative_crosstab

ool_raw = pd.read_csv('../data/ool_pds.csv')[[POLITICAL_SPECTRUM, ETHNICITY, ANGER]]

print('Define MOST_ANGRY as respondents that are Extremely or Very Angry.')
ool_raw['MOST_ANGRY'] = ool_raw.apply(most_angry, axis=1)

ool_raw['BLACK'] = (ool_raw[ETHNICITY] == 2).map({True: 1, False: 0})

prepare_numeric(ool_raw, 'MOST_ANGRY')
prepare_numeric(ool_raw, POLITICAL_SPECTRUM)
prepare_numeric(ool_raw, ETHNICITY)
prepare_numeric(ool_raw, ANGER)

# Create CHILD_BLACK_X binary columns
# ool_raw = ool_raw[ ool_raw[CHILD_BLACK] != -1 ]
# racial_outlook = pd.get_dummies(ool_raw[CHILD_BLACK], prefix='CHILD_BLACK')
# ool_raw = pd.concat([ool_raw, racial_outlook], axis=1)

ool = ool_raw.dropna()
print('Data ready %s' % (ool.shape, ))
print(ool.head())

summarize(ool, 'MOST_ANGRY', ANGER_Q)
crosstab_summarize(ool, POLITICAL_SPECTRUM, ANGER, 'Anger and political spectrum among americans')

def regres(formula):
    print('Logistic regression formula: %s' % formula)
    regression = smf.logit(formula, data=ool).fit()
    print(regression.summary())
    conf_int = regression.conf_int()
    conf_int['OddsRatio'] = regression.params
    conf_int.columns = ['Lower CI', 'Upper CI', 'OddsRatio']
    print(np.exp(conf_int))

# Don't use a dummy variable for every single category to avoid the dummy variable trap
# where perfect multicollinearity occurs. Using C() in the formula does this automatically.
# Use category 4, Moderate; middle of the road, as the baseline.
# Understand P > |z| with http://logisticregressionanalysis.com/1577-what-are-z-values-in-logistic-regression/
regres("MOST_ANGRY ~ C(%s, Treatment(reference=4))" % (POLITICAL_SPECTRUM))

# Does the oversampling of black americans moderate the relationship?
regres("MOST_ANGRY ~ C(%s, Treatment(reference=4)) + BLACK" % (POLITICAL_SPECTRUM))
```
