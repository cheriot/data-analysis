# Summary of Week 2
The program below summarizes anger among white americans. It then splits white americans
into two groups based on how they feel about biracial children and summarizes the amount
of anger in each group.

Little data is lost from non-responses. The highest among the questions examined is 5.5% for
the question on biracial children, which may reflect the sensitive nature of the topic.

In the first table below, there's a large number of Americans in each of the inclusive and exclusive
categories. In the second table, we see how there the frequency of anger shifts between the two groups.
For example, 22% of exclusive Americans are Extremely Angry while only 14% of inlclusive Americans are.
Is this difference statistically significant?

### [African/African American/Black: I have concerns about having bi-racial/ethnic children]

| Response         | Count | PercentofWhites | CategoryAssigned |
|------------------|----:|----------:|----------:|
|Agree Strongly    | 140 | 17.2 | exclusive |
|Agree Somewhat    | 206 | 25.3 | exclusive |
|Disagree Somewhat | 178 | 21.9 | inclusive |
|Disagree Strongly | 245 | 30.1 | inclusive |

### Anger Comparison (Percentage)
|                           | Extremely Angry    | Very Angry     | Somewhat Angry | A Little Angry | Not At All Angry|
| :-------------------------| ------------------:| --------------:| --------------:| --------------:| ---------------:|
| Inclusive White Americans | 13.0               |     22.7       | 34.3           | 22.9           | 6.9             |
| Exclusive White Americans | 22.0               |     29.2       | 28.6           | 16.2           | 4.0             |
*See program output below for the complete data.*


# Program Output
```
Outlook on Life Surveys, 2012
Count of rows 2294
Count of columns 436
Limiting to 814 responses from white Americans

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
-1      8
 1    140
 2    206
 3    256
 4    160
 5     44
dtype: int64
Response percentages:
W1_B4
-1     0.982801
 1    17.199017
 2    25.307125
 3    31.449631
 4    19.656020
 5     5.405405
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
-1     45
 1    140
 2    206
 3    178
 4    245
dtype: int64
Response percentages:
W1_E61_C
-1     5.528256
 1    17.199017
 2    25.307125
 3    21.867322
 4    30.098280
dtype: float64

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
1     76
2    101
3     99
4     56
5     14
dtype: int64
Response percentages:
W1_B4
1    21.965318
2    29.190751
3    28.612717
4    16.184971
5     4.046243
dtype: float64

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
-1      1
 1     55
 2     96
 3    145
 4     97
 5     29
dtype: int64
Response percentages:
W1_B4
-1     0.236407
 1    13.002364
 2    22.695035
 3    34.278960
 4    22.931442
 5     6.855792
dtype: float64
```

# Program
Source code is available at [week2.py](week2.py). I've copied it here for convenience.
```
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

whites = ool[(ool[ETHNICITY] == 1)].copy()
print('Limiting to %d responses from white Americans' % len(whites))
summarize(whites, ANGER, ANGER_Q)
summarize(whites, CHILD_BLACK, CHILD_BLACK_Q)
exclusive_whites = whites[(whites[CHILD_BLACK] == 1) | (whites[CHILD_BLACK] == 2)].copy()
inclusive_whites = whites[(whites[CHILD_BLACK] == 3) | (whites[CHILD_BLACK] == 4)].copy()
summarize(exclusive_whites, ANGER, 'Anger among white americans that are concerned about having biracial children.')
summarize(inclusive_whites, ANGER, 'Anger among white americans that are not concerned about having biracial children.')
```
