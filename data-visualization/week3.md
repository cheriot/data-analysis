# Summary of Week 3
Respondants were asked about their views on biracial children, anger at the direction of the country, and their opinion on President Obama. I've limited the dataset to white Americans to examine the feelings of voters to the first President that looks different from them.

Little data is lost from non-responses. The highest among the questions examined is 5.5% for
the question on biracial children, which may reflect the sensitive nature of the topic.

I've created two new columns in the data.
* **IN_EX_CLUSIVE**
  * Based on responses to "[African/African American/Black: I have concerns about having bi-racial/ethnic children] How do you rate each of the following groups on these characteristics?"
  * **exclusive** Respondants that are concerned by the idea of having biracial children.
  * **inclusive** Respondants that are NOT concerned by the idea of having biracial children.
* **MOST_ANGRY**
  * Based on responses to "Generally speaking, how angry do you feel about the way things are going in the country these days?"
  * **True** Respondants that are "Extremely" or "Very" Angry
  * **False** Respondants that are "Somewhat", "A little", or "Not at all" Angry

See the program output for univariate descriptions of each column discussed.

#### Break down President Obama's approval rating by IN_EX_CLUSIVE and MOST_ANGRY.

Approve of Obama |         |    Yes | No
---|---|---|---
IN_EX_CLUSIVE | MOST_ANGRY |        |
exclusive     |  False     |     80 | 88
              |  True      |     29 | 146
inclusive     |  False     |    160 | 111
              |  True      |     40 | 108

Approve of Obama |         |        Yes | No
---|---|---|---
IN_EX_CLUSIVE | MOST_ANGRY |       | 
exclusive     | False      | 47.6%  | 52.4%
              | True       | 16.6%  | 83.4%
inclusive     | False      | 59.0%  | 41.0%
              | True       | 27.0%  | 73.0%

President Obama is most popular with inclusive, less angry white Americans (59.0%) and least
popular with exclusive, angry white Americans (16.6%). Digging into the more finely grained
categories of anger, we see that all categories are affected by inclusive/exclusive. It's as
if the entire curve is shifted.

### Anger Comparison (Percentage)
W1_B4          | Extremely Angry | Very Angry        | Somewhat Angry | A Little Angry | Not At All Angry
            ---|---:|---:|---:|---:|---:|
IN_EX_CLUSIVE  |
exclusive      | 22.0% | 29.2% | 28.6% | 16.2%  | 4.0%
inclusive      | 13.0% | 22.7% | 34.4% | 23.0%  | 6.9%

# Program Output
```
Outlook on Life Surveys, 2012
Count of rows 2294
Count of columns 436
Limiting to 814 responses from white Americans
Define IN_EX_CLUSIVE (inclusive vs exclusive) by views on mixed race children.
Definte MOST_ANGRY as respondants that are Extremely or Very Angry.


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
3.0    256
1.0    140
4.0    160
2.0    206
5.0     44
dtype: int64
Response percentages:
W1_B4
3.0    31.449631
1.0    17.199017
4.0    19.656020
2.0    25.307125
5.0     5.405405
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
1.0    140
3.0    178
4.0    245
2.0    206
dtype: int64
Response percentages:
W1_E61_C
1.0    17.199017
3.0    21.867322
4.0    30.098280
2.0    25.307125
dtype: float64


---------------------------------------------------------------------------
Inclusive vs Exclusive Whites
Response counts:
IN_EX_CLUSIVE
exclusive    346
inclusive    423
dtype: int64
Response percentages:
IN_EX_CLUSIVE
exclusive    42.506143
inclusive    51.965602
dtype: float64


---------------------------------------------------------------------------
Extremely and Very Angry Americans compared to less angry Americans.
Response counts:
MOST_ANGRY
False    468
True     346
dtype: int64
Response percentages:
MOST_ANGRY
False    57.493857
True     42.506143
dtype: float64


---------------------------------------------------------------------------
Break down President Obama's approval rating by IN_EX_CLUSIVE and MOST_ANGRY.
(Within W1_A12: 1 is approve, 2 is disapprove)
Counts
W1_A12                    1.0  2.0
IN_EX_CLUSIVE MOST_ANGRY
exclusive     False        80   88
              True         29  146
inclusive     False       160  111
              True         40  108
Percentages
W1_A12                          1.0        2.0
IN_EX_CLUSIVE MOST_ANGRY
exclusive     False       47.619048  52.380952
              True        16.571429  83.428571
inclusive     False       59.040590  40.959410
              True        27.027027  72.972973


---------------------------------------------------------------------------
Comparison of Anger among Inclusive and Exclusive white Americans.
Counts
W1_B4          1.0  2.0  3.0  4.0  5.0
IN_EX_CLUSIVE
exclusive       76  101   99   56   14
inclusive       55   96  145   97   29
Percentages
W1_B4                1.0        2.0        3.0        4.0       5.0
IN_EX_CLUSIVE
exclusive      21.965318  29.190751  28.612717  16.184971  4.046243
inclusive      13.033175  22.748815  34.360190  22.985782  6.872038
```

# Program
```
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
```
