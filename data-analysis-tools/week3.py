import numpy
import pandas
import seaborn
import matplotlib.pyplot as plt
import scipy

ool = pandas.read_csv('../data/ool_pds.csv', low_memory=False)

print('Outlook on Life Surveys, 2012')
print('rows %d, columns %d' % ool.shape)

RATE_MICHELLE = 'W1_D3'
RATE_MICHELLE_Q = '[Michelle Obama] How would you rate'

RATE_BARACK = 'W1_D1'
RATE_BARACK_Q = '[Barack Obama] How would you rate'

RATE_ROMNEY = 'W1_D2'
RATE_ROMNEY_Q = '[Mitt Romney] How would you rate'

ool = ool.loc[:,[RATE_MICHELLE, RATE_BARACK, RATE_ROMNEY]]


def prepare_rate(data, attr, name):
    data[attr] = pandas.to_numeric(data[attr], errors='coerce')
    data[attr] = data[attr].replace(-1, numpy.nan)
    data[attr] = data[attr].replace(998, numpy.nan)

prepare_rate(ool, RATE_MICHELLE, 'Michelle Obama')
prepare_rate(ool, RATE_BARACK, 'Barack Obama')
prepare_rate(ool, RATE_ROMNEY, 'Mitt Romney')
ool = ool.dropna()

pearson_r, p_value = scipy.stats.pearsonr(ool[RATE_BARACK], ool[RATE_ROMNEY])
print('pearson\'s r %s, p-value %f, r**2 %s' % (pearson_r, p_value, pearson_r**2))
scat1 = seaborn.regplot(x=RATE_BARACK, y=RATE_ROMNEY, fit_reg=True, data=ool)
plt.xlabel('Obama Rating')
plt.ylabel('Romney Rating')
plt.title('Scatterplot for the Association Between Barack Obama and Mitt Romney Ratings')
plt.show()
scat1.get_figure().savefig('BarackMittScatter.png')

pearson_r, p_value = scipy.stats.pearsonr(ool[RATE_BARACK], ool[RATE_MICHELLE])
print('pearson\'s r %s, p-value %f, r**2 %s' % (pearson_r, p_value, pearson_r**2))
scat1 = seaborn.regplot(x=RATE_BARACK, y=RATE_MICHELLE, fit_reg=True, data=ool)
plt.xlabel('Barack Rating')
plt.ylabel('Michelle Rating')
plt.title('Scatterplot for the Association Between Barack and Michelle Obama Ratings')
plt.show()
scat1.get_figure().savefig('BarackMichelleScatter.png')
