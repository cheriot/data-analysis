# Program Output
```
Outlook on Life Surveys, 2012
Count of rows 2294
Count of columns 436

---------------------------------------------------------------------------
Generally speaking, how angry do you feel about the way things are going in the
country these days?
-1 Refused
1  Extremely angry
2  Very angry
3  Somewhat angry
4  A little angry
5  Not angry at all
Response counts:
W1_B4
-1     27
 1    243
 2    437
 3    731
 4    555
 5    301
dtype: int64
Response percentages:
W1_B4
-1     1.176983
 1    10.592851
 2    19.049695
 3    31.865737
 4    24.193548
 5    13.121186
dtype: float64

---------------------------------------------------------------------------
Race / Ethnicity
1 White, Non-Hispanic
2 Black, Non-Hispanic
3 Other, Non-Hispanic
4 Hispanic
5 2+ Races, Non-Hispanic
Response counts:
PPETHM
1     814
2    1278
3      46
4     123
5      33
dtype: int64
Response percentages:
PPETHM
1    35.483871
2    55.710549
3     2.005231
4     5.361813
5     1.438535
dtype: float64

---------------------------------------------------------------------------
[African/African American/Black: My family, friends, relatives would not approve]
How do you rate each of the following groups on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly
Response counts:
W1_E61_B
-1      99
 1     229
 2     419
 3     501
 4    1046
dtype: int64
Response percentages:
W1_E61_B
-1     4.315606
 1     9.982563
 2    18.265039
 3    21.839582
 4    45.597210
dtype: float64

---------------------------------------------------------------------------
[African/African American/Black: I have concerns about having bi-racial/ethnic children]
How do you rate each of the following groups
on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly
Response counts:
W1_E61_C
-1     103
 1     214
 2     377
 3     436
 4    1164
dtype: int64
Response percentages:
W1_E61_C
-1     4.489974
 1     9.328684
 2    16.434176
 3    19.006103
 4    50.741064
dtype: float64
```

# Program
Source code is available at [week2.py](week2.py).
```
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
    print('\n' + '-'*80)
    print(desc)
    print('Response counts:')
    print(counts)
    print('Response percentages:')
    print(relative)

ANGER = 'W1_B4'
ANGER_Q = """Generally speaking, how angry do you feel about the way things are going in the country these days?
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

APPROVE_BLACK = 'W1_E61_B'
APPROVE_BLACK_Q = """[African/African American/Black: My family, friends, relatives would not approve] How do you rate each of the following groups on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly"""
summarize(APPROVE_BLACK, APPROVE_BLACK_Q)

CHILD_BLACK = 'W1_E61_C'
CHILD_BLACK_Q = """[African/African American/Black: I have concerns about having bi-racial/ethnic children] How do you rate each of the following groups on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly"""
summarize(CHILD_BLACK, CHILD_BLACK_Q)
```
