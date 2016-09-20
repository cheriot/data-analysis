# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 13:50:02 2016

@author: cheriot
"""

import pandas

ool = pandas.read_csv('../data/ool_pds.csv', low_memory=False)

print('Outlook on Life Surveys, 2012')
print('Count of rows %d' % len(ool))
print('Count of columns %d' % len(ool.columns))

def summarize(data, attr, desc):
    data[attr] = pandas.to_numeric(data[attr], errors='coerce')
    counts = data.groupby(attr).size()
    relative = counts * 100 / len(data)
    print('\n' + '-'*75)
    print(desc)
    print('Response counts:')
    print(counts)
    print('Response percentages:')
    print(relative)

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

whites = ool[(ool[ETHNICITY] == 1)].copy()
print('Limiting to %d responses from white Americans' % len(whites))
summarize(whites, ANGER, ANGER_Q)
summarize(whites, CHILD_BLACK, CHILD_BLACK_Q)
exclusive_whites = whites[(whites[CHILD_BLACK] == 1) | (whites[CHILD_BLACK] == 2)].copy()
inclusive_whites = whites[(whites[CHILD_BLACK] == 3) | (whites[CHILD_BLACK] == 4)].copy()
summarize(exclusive_whites, ANGER, 'Anger among white americans that are concerned about having biracial children.')
summarize(inclusive_whites, ANGER, 'Anger among white americans that are not concerned about having biracial children.')
summarize(whites, APPROVE_OBAMA, APPROVE_OBAMA_Q)
summarize(exclusive_whites, APPROVE_OBAMA, 'Obama job approval among exclusive whites.')
summarize(inclusive_whites, APPROVE_OBAMA, 'Obama job approval among inclusive whites.')