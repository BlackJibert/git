
"""
    聚类算法
"""
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

from sklearn import (manifold, datasets, decomposition, ensemble, discriminant_analysis, random_projection)

from sklearn.cluster import DBSCAN

df_data = pd.read_csv('pca_dbscan_CC.csv')
X = df_data.iloc[:, 0:40+104+819]
print(X)

"""
    规范化之后，会分不出类别，都是0.
"""
# X_scaled2 = decomposition.TruncatedSVD(n_components=3).fit_transform(X)
#
# dbscan1 = DBSCAN(eps=50).fit_predict(X)
#
# dbscan2 = dbscan1.tolist()
#
# df_data['svd_dbscan'] = dbscan2
#
# genders = [0, 1]
# df = pd.DataFrame({
#     'X': X[:, 0],
#     'Y': X[:, 1],
#     'label': dbscan1
# })
#
# fg = sns.FacetGrid(data=df, hue='label', hue_order=genders)
# fg.map(plt.scatter, 'X', 'Y').add_legend(title='svd_dbscan')
# # plt.show()
# plt.savefig('svd_dbscan.png')


import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import (manifold, datasets, decomposition, ensemble, discriminant_analysis, random_projection)
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN


"""
    规范化之后，会分不出类别，都是0.
"""
X_scaled2 = decomposition.TruncatedSVD(n_components=2).fit_transform(X)

dbscan1 = DBSCAN(eps=50).fit_predict(X_scaled2)

dbscan2 = dbscan1.tolist()
print('dbscan2:', dbscan2)
df_data['svd_dbscan'] = dbscan2
print(X_scaled2[:, 0])
print(X_scaled2[:, 1])
genders = [0, 1]
df = pd.DataFrame({
    'X': X_scaled2[:, 0],
    'Y': X_scaled2[:, 1],
    'Class': dbscan1
})

fg = sns.FacetGrid(data=df, hue='Class', hue_order=genders)

fg.map(plt.scatter, 'X', 'Y').add_legend(title='svd_dbscan')
# plt.show()
plt.savefig('svd_dbscan_CC.png')

df_data.to_csv('svd_dbscan_CC.csv')