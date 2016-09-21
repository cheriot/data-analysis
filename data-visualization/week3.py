# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 13:50:02 2016

@author: cheriot
"""

import numpy
import pandas

ool = pandas.read_csv('../data/ool_pds.csv', low_memory=False)

print('Outlook on Life Surveys, 2012')
print('Count of rows %d' % len(ool))
print('Count of columns %d' % len(ool.columns))

ETHNICITY = 'PPETHM'
ETHNICITY_Q = """Race / Ethnicity
1 White, Non-Hispanic
2 Black, Non-Hispanic
3 Other, Non-Hispanic
4 Hispanic
5 2+ Races, Non-Hispanic"""

ANGER = 'W1_B4'
ANGER_Q = """Generally speaking, how angry do you feel about the way things are going in the
country these days?
-1 Refused
1  Extremely angry
2  Very angry
3  Somewhat angry
4  A little angry
5  Not angry at all"""

GENDER = 'PPGENDER'
GENDER_Q = """Gender
1 Male
2 Female"""

GO_BLACK = 'W1_E5_1'
GO_BLACK_Q = """[African/African American/Black] Which racial and ethnic groups would you or
have you dated?
0 No
1 Yes"""

ATTRACT_BLACK = 'W1_E61_A'
ATTRACT_BLACK_Q = """[African/African American/Black: They are physically attractive] How do you
rate each of the following groups on these characteristics?
1 Agree Strongly
2 Agree Somewhat
3 Disagree Somewhat"""

APPROVE_BLACK = 'W1_E61_B'
APPROVE_BLACK_Q = """[African/African American/Black: My family, friends, relatives would not approve]
How do you rate each of the following groups on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly"""

CHILD_BLACK = 'W1_E61_C'
CHILD_BLACK_Q =  """[African/African American/Black: I have concerns about having bi-racial/ethnic children]
How do you rate each of the following groups
on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly"""

APPROVE_OBAMA = 'W1_A12'
APPROVE_OBAMA_Q = """Do you approve or disapprove of the way Barack Obama is handling his job as President?
-1 Refused
1  Approve
2  Disapprove
"""

def prepareNumeric(data, attr):
    data[attr] = pandas.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, numpy.nan)

prepareNumeric(ool, ANGER)
prepareNumeric(ool, CHILD_BLACK)
prepareNumeric(ool, APPROVE_OBAMA)

whites = ool[(ool[ETHNICITY] == 1)].copy()
print('Limiting to %d responses from white Americans' % len(whites))

print('Define IN_EX_CLUSIVE (inclusive vs exclusive) by views on mixed race children.')
def inclusive_or_exclusive(row):
    if row[CHILD_BLACK] == 1 or row[CHILD_BLACK] == 2:
        return 'exclusive'
    elif row[CHILD_BLACK] == 3 or row[CHILD_BLACK] == 4:
        return 'inclusive'
    else:
        numpy.nan
whites['IN_EX_CLUSIVE'] = whites.apply(inclusive_or_exclusive, axis=1)

print('Definte MOST_ANGRY as respondants that are Extremely or Very Angry.')
def most_angry(row):
    # 1: Extremely or Very Angry
    # 0: Somewhat, A little, or Not Angry
    return row[ANGER] == 1 or row[ANGER] == 2
whites['MOST_ANGRY'] = whites.apply(most_angry, axis=1)

def print_divider():
    print('\n\n' + '-'*75)

def summarize(data, attr, desc):
    counts = data.groupby(attr, sort=False).size()
    relative = counts * 100 / len(data)
    print_divider()
    print(desc)
    print('Response counts:')
    print(counts)
    print('Response percentages:')
    print(relative)

summarize(whites, ANGER, ANGER_Q)
summarize(whites, CHILD_BLACK, CHILD_BLACK_Q)
summarize(whites, 'IN_EX_CLUSIVE', 'Inclusive vs Exclusive Whites')
summarize(whites, 'MOST_ANGRY', 'Extremely and Very Angry Americans compared to less angry Americans.')

crosstab = pandas.crosstab([whites['IN_EX_CLUSIVE'], whites['MOST_ANGRY']], whites[APPROVE_OBAMA])
normalized_crosstab = crosstab.apply(lambda r: 100*r/r.sum(), axis=1)
print_divider()
print('Break down President Obama\'s approval rating by IN_EX_CLUSIVE and MOST_ANGRY.')
print('(Within %s: 1 is approve, 2 is disapprove)' % APPROVE_OBAMA)
print('Counts')
print(crosstab)
print('Percentages')
print(normalized_crosstab)

print_divider()
print('Comparison of Anger among Inclusive and Exclusive white Americans.')
crosstab_in_ex_anger = pandas.crosstab(whites['IN_EX_CLUSIVE'], whites[ANGER])
relative_crosstab_in_ex_anger = crosstab_in_ex_anger.apply(lambda r: 100*r/r.sum(), axis=1)
print('Counts')
print(crosstab_in_ex_anger)
print('Percentages')
print(relative_crosstab_in_ex_anger)

