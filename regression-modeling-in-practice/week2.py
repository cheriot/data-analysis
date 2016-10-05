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
