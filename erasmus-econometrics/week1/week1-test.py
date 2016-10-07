import pandas as pd
import seaborn
import matplotlib.pyplot as plt

data = pd.read_csv('./TestExer1-sales-round1.txt', low_memory=False, delimiter='\t')
print(data.head())

# (a) Make the scatter diagram with sales on the vertical axis and advertising on the horizontal axis. What do you expect to find if you would fit a regression line to these data?

scatter_plot = seaborn.regplot(x=data['Advert'], y=data['Sales'], fit_reg=False, data=data)
plt.title('Department Store')
scatter_plot.get_figure().savefig('Advert-Sales-scatter.png')

# (b) Estimate the coefficients a and b in the simple regression model with sales as dependent variable and advertising as explanatory factor. Also compute the standard error and t-value of b. Is b significantly different from 0?

def regres(subset, desc):
  regression = smf.ols('Sales ~ Advert', data=subset).fit()
  subset['residual'] = regression.resid
  print(regression.summary())
  scatter_plot = seaborn.regplot(x=subset['Advert'], y=subset['Sales'], fit_reg=True, data=subset)
  plt.title('%s Department Store' % desc)
  plt.show()
  scatter_plot.get_figure().savefig('%s-regression.png' % desc)
  return regression

regres(data, 'Full')

# (c) Compute the residuals and draw a histogram of these residuals. What conclusion do you draw from this histogram?

residual_distplot = seaborn.distplot(data['residual'], kde=False);
residual_distplot.get_figure().savefig('residual-histogram.png')
plt.title('Residual: One is not like the others.')
plt.show()

# (d) Apparently, the regression result of part (b) is not satisfactory. Once you realize that the large residual corresponds to the week with opening hours during the evening, how would you proceed to get a more satisfactory regression model?

print('(d) Delete the outlier because it is different for a reason that does not apply to the events we want to predict.')

# (e) Delete this special week from the sample and use the remaining 19 weeks to estimate the coefficients a and b in the simple regression model with sales as dependent variable and advertising as explanatory factor. Also compute the standard error and t-value of b. Is b significantly different from 0?

subset = data[ data['Sales'] < 50 ].copy()
regres(subset, 'Subset')
