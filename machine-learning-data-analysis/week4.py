import itertools
import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import matplotlib.pylab as plt
from scipy.stats import chi2_contingency

# SEX
# 1. Male
# 2. Femail
GENDER = 'SEX'

# DATE OF BIRTH: YEAR
# 1895-1984.  Year
BIRTH_YEAR = 'DOBY'

# HOW MANY DRINKS CAN HOLD WITHOUT FEELING INTOXICATED
# 0-98.  Number of drinks
# 99. Unknown
# BL.  NA, former drinker or lifetime abstainer
DRINKS_HOLD = 'S2AQ11'

# NUMBER OF EPISODES OF ALCOHOL DEPENDENCE
# 1-98.  Number of episodes
# 99.  Unknown
# BL.  NA, lifetime abstainer; did not meet symptom and/or duration criteria for lifetime alcohol dependence
AL_DEP_NUM = 'S2BQ2E'

# NUMBER OF EPISODES
# 1-98.  Separate times
# 99. Unknown
# BL.  NA, never or unknown if ever had fear/avoidance of social situation
SOCIAL_FEAR_DUR = 'S7Q17C'

# DURATION (WEEKS) OF ONLY/LONGEST EPISODE (BASED ON S7Q20A IF ONLY 1 EPISODE)
# 1-4435.  Weeks
# 9999.  Unknown
# BL.  NA, never or unknown if ever had fear/avoidance of social situation
SOCIAL_FEAR_LONG = 'S7Q19DR'

# TOTAL HOUSEHOLD INCOME IN LAST 12 MONTHS
# 24-3000000.  Household income in dollars
HOUSEHOLD_INCOME = 'S1Q12A'

# DRINKING STATUS
# 1.  Current drinker
# 2.  Ex-drinker
# 3.  Lifetime Abstainer
DRINK_STATUS = 'CONSUMER'

# MAIN TYPE OF ALCOHOL CONSUMED DURING PERIOD OF HEAVIEST DRINKING
# 1.  Coolers
# 2.  Beer
# 3.  Wine
# 4.  Liquor
# 9.  Unknown
# BL.  NA, lifetime abstainer
DRINK_PREF = 'S2AQ23'

explanatory_cols = [BIRTH_YEAR, DRINKS_HOLD, AL_DEP_NUM, SOCIAL_FEAR_DUR, GENDER, HOUSEHOLD_INCOME]
cols = [DRINK_STATUS, DRINK_PREF] + explanatory_cols

nesarc = pd.read_csv('../data/nesarc.csv', low_memory=False)[cols]
# Forget the non-drinkers.
nesarc = nesarc[ nesarc[DRINK_STATUS] != 3 ]

def prepare_numeric(data, attr, map_before={}, map_after={}):
    for oldVal, newVal in map_before.items():
      data[attr] = data[attr].replace(oldVal, newVal)
    data[attr] = pd.to_numeric(data[attr], errors='coerce')
    for oldVal, newVal in map_after.items():
      data[attr] = data[attr].replace(oldVal, newVal)

# Scale everything to mean 0, stdev 1
def to_normal_scale(data, *attrs):
    for attr in attrs:
        data[attr] = preprocessing.scale(data[attr].astype('float64'))
        print('Scaled %s to %s and std %s' % (attr, data[attr].mean(), data[attr].std()))

def summarize(data, attr, desc):
    counts = data.groupby(attr, sort=True).size()
    relative = counts * 100 / len(data)
    print('-' * 80)
    print(desc)
    print('Response counts:')
    print(counts)
    print('Response percentages:')
    print(relative)

# No change needed for BIRTH_YEAR, GENDER, and HOUSEHOLD_INCOME.
# Set unknown values to 1 and NA to 0.
prepare_numeric(nesarc, DRINKS_HOLD, map_after={99: 1})
prepare_numeric(nesarc, AL_DEP_NUM, map_before={' ': 0}, map_after={99: 1})
prepare_numeric(nesarc, SOCIAL_FEAR_DUR, map_before={' ': 0}, map_after={9999: 1})
prepare_numeric(nesarc, DRINK_PREF, map_after={9: np.nan, 1: np.nan}) # Ignore coolers (1).

# summarize(nesarc, DRINKS_HOLD, 'DRINKS_HOLD')
# summarize(nesarc, AL_DEP_NUM, 'AL_DEP_NUM')
# summarize(nesarc, SOCIAL_FEAR_DUR, 'Social Fear Duration')
# summarize(nesarc, HOUSEHOLD_INCOME, 'Household Income')
# summarize(nesarc, GENDER, 'Gender')
# summarize(nesarc, DRINK_STATUS, 'Drink status')
# summarize(nesarc, DRINK_PREF, 'Drink preference')

nesarc = nesarc[cols].dropna()
to_normal_scale(nesarc, *explanatory_cols)

# split data into train and test sets
clus_train, clus_test = train_test_split(nesarc, test_size=.3, random_state=830)

# k-means cluster analysis for 1-9 clusters
clusters=range(1,10)
meandist=[]

for k in clusters:
    model=KMeans(n_clusters=k)
    model.fit(clus_train)
    clusassign=model.predict(clus_train)
    meandist.append(sum(np.min(cdist(clus_train, model.cluster_centers_, 'euclidean'), axis=1)) 
    / clus_train.shape[0])

"""
Plot average distance from observations from the cluster centroid
to use the Elbow Method to identify number of clusters to choose
"""

fig = plt.figure()
plt.plot(clusters, meandist)
plt.xlabel('Number of clusters')
plt.ylabel('Average distance')
plt.title('Selecting k with the Elbow Method')
fig.savefig('clusters_distance.png')
plt.show()

# Interpret 3 cluster solution
model3=KMeans(n_clusters=3)
model3.fit(clus_train)
clusassign=model3.predict(clus_train)

# plot clusters
from sklearn.decomposition import PCA
pca_2 = PCA(2)
plot_columns = pca_2.fit_transform(clus_train)
fig = plt.figure()
plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=model3.labels_,)
plt.xlabel('Canonical variable 1')
plt.ylabel('Canonical variable 2')
plt.title('Scatterplot of Canonical Variables for 3 Clusters')
fig.savefig('pca_scatter.png')
plt.show()

# Label data by their assigned cluster.
clus_train.reset_index(inplace=True)
cluster_assignments = pd.DataFrame(data=model3.labels_, columns=['cluster'])
clustered = pd.concat([clus_train, cluster_assignments], axis=1)

# FINALLY calculate clustering variable means by cluster
print("Clustering variable means by cluster")
print(clustered.groupby('cluster').mean())

# Analyize differences in drink preference by cluster
crosstab = pd.crosstab(clustered[DRINK_PREF], clustered['cluster'])
relative_crosstab = crosstab.apply(lambda r: 100*r/r.sum(), axis=1)
print(relative_crosstab)
print(chi2_contingency(crosstab))

# Test each pair of drink preference and cluster.
# DRINK_PREF is 2, 3, 4
# cluster is 0, 1, 2
drink_prefs = clustered[DRINK_PREF].unique()
clusters = clustered['cluster'].unique()
for (drink_pref_a, drink_pref_b) in itertools.combinations(drink_prefs, 2):
    for (cluster_a, cluster_b) in itertools.combinations(clusters, 2):
        print('\n\n{} and {}, {} and {}'.format(drink_pref_a, drink_pref_b, cluster_a, cluster_b))
        testable = pd.DataFrame()
        dp_series = clustered[DRINK_PREF].map({drink_pref_a: drink_pref_a, drink_pref_b: drink_pref_b})
        c_series = clustered['cluster'].map({cluster_a: cluster_a, cluster_b: cluster_b})
        testable = pd.concat([dp_series, c_series], axis=1).dropna()
        print(testable.shape)
        testable_crosstab = pd.crosstab(testable[DRINK_PREF], testable['cluster'])
        print(chi2_contingency(testable_crosstab))
