import pandas as pd
import numpy as np
import random
import datetime



dataset = pd.read_csv("./data/gen-data-shop.csv")

transaction_data = pd.read_csv("./data/gen-data-shop.csv")

# MUST ATTENTION, UPDATE BELOW DATE TO GENERATE DATES FROM PURCHASE DAY
dateSelect = '2018-07-01'

transaction_data['Transaction_Date'] = dateSelect
transaction_data['Transaction_Date'] = pd.to_datetime(transaction_data.Transaction_Date)
transaction_data['PurchaseDay'] = pd.to_timedelta(transaction_data['PurchaseDay'], unit='d')
transaction_data['Transaction_Date'] = transaction_data['Transaction_Date'] + transaction_data['PurchaseDay']
transaction_data['WeekDay'] = transaction_data['Transaction_Date'].dt.weekday_name
transaction_data.sort_values(by=['Transaction_Date'], inplace=True, ascending=False)
transaction_data.drop('Price', 1, inplace = True)
transaction_data.drop('PurchaseDay', 1, inplace = True)
transaction_data.head()


smalldata = transaction_data[(transaction_data['Size'] == 'S')]
smalldata['Price'] = np.random.uniform(0.6, 3.8, smalldata.shape[0]).round(2)


mediumdata = transaction_data[(transaction_data['Size'] == 'M')]
mediumdata['Price'] = np.random.uniform(4.1, 5.9, mediumdata.shape[0]).round(2)


largedata = transaction_data[(transaction_data['Size'] == 'L')]
largedata['Price'] = np.random.uniform(6.1, 8.4, largedata.shape[0]).round(2)


frames = [smalldata, mediumdata, largedata]
transaction_data = pd.concat(frames)

transaction_data = transaction_data.sort_values(by=['User'])
transaction_data.to_csv('./data/user_purchase_history.csv', index = False, header=True)

print("Data Prepared in user_purchase_history.csv")