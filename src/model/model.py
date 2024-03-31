# new terminal
# cd model
# python model.py -u 'MONGO_DB_CONNECTION_STRING'

import argparse
import matplotlib.pyplot as plt
import pprint

import pandas as pd
import seaborn as sn
from pymongo import MongoClient

parser = argparse.ArgumentParser(description='Create Model')
parser.add_argument('-u', '--uri', required=True, help="mongodb uri with username/password")
args = parser.parse_args()

mongo_uri = args.uri
mongo_db = "mdmBreweryDb"
mongo_collection = "beer"

client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

# fetch a single document
beer = collection.find_one(projection={"url": 0})
# Construct a list of dictionaries, ensuring all keys are present in each document
values = [{key: beer.get(key, None) for key in
           ["_id", "alcohol_by_volume", "bitterness_ibu", "brew_style", "color_srm", "primary_flavor_notes",
            "serving_temperature"]} for beer in collection.find(projection={"url": 0})]

#values = [beer.values() for beer in collection.find(projection={"url": 0})]
# we later use track document's field names to label the columns of the dataframe
df = pd.DataFrame(columns=beer.keys(), data=values).set_index("_id")
# Cleanup Alcohol by volume attriibute
df = df[df['alcohol_by_volume'].notna()]
df['alcohol_by_volume'] = df['alcohol_by_volume'].str.replace('%', '')
df['alcohol_by_volume'] = df['alcohol_by_volume'].str.split('-').apply(
    lambda x: (float(x[0]) + float(x[1])) / 2 if len(x) > 1 else float(x[0]))
# bitterness_ibu
df['bitterness_ibu'] = df['bitterness_ibu'].str.replace(' ', '')
df['bitterness_ibu'] = df['bitterness_ibu'].str.split('-').apply(
    lambda x: (float(x[0]) + float(x[1])) / 2 if len(x) > 1 else float(x[0]))

# primary flavor notes (From String array to dummy variables
dummy_variables = pd.get_dummies(df['primary_flavor_notes'].apply(pd.Series).stack(), prefix="pfn").groupby(
    level=0).sum()
df = pd.concat([df, dummy_variables], axis=1)
df.drop('primary_flavor_notes', axis=1, inplace=True)

# brew_style into dummy variables
# Create dummy variables for brew_style
df['brew_style'] = df['brew_style'].str.replace(' ', '')
brew_style_dummies = pd.get_dummies(df['brew_style'], prefix='bs')
df = pd.concat([df, brew_style_dummies], axis=1)
df.drop('brew_style', axis=1, inplace=True)

# color_srm
df['color_srm'] = df['color_srm'].str.extract(r'(\d+)')
df = df[df['color_srm'].notna()]
df['color_srm'] = df['color_srm'].apply(lambda x: float(x))

# serving_temperature
serving_temperature_dummies = pd.get_dummies(df['serving_temperature'], prefix='st')
df = pd.concat([df, serving_temperature_dummies], axis=1)
df.drop('serving_temperature', axis=1, inplace=True)


corr = df.corr(numeric_only=True)
#filtered_corr_matrix = corr.where(((corr >= 0.2) | (corr <= -0.2)))
#for feature, correlation in corr['alcohol_by_volume'].items():
#    print(f"Correlation with '{feature}': {correlation}")
#Maybe do forward selection
#Features die ich will bitterness_ibu,
#sn.heatmap(corr, annot=True)
#plt.show()

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
#Forward selection in Excel ->
y = df.reset_index()['alcohol_by_volume']
x = df.reset_index()[['bitterness_ibu', 'st_Cold', 'bs_American-StyleImperialStout', 'pfn_Bittersweet','color_srm']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=42)

# Baseline Linear Regression
lr = LinearRegression()
lr.fit(x_train, y_train)

y_pred_lr = lr.predict(x_test)
r2 = r2_score(y_test, y_pred_lr)
mse = mean_squared_error(y_test, y_pred_lr)

# Mean Squared Error / R2
print("r2:\t{}\nMSE: \t{}".format(r2, mse))

# GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

gbr = GradientBoostingRegressor(n_estimators=50, random_state=9000)
gbr.fit(x_train, y_train)
y_pred_gbr = gbr.predict(x_test)
r2 = r2_score(y_test, y_pred_gbr)
mse = mean_squared_error(y_test, y_pred_gbr)

print("r2:\t{}\nMSE: \t{}".format(r2, mse))

print("*** DEMO ***")
bitterness_ibu = 46
st_Cold = True
bs_American_StyleImperialStout = False
pfn_Bittersweet = False
color_srm = 10
demoinput = [[bitterness_ibu,st_Cold,bs_American_StyleImperialStout,pfn_Bittersweet,color_srm]]
demodf = pd.DataFrame(columns=['bitterness_ibu', 'st_Cold', 'bs_American-StyleImperialStout', 'pfn_Bittersweet','color_srm'], data=demoinput)
demooutput = gbr.predict(demodf)
abv_predicted = demooutput[0]

print("Reality: 4.7%")
print("Our Model: " + str(abv_predicted)+"%")


# Save To Disk
import pickle

# save the classifier
with open('GradientBoostingRegressor.pkl', 'wb') as fid:
    pickle.dump(gbr, fid)

# load it again
with open('GradientBoostingRegressor.pkl', 'rb') as fid:
    gbr_loaded = pickle.load(fid)
    demooutput = gbr_loaded.predict(demodf)
    abv_predicted = demooutput[0]
    print("Our Model: " + str(abv_predicted)+"%")
