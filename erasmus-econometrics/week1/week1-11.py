import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

# Dataset TrainExer11 contains survey outcomes of a travel agency that wishes to improve recommendation strategies
# for its clients. The dataset contains 26 observations on age and average daily expenditures during holidays.

data = pd.read_csv('./TrainExer11.txt', low_memory=False, delimiter='\t')
print(data.head())

# (a) Make two histograms, one of expenditures and the other of age. Make also a scatter
# diagram with expenditures on the vertical axis versus age on the horizontal axis.
seaborn.distplot(data['Age'], kde=False);
plt.show()

seaborn.distplot(data['Expenditures'], kde=False)
plt.show()

scatter_plot = seaborn.regplot(x=data['Age'], y=data['Expenditures'], fit_reg=False, data=data)
plt.title('Travel Expenses')
plt.show()

# (b) In what respect do the data in this scatter diagram look different from the case of
# the sales and price data discussed in the lecture?
# Answer: There are two groups, each with a somewhat strong linear relationship, but combined there is only a weak relationship.

# (c) Propose a method to analyze these data in a way that assists the travel agent in making
# recommendations to future clients.
# The scatter diagram indicates two groups of clients. Younger clients spend more than older
# ones. Further, expenditures tend to increase with age for younger clients, whereas the
# pattern is less clear for older clients.
# Split customers into two groups based on age 40. For customers that have a previous data point
# in the same group, sell them something a little bit more expensive.

# (d) Compute the sample mean of expenditures of all 26 clients.
print('Mean of all expenditures: %s' % data['Expenditures'].mean())

# (e) Compute two sample means of expenditures, one for clients of age forty or more and
# the other for clients of age below forty.
over40 = data[(data['Age'] >= 40)]
print('Over 40 expenditure mean is %s.' % over40['Expenditures'].mean())
under40 = data[(data['Age'] < 40)]
print('Under 40 expenditure mean is %s.' % under40['Expenditures'].mean())

# (f) What daily expenditures would you predict for a new client of fifty years old? And
# for someone who is twenty-five years old?
def regres(subset, desc):
  regression = smf.ols('Expenditures ~ Age', data=subset).fit()
  print(regression.summary())
  scatter_plot = seaborn.regplot(x=subset['Age'], y=subset['Expenditures'], fit_reg=True, data=subset)
  plt.title('%s Travel Expenses' % desc)
  plt.show()
  return regression

over40model = regres(over40, 'Over 40')
under40model = regres(under40, 'Under 40')
def predict(model, age):
  return age * model.params['Age'] + model.params['Intercept']
print('Prediction for Age 25 is %s' % (predict(under40model, 25)))
print('Prediction for Age 50 is %s' % (predict(over40model, 50)))
