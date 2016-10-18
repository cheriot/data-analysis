import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Response variable
RATE_BARACK = 'W1_D1'
RATE_BARACK_Q = 'How would you rate [Barack Obama] [0 to 100]'

# Explanatory variable
RATE_ROMNEY = 'W1_D2'
RATE_ROMNEY_Q = 'How would you rate [Mitt Romney] [0 to 100]'

# Explanatory variable
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

# Explanatory variable
ETHNICITY = 'PPETHM'
ETHNICITY_Q = """Race / Ethnicity
1 White, Non-Hispanic
2 Black, Non-Hispanic
3 Other, Non-Hispanic
4 Hispanic
5 2+ Races, Non-Hispanic"""


def prepare_numeric(data, attr):
    data[attr] = pd.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, np.nan)


def prepare_rate(data, attr):
    data[attr] = pd.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, np.nan)
    data[attr] = data[attr].replace(998, np.nan)


def center(data, attr):
    mean = data[attr].mean()
    new_col = '%s_centered' % attr
    data[new_col] = (data[attr] - mean)
    # New means will be really, really close to zero, but not exactly.
    print('Centered %s into %s. Now mean is %s instead of %s' % (attr, new_col, data[new_col].mean(), mean))
    return new_col

# Read, prepare, and center data.
ool_raw = pd.read_csv('../data/ool_pds.csv')[[POLITICAL_SPECTRUM, RATE_BARACK, RATE_ROMNEY, ETHNICITY]]

prepare_numeric(ool_raw, ETHNICITY)
ool_raw[ETHNICITY] = ool_raw[ETHNICITY].map(
        {1: 'WHITE',2: 'BLACK',3: 'OTHER',4: 'HISPANIC',5: 'MORE'})
ethnicity_dummies = pd.get_dummies(ool_raw[ETHNICITY], prefix='ETHNICITY')
ool_raw = pd.concat([ool_raw, ethnicity_dummies], axis=1)

prepare_numeric(ool_raw, POLITICAL_SPECTRUM)
prepare_rate(ool_raw, RATE_BARACK)
prepare_rate(ool_raw, RATE_ROMNEY)
POLITICAL_SPECTRUM_C = center(ool_raw, POLITICAL_SPECTRUM)
RATE_BARACK_C = center(ool_raw, RATE_BARACK)
RATE_ROMNEY_C = center(ool_raw, RATE_ROMNEY)
ool = ool_raw.dropna()

print('Data ready. %s' % (ool.shape,))
print(ool.head())
print('POLITICAL_SPECTRUM.describe()')
print(ool[POLITICAL_SPECTRUM].describe())
print('RATE_BARACK.describe()')
print(ool[RATE_BARACK].describe())
print('RATE_ROMNEY.describe()')
print(ool[RATE_ROMNEY].describe())

# Scatter of response with each explanatory variable.
obama_romney_scatter = seaborn.regplot(x=RATE_ROMNEY_C, y=RATE_BARACK_C, scatter=True, data=ool)
plt.xlabel('Centered Rating of Mitt Romney')
plt.ylabel('Centered Rating of Barack Obama')
obama_romney_scatter.get_figure().savefig('obama-romney-ratings-scatter.png')
plt.show()
obama_political_scatter = seaborn.regplot(x=POLITICAL_SPECTRUM_C, y=RATE_BARACK_C, scatter=True, data=ool)
plt.xlabel('Centered Political Spectrum - Left is left, Right is right')
plt.ylabel('Centered Rating of Barack Obama')
obama_political_scatter.get_figure().savefig('obama-ratings-political-spectrum-scatter.png')
plt.show()

# Regress!
formula = '%s ~ %s + %s + ETHNICITY_WHITE + ETHNICITY_BLACK + ETHNICITY_OTHER + ETHNICITY_HISPANIC + ETHNICITY_MORE' % (RATE_BARACK_C, RATE_ROMNEY_C, POLITICAL_SPECTRUM_C)
print('Regression formula is %s.' % formula)
regression = smf.ols(formula, data=ool).fit()
print(regression.summary())

# Q-Q plot for normality
qq_fig = sm.qqplot(regression.resid, line='r')
qq_fig.savefig('obama-rating-qq-plot.png')
plt.show()

# simple plot of residuals
stdres = pd.DataFrame(regression.resid_pearson)
stdres_fig = plt.figure()
plt.plot(stdres, 'o', ls='None')
l = plt.axhline(y=0, color='r')
plt.ylabel('Standardized Residual')
plt.xlabel('Observation Number')
plt.show()
stdres_fig.savefig('stdres-plot.png')

# additional regression diagnostic plots
plot_regres_exog_romney = plt.figure() # figsize(12,8))
plot_regres_exog_romney = sm.graphics.plot_regress_exog(regression,  RATE_ROMNEY_C, fig=plot_regres_exog_romney)
plt.show()
plot_regres_exog_romney.savefig('plot-regres-exog-romney.png')

plot_regres_exog_political = plt.figure() # figsize(12,8))
plot_regres_exog_political = sm.graphics.plot_regress_exog(regression,  POLITICAL_SPECTRUM_C, fig=plot_regres_exog_political)
plt.show()
plot_regres_exog_political.savefig('plot-regres-exog-political.png')

# leverage plot
influence_plot = sm.graphics.influence_plot(regression, size=8)
influence_plot.savefig('influence-plot.png')
print(influence_plot)
influence_plot.show()

# Examine histograms based on regression diagnostics.
fig = plt.figure()
political_hist = seaborn.distplot(ool[POLITICAL_SPECTRUM], kde=False)
plt.ylabel('Frequency')
plt.title("Political Spectrum")
plt.show()
political_hist.get_figure().savefig('political-spectrum-histogram.png')
obama_hist = seaborn.distplot(ool[RATE_BARACK], kde=False)
plt.ylabel('Frequency')
plt.title("Rating of President Obama")
obama_hist.get_figure().savefig('obama-rating-histogram.png')
plt.show()
romney_hist = seaborn.distplot(ool[RATE_ROMNEY], kde=False)
plt.ylabel('Frequency')
plt.title("Rating of Mitt Romney")
plt.show()
romney_hist.get_figure().savefig('romney-rating-histogram.png')
