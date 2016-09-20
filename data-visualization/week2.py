# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 13:50:02 2016

@author: cheriot
"""

import pandas
import numpy


ool = pandas.read_csv('../data/ool_pds.csv', low_memory=False)

print('Outlook on Life Surveys, 2012')
print('Count of rows %d' % len(ool))
print('Count of columns %d' % len(ool.columns))

def summarize(attr, desc):
    ool[attr] = pandas.to_numeric(ool[attr], errors='coerce')
    counts = ool.groupby(attr).size()
    relative = counts * 100 / len(ool)
    print('\n' + '-'*75)
    print(desc)
    print('Response counts:')
    print(counts)
    print('Response percentages:')
    print(relative)

ANGER = 'W1_B4'
ANGER_Q = """Generally speaking, how angry do you feel about the way things are going in the
country these days?
-1 Refused
1  Extremely angry
2  Very angry
3  Somewhat angry
4  A little angry
5  Not angry at all"""
summarize(ANGER, ANGER_Q)

ETHNICITY = 'PPETHM'
ETHNICITY_Q = """Race / Ethnicity
1 White, Non-Hispanic
2 Black, Non-Hispanic
3 Other, Non-Hispanic
4 Hispanic
5 2+ Races, Non-Hispanic"""
summarize(ETHNICITY, ETHNICITY_Q)

GENDER = 'PPGENDER'
GENDER_Q = """Gender
1 Male
2 Female"""
# summarize(GENDER, GENDER_Q)

GO_BLACK = 'W1_E5_1'
GO_BLACK_Q = """[African/African American/Black] Which racial and ethnic groups would you or
have you dated?
0 No
1 Yes"""
# summarize(GO_BLACK, GO_BLACK_Q)

ATTRACT_BLACK = 'W1_E61_A'
ATTRACT_BLACK_Q = """[African/African American/Black: They are physically attractive] How do you
rate each of the following groups on these characteristics?
1 Agree Strongly
2 Agree Somewhat
3 Disagree Somewhat"""
# summarize(ATTRACT_BLACK, ATTRACT_BLACK_Q)

APPROVE_BLACK = 'W1_E61_B'
APPROVE_BLACK_Q = """[African/African American/Black: My family, friends, relatives would not approve]
How do you rate each of the following groups on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly"""
summarize(APPROVE_BLACK, APPROVE_BLACK_Q)

CHILD_BLACK = 'W1_E61_C'
CHILD_BLACK_Q =  """[African/African American/Black: I have concerns about having bi-racial/ethnic children]
How do you rate each of the following groups
on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly"""
summarize(CHILD_BLACK, CHILD_BLACK_Q)

USE_BLACK = 'W1_E61_D'
USE_BLACK_Q = """[African/African American/Black: I would only want to date this group for sexual
reasons rather than for a serious or potential marital relationship] How do you
rate each of the following groups on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly"""
# summarize(USE_BLACK, USE_BLACK_Q)
