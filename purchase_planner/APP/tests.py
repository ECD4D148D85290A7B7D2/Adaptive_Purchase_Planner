from django.test import TestCase

from django.test import TestCase

import os


def __setup_django(root_path, settings):
    import os
    import django
    import sys

    os.chdir(root_path)

    # Django settings
    sys.path.append(root_path)
    os.environ['DJANGO_SETTINGS_MODULE'] = settings

    django.setup()

PROJECT_PATH = "."
PROJECT_SETTING = "purchase_planner.settings"

__setup_django(PROJECT_PATH, PROJECT_SETTING)



from APP.models import Purchases
# Create your tests here.

import sqlite3

conn = sqlite3.connect("./db.sqlite3")
cur = conn.cursor()

# use .tables
# .header on
'''
pip install pandabase

sqlite> .schema APP_purchasetable 
CREATE TABLE IF NOT EXISTS "APP_purchasetable" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL, "item" varchar(255) NOT NULL, "price" real NOT NULL, "store" varchar(255) NOT NULL, "purchaseDate" date NOT NULL);

delete from APP_purchasetable

python ./APP/tests.py 

'''

import pandas as pd
import numpy as np

import pandabase

dataset = pd.read_csv("/home/rhofix/work/TCD/AD/group/mock-data-2.csv")
dataset['PurchaseDate'] = pd.to_datetime(dataset.PurchaseDate)
dataset.sort_values(by=['PurchaseDate'], inplace=True, ascending=True)
dataset['Price'] = np.random.uniform(0.6, 8.8, dataset.shape[0])
dataset['Price'] = dataset['Price'].round(2)


# dataset['day_of_week'] = dataset['PurchaseDate'].dt.weekday_name this will come while designing recommendation api
print(dataset.shape)

dataset.index.name = 'id'  # index must be named to use as PK
dataset.index = [x for x in range(1, len(dataset.values) + 1)]

my_data = pd.DataFrame(
    columns=['User', 'Item', 'Price', 'Store', 'PurchaseDate'],
    data=dataset)



for dataitem in my_data.itertuples():
    data = Purchases.objects.create(user_id=dataitem.User, item=dataitem.Item, price=dataitem.Price, store=dataitem.Store, purchase_date=dataitem.PurchaseDate)



'''     
import pytz
eastern = pytz.timezone('US/Eastern')
my_data.PurchaseDate = my_data.PurchaseDate.tz_localize(pytz.utc).tz_convert(eastern)

my_data.index.name = 'id'
print(my_data)
pandabase.to_sql(my_data, table_name='app_purchasetable', con=conn, how='append')
'''
