import pandas as pd
import numpy as np
import seaborn
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
import sklearn.metrics
from sklearn.model_selection import cross_val_score
from sklearn import tree
from io import StringIO
import pydotplus

ANGER = 'W1_B4'
ANGER_Q = """Generally speaking, how angry do you feel about the way things are going in the
country these days?
-1 Refused
1  Extremely angry
2  Very angry
3  Somewhat angry
4  A little angry
5  Not angry at all"""


def most_angry(row):
    # 1: Extremely or Very Angry
    # 0: Somewhat, A little, or Not Angry
    if row[ANGER] == 1 or row[ANGER] == 2:
        return 1
    else:
        return 0


def collapse_anger(row):
    anger_cat = row[ANGER]
    if anger_cat <= 2:
        return 0
    elif anger_cat == 3:
        return 1
    else:
        return 2

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

INCOME = 'W1_P20'
INCOME_Q = """Which of the following income groups includes YOUR personal annual income (Do not include the income of other members of your household)?
1  Less than $5,000       261   11.4 %
2  $5,000 to $7,499        72    3.1 %
3  $7,500 to $9,999        58    2.5 %
4  $10,000 to $12,499     107    4.7 %
5  $12,500 to $14,999      87    3.8 %
6  $15,000 to $19,999      91    4.0 %
7  $20,000 to $24,999     149    6.5 %
8  $25,000 to $29,999     127    5.5 %
9  $30,000 to $34,999     118    5.1 %
10 $35,000 to $39,999     107    4.7 %
11 $40,000 to $49,999     174    7.6 %
12 $50,000 to $59,999     166    7.2 %
13 $60,000 to $74,999     185    8.1 %
14 $75,000 to $84,999      86    3.7 %
15 $85,000 to $99,999      81    3.5 %
16 $100,000 to $124,999   114    5.0 %
17 $125,000 to $149,999    38    1.7 %
18 $150,000 to $174,999    44    1.9 %
19 $175,000 or more        27    1.2 %
-1 Refused                202    8.8 %
"""


def collapse_income(row):
    income_cat = row[INCOME]
    if income_cat <= 7:
        return 0
    elif income_cat <= 10:
        return 1
    elif income_cat <= 14:
        return 2
    else:
        return 3

AGE = 'PPAGECAT'
AGE_Q = """Age - 7 Categories
1 18-24   237   10.3 %
2 25-34   289   12.6 %
3 35-44   360   15.7 %
4 45-54   457   19.9 %
5 55-64   514   22.4 %
6 65-74   329   14.3 %
7 75+     108   4.7 %
99 Under   18   0 0.0 %
"""


def collapse_age(row):
    age_cat = row[AGE]
    if age_cat <= 2:
        return 0
    elif age_cat <= 4:
        return 1
    else:
        return 2

EDUCATION = 'PPEDUCAT'
EDUCATION_Q = """Education (Categorical)
1 Less than high school         219  9.5 %
2 High school                   700 30.5%
3 Some college                  682 29.7%
4 Bachelor's degree or higher   693 30.2%
"""

ETHNICITY = 'PPETHM'
ETHNICITY_Q = """Race / Ethnicity
1 White, Non-Hispanic
2 Black, Non-Hispanic
3 Other, Non-Hispanic
4 Hispanic
5 2+ Races, Non-Hispanic"""

GENDER = 'PPGENDER'
GENDER_Q = """Gender
1 Male 1032 45.0 %
2 Female 1262 55.0 %
"""


def summarize(data, attr, desc):
    # counts = data.groupby(attr, sort=False).size()
    # relative = counts * 100 / len(data)
    # print('-' * 80)
    # print(desc)
    # print('Response counts:')
    # print(counts)
    # print('Response percentages:')
    # print(relative)
    count_plot = seaborn.countplot(x=attr, data=data)
    plt.title(desc.split('\n')[0])
    plt.xlabel(attr)
    plt.ylabel('Count of Americans')
    plt.show()
    count_plot.get_figure().savefig('%s-countplot.png' % attr)


def prepare_numeric_category(data, attr):
    data[attr] = pd.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, np.nan)
    data[attr] = data[attr].astype('category')


# Load and transform data
ool = pd.read_csv('../data/ool_pds.csv', low_memory=False)
print('Outlook on Life Surveys, 2012 %s' % (ool.shape,))
prepare_numeric_category(ool, POLITICAL_SPECTRUM)
prepare_numeric_category(ool, INCOME)
prepare_numeric_category(ool, AGE)
prepare_numeric_category(ool, EDUCATION)
prepare_numeric_category(ool, GENDER)
prepare_numeric_category(ool, ANGER)

print('Define MOST_ANGRY as respondents that are Extremely or Very Angry.')
ool['MOST_ANGRY'] = ool.apply(most_angry, axis=1)
prepare_numeric_category(ool, 'MOST_ANGRY')

print('Define ANGER_3 as the ANGER column divided into 3 categories.')
ool['ANGER_3'] = ool.apply(collapse_anger, axis=1)
prepare_numeric_category(ool, 'ANGER_3')

print('Define INCOME_4 as the INCOME column divided into 4 categories.')
ool['INCOME_4'] = ool.apply(collapse_income, axis=1)
prepare_numeric_category(ool, 'INCOME_4')

print('Define AGE_3 as the AGE column divided into 3 categories.')
ool['AGE_3'] = ool.apply(collapse_age, axis=1)
prepare_numeric_category(ool, 'AGE_3')

# Univariate summaries
summarize(ool, INCOME, INCOME_Q)
summarize(ool, AGE, AGE_Q)
summarize(ool, 'AGE_3', '3 category age')
summarize(ool, ANGER, ANGER_Q)
summarize(ool, POLITICAL_SPECTRUM, POLITICAL_SPECTRUM_Q)
summarize(ool, EDUCATION, EDUCATION_Q)
summarize(ool, GENDER, GENDER_Q)
summarize(ool, ETHNICITY, ETHNICITY_Q)
summarize(ool, 'INCOME_4', '4 category income')
summarize(ool, 'MOST_ANGRY', '2 category anger')

predictor_names = ['PoliticalSpectrum', 'Education', 'Gender', 'Ethnicity', 'Income_4']
predictor_cols = [POLITICAL_SPECTRUM, EDUCATION, GENDER, ETHNICITY, 'INCOME_4']
target_cols = ['MOST_ANGRY']
target_class_names = ['LessAngry', 'MostAngry']
ool = ool[predictor_cols + target_cols].dropna()
print('Data ready %s.' % (ool.shape,))
print(ool.head())
print(ool.dtypes)
print(ool.describe())

predictors = ool[predictor_cols]
targets = ool[target_cols]
pred_train, pred_test, tar_train, tar_test  =   train_test_split(predictors, targets, test_size=.4)

assert pred_train.shape[0] == tar_train.shape[0]
assert pred_test.shape[0] == tar_test.shape[0]

# Train decision tree
classifier=DecisionTreeClassifier(max_depth=4, min_samples_leaf=20, class_weight='balanced')
classifier=classifier.fit(pred_train,tar_train)
predictions=classifier.predict(pred_test)

# What do these results mean?
print('A confusion matrix C is such that C_{i, j} is equal to the number of observations known to be in group i but predicted to be in group j.')
print('Correct results are along the top-left to bottom-right diagonal in the confusion matrix.')
print('False positives are the top-right.')
print('False negatives are the bottom-left.')
print(target_class_names)
print(sklearn.metrics.confusion_matrix(tar_test,predictions) / predictions.shape[0] * 100)
print(sklearn.metrics.accuracy_score(tar_test, predictions))
# Why does this want a Series instead of a DataFrame for the last parameter?
# What does cross_val_score really calculate?
print(cross_val_score(classifier, pred_test, tar_test[target_cols[0]]))

# Visual decision tree
out = StringIO()
tree.export_graphviz(classifier, out_file=out, feature_names=predictor_names, class_names=target_class_names, filled=True, rounded=True)
graph=pydotplus.graph_from_dot_data(out.getvalue())
with open('political-decision-tree2.png', 'wb') as f:
    f.write(graph.create_png())

print('Done. Check political-decision-tree.png')
