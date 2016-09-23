import numpy
import pandas
import seaborn
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi

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

CHILD_BLACK = 'W1_E61_C'
CHILD_BLACK_Q =  """I have concerns about having bi-racial/ethnic children [African/African American/Black]
How do you rate each of the following groups
on these characteristics?
-1 Refused
1  Agree Strongly
2  Agree Somewhat
3  Disagree Somewhat
4  Disagree Strongly"""

RATE_MICHELLE = 'W1_D3'
RATE_MICHELLE_Q = '[Michelle Obama] How would you rate'

def prepareNumeric(data, attr):
    data[attr] = pandas.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, numpy.nan)

prepareNumeric(ool, CHILD_BLACK)
prepareNumeric(ool, RATE_MICHELLE)
ool[RATE_MICHELLE] = ool[RATE_MICHELLE].replace(998, numpy.nan)

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

def crosstab_summarize(data, attr1, attr2, title):
    print_divider()
    print('%s (crosstab %s * %s).' % (title, attr1, attr2))
    crosstab = pandas.crosstab(data[attr1], data[attr2])
    relative_crosstab = crosstab.apply(lambda r: 100*r/r.sum(), axis=1)
    print('Counts')
    print(crosstab)
    print('Percentages')
    print(relative_crosstab)

def as_category(data, attr, names):
  data[attr] = data[attr].astype('category')
  data[attr] = data[attr].cat.rename_categories(names)

# Figure sizes in inches. For some reason this does not apply to the factorplot.
seaborn.mpl.rc("figure", figsize=(7,7))

as_category(whites, CHILD_BLACK, ["Agree Strongly", "Agree Somewhat", "Disagree Somewhat", "Disagree Strongly"])
seaborn.countplot(x=CHILD_BLACK, data=whites)
plt.title('I have concerns about having bi-racial/ethnic children (African/African American/Black)\n')
plt.xlabel('')
plt.ylabel('# White Americans')
plt.show()

seaborn.boxplot(y=RATE_MICHELLE, data=whites);
plt.ylabel('Rating')
plt.title('Rating of Michelle Obama by White Americans\n')
plt.show()

seaborn.boxplot(x='IN_EX_CLUSIVE', y=RATE_MICHELLE, data=whites);
plt.ylabel('Rating')
plt.title('Rating of Michelle Obama by White Americans\n')
plt.show()

model1 = smf.ols(formula='%s ~ C(%s)' % (RATE_MICHELLE, 'IN_EX_CLUSIVE'), data=whites)
results1 = model1.fit()
print(results1.summary())

seaborn.factorplot(x=CHILD_BLACK, y=RATE_MICHELLE, data=whites, kind='bar', ci=None, size=8)
plt.xlabel('I have concerns about having bi-racial/ethnic children (African/African American/Black)')
plt.ylabel('Rating of Michelle Obama')
plt.title('White American\'s Rating of Michell Obama and Concerns of Biracial Children')
plt.show()

seaborn.boxplot(x=CHILD_BLACK, y=RATE_MICHELLE, data=whites);
plt.xlabel('I have concerns about having bi-racial/ethnic children (African/African American/Black)')
plt.ylabel('Rating')
plt.title('Rating of Michelle Obama by White Americans\n')
plt.show()

whites = whites[[RATE_MICHELLE, CHILD_BLACK]].dropna()
mc1 = multi.MultiComparison(whites[RATE_MICHELLE], whites[CHILD_BLACK])
res1 = mc1.tukeyhsd()
print(res1.summary())
