import numpy
import pandas
import seaborn
import scipy.stats
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi

ETHNICITY = 'PPETHM'
ETHNICITY_Q = """Race / Ethnicity
1 White, Non-Hispanic
2 Black, Non-Hispanic
3 Other, Non-Hispanic
4 Hispanic
5 2+ Races, Non-Hispanic"""

CHILD_BLACK = 'W1_E61_C'
CHILD_BLACK_Q = """I have concerns about having bi-racial/ethnic children [African/African American/Black]
How do you rate each of the following groups
on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly"""

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

ool = pandas.read_csv('../data/ool_pds.csv', low_memory=False)

print('Outlook on Life Surveys, 2012')
print('Count of rows %d' % len(ool))
print('Count of columns %d' % len(ool.columns))

whites = ool[(ool[ETHNICITY] == 1)].copy()
print('Limiting to %d responses from white Americans' % len(whites))


def prepareNumeric(data, attr):
    data[attr] = pandas.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, numpy.nan)


prepareNumeric(whites, CHILD_BLACK)
prepareNumeric(whites, ANGER)

print('Define MOST_ANGRY as respondants that are Extremely or Very Angry.')


def most_angry(row):
    # 1: Extremely or Very Angry
    # 0: Somewhat, A little, or Not Angry
    if row[ANGER] == 1 or row[ANGER] == 2:
        return 1
    else:
        return 0


whites['MOST_ANGRY'] = whites.apply(most_angry, axis=1)


def print_divider():
    print('\n\n' + '-' * 75)


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


def as_category(data, attr, names):
    data[attr] = data[attr].astype('category')
    data[attr] = data[attr].cat.rename_categories(names)


summarize(whites, CHILD_BLACK, CHILD_BLACK_Q)
summarize(whites, 'MOST_ANGRY', ANGER_Q)


def chi2test(data, response_attr, explanatory_attr):
    crosstab = pandas.crosstab(data[response_attr], data[explanatory_attr])
    relative_crosstab = crosstab.apply(lambda c: c / c.sum(), axis=0)
    c2t = scipy.stats.chi2_contingency(crosstab)
    print_divider()
    print('Compare %s, %s' % (response_attr, explanatory_attr))
    print(crosstab)
    print(relative_crosstab)
    print(c2t)


# Null Hypothesis: CHILD_BLACK and ANGER are independent variables. No relationship.
# Alternate Hypothesis: CHILD_BLACK and ANGER have a relationship and are not independent.
chi2test(whites, 'MOST_ANGRY', CHILD_BLACK)

CHILD_BLACK_NAMES = ['AgreeStrongly', 'AgreeSomewhat', 'DisagreeSomewhat', 'DisagreeStrongly']
# Post hoc test:
# For each of the explainatory categories, see if they are significantly different.
# CHILD_BLACK, has the values 1, 2, 3, 4
for cat1 in range(1, 5):
    for cat2 in range(cat1 + 1, 5):
        name = 'ChildBlack_%s_%s' % (CHILD_BLACK_NAMES[cat1 - 1], CHILD_BLACK_NAMES[cat2 - 1])
        whites[name] = whites[CHILD_BLACK].map({cat1: cat1, cat2: cat2})
        chi2test(whites, 'MOST_ANGRY', name)
        print('(%s) chi-square, p-value, is the null hypothesis rejected?' % (name))

# Figure sizes in inches. For some reason this does not apply to the factorplot.
seaborn.mpl.rc("figure", figsize=(9, 9))

# Make a pretty picture
as_category(whites, CHILD_BLACK, ['Agree Strongly', 'Agree Somewhat', 'Disagree Somewhat', 'Disagree Strongly'])
as_category(whites, ANGER, ['Extremely Angry', 'Very Angry', 'Somewhat Angry', 'A Little Angry', 'Not At All Angry'])
print_divider()
crosstab = pandas.crosstab(whites[CHILD_BLACK], whites[ANGER])
relative_crosstab = crosstab.apply(lambda r: 100 * r / r.sum(), axis=1)
bar = relative_crosstab.plot(kind='bar', stacked=True)
plt.xlabel('I have concerns about having bi-racial/ethnic children [African/African American/Black]')
plt.ylabel('% White Americans')
plt.title('Generally speaking, how angry do you feel about the way things are going in the country these days?\n')
fig = bar.get_figure()
fig.savefig('ChildBlackAngerStackedBar.png')
