import numpy as np
import pandas as pd
import statsmodels.formula.api as smf 
import statsmodels.stats.multicomp as multi
import seaborn
import matplotlib.pyplot as plt

RATE_BARACK = 'W1_D1'
RATE_BARACK_Q = 'How would you rate [Barack Obama] [0 to 100]'

ETHNICITY = 'PPETHM'
ETHNICITY_Q = """Race / Ethnicity
1 White, Non-Hispanic
2 Black, Non-Hispanic
3 Other, Non-Hispanic
4 Hispanic
5 2+ Races, Non-Hispanic"""


def assign_ethnicity_2(row):
    ethnicity_cat = row[ETHNICITY]
    if ethnicity_cat == 1:
        return 1
    elif ethnicity_cat > 1:
        return 0
    else:
        return np.nan

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


def assign_political_2(row):
    political_cat = row[POLITICAL_SPECTRUM]
    if political_cat < 4:
        return 0 # left of center
    elif political_cat > 4:
        return 1 # right of center
    else:
        return np.nan


def prepare_rate(data, attr):
    data[attr] = pd.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, np.nan)
    data[attr] = data[attr].replace(998, np.nan)


def prepare_numeric_category(data, attr):
    data[attr] = pd.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, np.nan)

ool_raw = pd.read_csv('../data/ool_pds.csv')[[RATE_BARACK, ETHNICITY, POLITICAL_SPECTRUM]]
prepare_numeric_category(ool_raw, ETHNICITY)
prepare_numeric_category(ool_raw, POLITICAL_SPECTRUM)
prepare_rate(ool_raw, RATE_BARACK)
ool_raw['ETHNICITY_2'] = ool_raw.apply(assign_ethnicity_2, axis=1)
ool_raw['POLITICAL_2'] = ool_raw.apply(assign_political_2, axis=1)
ool = ool_raw.dropna()
print('Data ready. %s' % ((ool.shape,)))
print(ool.head())


def summarize(data, attr, desc):
    counts = data.groupby(attr, sort=False).size()
    relative = counts * 100 / len(data)
    print('-'*80)
    print(desc)
    print('Response counts:')
    print(counts)
    print('Response percentages:')
    print(relative)

# Univariate overview.
summarize(ool, ETHNICITY, ETHNICITY_Q)
summarize(ool, 'ETHNICITY_2', 'Ethnicity by 1 white and 0 non-white.')
summarize(ool, POLITICAL_SPECTRUM, POLITICAL_SPECTRUM_Q)
summarize(ool, 'POLITICAL_2', 'Political spectrum by 0 liberal and 1 conservative.')
print(ool[RATE_BARACK].describe())
rating_boxplot = seaborn.boxplot(y=RATE_BARACK, data=ool)
plt.ylabel('Rating')
plt.title('American\'s rating of Presitent Obama')
plt.show()
rating_boxplot.get_figure().savefig('RATE_BARACK-boxplot.png')

# Bivariate overview.
print(pd.crosstab(ool['ETHNICITY_2'], ool['POLITICAL_2']))


# Obama's rating by race. Obama's rating by race for Dem vs Rep.
def investigate_rating_by_ethnicity(data, desc):
    rating_by_ethnicity_boxplot = seaborn.boxplot(x='ETHNICITY_2', y=RATE_BARACK, data=data)
    plt.xlabel('Non-White vs White')
    plt.ylabel('Rating')
    plt.title('%s rating of Presitent Obama' % desc)
    plt.show()
    rating_by_ethnicity_boxplot.get_figure().savefig('%s-boxplot.png' % desc)
    print(data.groupby('ETHNICITY_2')[RATE_BARACK].describe())
    regression = smf.ols(formula='%s ~ C(ETHNICITY_2)' % RATE_BARACK, data=data).fit()
    print(regression.summary())

# 1. Regression RATING_OBAMA explained by ETHNICITY.
#    * means per ETHNICITY
#    * stdev per ETHNICITY
investigate_rating_by_ethnicity(ool, 'FullPopulation')

# 2. Subset by party affiliation.
liberal_ool = ool[ ool['POLITICAL_2'] == 0 ]
conservative_ool = ool[ ool['POLITICAL_2'] == 1 ]

# 3. Show that the relationship is different in each subset.
#    * repeat step 1
investigate_rating_by_ethnicity(liberal_ool, 'Liberal')
investigate_rating_by_ethnicity(conservative_ool, 'Conservative')

# Now compare white liberals and white conservatives.
white_ool = ool[ ool['ETHNICITY_2'] == 1 ]
rating_by_political_2_among_whites_boxplot = seaborn.boxplot(x='POLITICAL_2', y=RATE_BARACK, data=white_ool)
plt.xlabel('Liberal vs Conservative')
plt.ylabel('Rating')
plt.title('Rating of President Obama by White Americans')
rating_by_political_2_among_whites_boxplot.get_figure().savefig('white-rating-by-political.png')
print(white_ool.groupby('POLITICAL_2')[RATE_BARACK].describe())
regression = smf.ols(formula='%s ~ C(POLITICAL_2)' % RATE_BARACK, data=white_ool).fit()
print(regression.summary())
