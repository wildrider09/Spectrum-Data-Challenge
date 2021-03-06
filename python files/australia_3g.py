# -*- coding: utf-8 -*-
"""Australia 3G

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n4uJL-7qoV8V1oRa2b-pxf4A861t4JCU

1.   4G - "700 - 900 - 2500"
2.   3G
"""



"""# Imports"""

!pip3 install catboost
!pip install shap
!pip install xlrd

import catboost as cb
import numpy as np
import pandas as pd
import seaborn as sns
import shap
#import load_boston
from matplotlib import pyplot as pltfrom
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.inspection import permutation_importance
from sklearn import datasets

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
import seaborn as sns

df = pd.read_excel ('Spectrum Database_March 2021.xlsx')

!pip install xlrd 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms

df = pd.read_excel ('Spectrum Database_March 2021.xlsx')

df = df[(df.countryName == 'Australia')]

df = df[df.awardName == '3G Auction']

df

payment = pd.read_excel ('Spectrum Payments_March 2021.xlsx') 

payment

merged = pd.merge(df, payment, on='lotId', how='inner')

merged

from matplotlib import pyplot as plt
plt.figure(figsize=(15,5))
# X axis : lotID
# Y axis : amount
plt.scatter(merged['lotId'], merged['amount'])

for i, winner in enumerate(merged['winner']):
  plt.annotate(winner, (merged['lotId'][i], merged['amount'][i]))

merged.plot(x='region', y='popCovered',figsize=(10,5),color='purple')

"""For each company as we have kind of 6 of them lets find out:
*   Number of wins
*   Total Money Spend above reserved price
*   Average bids
*   Avg Winning bid over reserved 
*   Total population covered 
*   Overall population covered
*   Average population coved 
*   Regions

"""

dict_for_Population_Overall = {"owner":[], "population":[], "average_population":[], "total_spend":[], "average_spend":[], "average_spend_over_reserve":[]}

def Get_Insights(For_Winner):
    # Prepare Variables
    # For_Winner = 'Telstra'
    Number_of_Wins = 0
    Total_Spend = int(0)
    Average_Biding_Price = 0
    Average_Biding_Price_Over_Reserved = 0
    Population_Coverd = 0
    Average_Population_Covered = 0
    Regions = set()

    for index, row in merged.iterrows():
        if row['winner'] == For_Winner:
            Number_of_Wins += 1
            Total_Spend += row['headlinePriceLocal']
            Average_Biding_Price_Over_Reserved +=  row['headlinePriceLocal'] -  row['reservePriceLocal']
            Population_Coverd += row['popCovered']
            Regions.add(row['region'])
    

    Average_Biding_Price = Total_Spend / Number_of_Wins
    Average_Biding_Price_Over_Reserved /= Number_of_Wins
    Average_Population_Covered = Population_Coverd / Number_of_Wins

    print(For_Winner)
    print("Won in ", Number_of_Wins, "  Bids") 
    print("Total Spend : ",Total_Spend)
    print("Average Bidding Price : ", round(Average_Biding_Price, 2))
    print("Average Bidding prie over Reserved : ", round(Average_Biding_Price_Over_Reserved, 2))
    print("Total population Coverd : ", Population_Coverd)
    dict_for_Population_Overall["owner"].append(For_Winner)
    dict_for_Population_Overall["population"].append(Population_Coverd)
    dict_for_Population_Overall["average_population"].append(round(Average_Population_Covered, 2))
    dict_for_Population_Overall["total_spend"].append(Total_Spend)
    dict_for_Population_Overall["average_spend"].append(round(Average_Biding_Price, 2))
    dict_for_Population_Overall["average_spend_over_reserve"].append(round(Average_Biding_Price_Over_Reserved, 2))
    print("Average Population Coverd : ", round(Average_Population_Covered, 2))
    print("Regions Coverd are : ", Regions)
    print("-----------------------------------------------------------------------------------------------------")
    #return dict_for_Population_Overall

#dict_for_Population_Overall = {"owner":[],"population":[]}
    
for winner in merged['winner'].unique():
    Get_Insights(winner)
    print("")

print(dict_for_Population_Overall)

# Plot of Average population of each owner  
fig = plt.figure(figsize=(12, 5))
ax = fig.add_axes([0,0,1,1])
langs = dict_for_Population_Overall['owner']
students = dict_for_Population_Overall['average_population']
ax.bar(langs,students,color='darkslategray',width=0.8)
plt.xlabel('winner')
plt.ylabel('Average Population')
plt.grid(color="teal", linestyle=':', linewidth=1.5 ,axis='y', alpha=0.7)
plt.show()

# Plot of TOtal population of each owner
# Plot of Average population of each owner  
fig = plt.figure(figsize=(12, 5))
ax = fig.add_axes([0,0,1,1])
langs = dict_for_Population_Overall['owner']
students = dict_for_Population_Overall['population']
ax.bar(langs,students,color='pink',width=0.8)
plt.xlabel('Winner')
plt.ylabel('Population')
plt.grid(color='mediumpurple', linestyle=':', linewidth=1.5, axis='y', alpha=0.7)
plt.show()

# Plot of total spending of each owner
# Plot of Average population of each owner  
fig = plt.figure(figsize=(12, 5))
ax = fig.add_axes([0,0,1,1])
langs = dict_for_Population_Overall['owner']
students = dict_for_Population_Overall['total_spend']
ax.bar(langs,students,color='lightsteelblue',width=0.8)
plt.xlabel('Winner')
plt.ylabel('Total Spend')
plt.grid(color='#95a5a6', linestyle=':', linewidth=1.5, axis='y', alpha=0.7)
plt.show()

# plot of average spending of each ownerr  
fig = plt.figure(figsize=(12, 5))
ax = fig.add_axes([0,0,1,1])
langs = dict_for_Population_Overall['owner']
students = dict_for_Population_Overall['average_spend']
ax.bar(langs,students,color='grey',width=0.8)
plt.xlabel('Winner')
plt.ylabel('Average Spend')
plt.grid(color='#95a5a6', linestyle=':', linewidth=1.5, axis='y', alpha=0.7)
plt.show()

# plot of average spending over reserve  
fig = plt.figure(figsize=(12, 3))
ax = fig.add_axes([0,0,1,1])
langs = dict_for_Population_Overall['owner']
students = dict_for_Population_Overall['average_spend_over_reserve']
ax.bar(langs,students,color='lightsalmon',width=0.8)
plt.grid(color='#95a5a6', linestyle=':', linewidth=1.5, axis='y', alpha=0.7)
plt.xlabel('Winner')
plt.ylabel('Average Spend above Reserve')
plt.show()

# Make a copy to save preds for next year
Data_3G_next_year_preds = merged.copy()

# Model
# Remove column name 
merged.drop(['minAmount', 'amount'], axis = 1)

"""### Handle Null Values

"""

# Handle Nulls
merged_cols = merged.columns.to_list()
mv = merged[merged_cols].isnull().sum()
mp = mv / len(merged)*100
mp

# Drop columns with null values 
# These columns have null value throughout
merged = merged.drop(['lotComments', 'awardComments'], axis = 1)

# Delete columns which have only one or null values overall
for col in merged.columns.to_list():
    count = merged[col].nunique()
    if count == 1:
        del merged[col]
        print(col)
merged

"""### Frequency Encoding"""

# Frequency Encoding
def Frequency_Encode(col):
    # print(col)
    fe = merged.groupby(col).size() / len(merged)
    merged.loc[:, col + '_freq_encode'] = merged[col].map(fe)
    merged

for col in merged.columns.to_list():
    # print(col, type(merged[col]))
    if merged[col].dtype == 'object':
        Frequency_Encode(col)
        del merged[col]

merged

x = merged.copy()
del x['amount']
del x['minAmount']
# del x['headlinePriceLocal']
y = pd.DataFrame(merged.headlinePriceLocal)
x

y

print(x.shape, y.shape)

# Generating Next year Expected Prices
x_test = merged.copy()
x_test['reservePriceLocal'] = x_test['headlinePriceLocal']
del x_test['amount']
del x_test['minAmount']
# del x['headlinePriceLocal']
y_test = pd.DataFrame(merged.headlinePriceLocal)
x_test

"""### Correlarion Matrix"""

# Compute the correlation matrix
corr = x.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(15, 12))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(190, 60, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, center=0,
            square=True, linewidths=.8, cbar_kws={"shrink": .8}, annot=True)

"""### Model"""

# x has train
# y has target var
del x['headlinePriceLocal']

train_dataset = cb.Pool(x, y)
model = cb.CatBoostRegressor(loss_function='RMSE')
grid = {'iterations': [150, 200, 300],
        'learning_rate': [0.1],
        'depth': [8, 10, 15],
        'l2_leaf_reg': [3, 5]}
model.grid_search(grid, train_dataset)

pred = model.predict(x)
rmse = (np.sqrt(mean_squared_error(y, pred)))
r2 = r2_score(y, pred)
print('Testing performance')
print('RMSE: {:.2f}'.format(rmse))
print('R2: {:.2f}'.format(r2))

# Take predictions on test datase
del x_test['headlinePriceLocal']
test_pred = model.predict(x_test)
rmse_test = (np.sqrt(mean_squared_error(x_test['reservePriceLocal'], test_pred)))
r2_test = r2_score(y, test_pred)
print('Testing performance')
print('RMSE: {:.2f}'.format(rmse_test))
print('R2: {:.2f}'.format(r2_test))
test_pred

sorted_feature_importance = model.feature_importances_.argsort()

plt.barh(merged.columns[sorted_feature_importance], 
        model.feature_importances_[sorted_feature_importance], 
        color='darkcyan')
plt.xlabel("Feature Importance")

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(x)
shap.summary_plot(shap_values, x, feature_names = merged.columns[sorted_feature_importance])

# ITs right time to save the preds
Data_3G_next_year_preds

Data_3G_next_year_preds['reservePriceLocal'] = Data_3G_next_year_preds['headlinePriceLocal']
Data_3G_next_year_preds['minAmount'] = Data_3G_next_year_preds['headlinePriceLocal']
Data_3G_next_year_preds

Data_3G_next_year_preds['headlinePriceLocal'] = test_pred
Data_3G_next_year_preds['amount'] = test_pred

Data_3G_next_year_preds

Data_3G_next_year_preds['date'] = Data_3G_next_year_preds['date'].apply(lambda x: '2002-03-22')  
Data_3G_next_year_preds

Data_3G_next_year_preds.to_csv('Spectrum_Data_Australia_3G_next_year_preds.csv', index=False)

from google.colab import files
files.download("Spectrum_Data_Australia_3G_next_year_preds.csv")