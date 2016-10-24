import pandas as pd
import statsmodels.formula.api as smf 
from statsmodels.stats.outliers_influence import reset_ramsey
import seaborn

explanatory_cols = ['INFL', 'PROD', 'UNEMPL', 'COMMPRI', 'PCE', 'PERSINC', 'HOUST']
columns = ['OBS', 'INTRATE'] + explanatory_cols
# pandas reads some unamed columns of NaN so exclude them.
data = pd.read_csv('TestExer3-TaylorRule-round1.tsv', low_memory=False, delimiter='\t') \
  [columns]
# Monthly data for the USA over the period 1960 through 2014 for the following variables:
# INTRATE: Federal funds interest rate
# INFL: Inflation
# PROD: Production
# UNEMPL: Unemployment
# COMMPRI: Commodity prices
# PCE: Personal consumption expenditure 
# PERSINC: Personal income
# HOUST: Housing starts

print(data.shape)
print(data.head())

def print_divider():
  print('\n\n\n')
  print('-'*80)

print_divider()
print('Part (a) Start by regressing INTRATE on all 7 other variables and eliminate 1 at a time.')
print(smf.ols(formula='INTRATE ~ INFL + PROD + UNEMPL + COMMPRI + PCE + PERSINC + HOUST', data=data).fit().summary())
print('\nThe highest p-value and lowest t statistic is for UNEMPL (t-value 1.059, p-value 0.290) so remove it from the model.')
print(smf.ols(formula='INTRATE ~ INFL + PROD + COMMPRI + PCE + PERSINC + HOUST', data=data).fit().summary())
print('\nThe highest p-value and lowest t statistic is now PROD (t-value -0.989, p-value 0.323) so remove it from the model.')
print(smf.ols(formula='INTRATE ~ INFL + COMMPRI + PCE + PERSINC + HOUST', data=data).fit().summary())
print('\nNow everything is significant while the R^2, AIC, and BIC have barely changed from the original. Result is INTRATE ~ INFL + COMMPRI + PCE + PERSINC + HOUST')

print_divider()
print('Part (b) Start by regressing the federal funds rate on only a constant and add 1 variable at a time.  Is the model the same as in (a)?')

print('Starting with INFL with t-value = 28.924506, p-value = 2.472635e-119.')
formula_b_1 = 'INTRATE ~ INFL'
print('Formula b1 %s' % formula_b_1)
print(smf.ols(formula=formula_b_1, data=data).fit().summary())
print('\nNext add PERSINC with t-value = 9.478074, p-value = 4.616637e-20.')
formula_b_2 = 'INTRATE ~ INFL + PERSINC'
print('Formula b2 %s' % formula_b_2)
print(smf.ols(formula=formula_b_2, data=data).fit().summary())
print('\nNext add PCE with t-value = 3.412051, p-value = 6.843747e-04.')
formula_b_3 = 'INTRATE ~ INFL + PERSINC + PCE'
print('Formula b3 %s' % formula_b_3)
print(smf.ols(formula=formula_b_3, data=data).fit().summary())
print('\nNext add HOUST with t-value = -4.893253, p-value = 1.249935e-06.')
formula_b_4 = 'INTRATE ~ INFL + PERSINC + PCE + HOUST'
print('Formula b4 %s' % formula_b_4)
print(smf.ols(formula=formula_b_4, data=data).fit().summary())
print('\nNext add COMMPRI with t-value = -2.841100, p-values 4.635778e-03.')
formula_b_5 = 'INTRATE ~ INFL + PERSINC + PCE + HOUST + COMMPRI'
print('Formula b5 %s' % formula_b_5)
print(smf.ols(formula=formula_b_5, data=data).fit().summary())

remaining_cols = [c for c in explanatory_cols if c not in ['INFL', 'PERSINC', 'PCE', 'HOUST', 'COMMPRI']]
for col in remaining_cols:
    formula = 'INTRATE ~ INFL + PERSINC + PCE + HOUST + COMMPRI + %s' % col
    print('Formula %s' % formula)
    r = smf.ols(formula=formula, data=data).fit()
    print(pd.concat([r.tvalues, r.pvalues], axis=1))

print_divider()
print('Part (c) Test the Taylor rule of equation (1) using the RESET test, Chow break and forecast test (with in both tests as break date January 1980) and a Jarque-Bera test.  What do you conclude?')

# OLS for the taylor formula. This will contain the R^2, AIC, BIC, Jarque-Bera, and P(Jarque-Bera) that will be used in the write up.
taylor_regres = smf.ols(formula='INTRATE ~ INFL + PROD', data=data).fit()
print(taylor_regres.summary())
print('Ramsey RESET: Null Hypothesis is that the model has no omitted variables.')
f_test = reset_ramsey(taylor_regres, degree=3)
print(f_test.summary())
print('\nTest for break at January 1980')
# break_index = data[ data['OBS'] == '1980:1' ].index.tolist()[0]
break_index = data[ data['OBS'] == '1980:1' ].index.tolist()[0]
print('break at index %s' % break_index)
print(het_goldfeldquandt(taylor_regres.resid, taylor_regres.model.exog, split=break_index, alternative='decreasing'))
# Useful example of how to actually use a Chow test:
# https://thetarzan.wordpress.com/2011/06/16/the-chow-test-in-r-a-case-study-of-yellowstones-old-faithful-geyser/
print(het_goldfeldquandt(taylor_regres.resid, taylor_regres.model.exog, split=break_index, alternative='increasing'))
