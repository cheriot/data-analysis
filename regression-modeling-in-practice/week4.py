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
# Understand P > |z| with http://logisticregressionanalysis.com/1577-what-are-z-values-in-logistic-regression/
formula = "MOST_ANGRY ~ C(%s, Treatment(reference=4))" % (POLITICAL_SPECTRUM)
regression = smf.logit(formula, data=ool).fit()
print(regression.summary())
conf_int = regression.conf_int()
conf_int['OddsRatio'] = regression.params
conf_int.columns = ['Lower CI', 'Upper CI', 'OddsRatio']
print(numpy.exp(conf_int))
