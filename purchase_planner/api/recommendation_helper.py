import numpy as np
import random
import datetime
import pandas as pd
from .sys_constant import aging_criteria, inactive, item_dict, user_dict

class AddProduct(object):

    def addUserPurchase(self, request):

        transaction_data = pd.read_csv("./api/data/user_purchase_history.csv")
        transaction_data = transaction_data.append({'User': request.data['user_id'],
                                                              'Store': request.data['store'],
                                                              'Size': request.data['size'],
                                                              'Product': request.data['product_id'],
                                                              'WeekDay': request.data['weekday'],
                                                              'Price': request.data['price'],
                                                              'Transaction_Date': request.data['transaction_date'],},
                                                             ignore_index=True)
        transaction_data.to_csv('./api/data/user_purchase_history.csv', index=False, header=True)


class RecommenderEngine(object):

    def productRecommendation(self, user_id):

        purchase_pattern_data = pd.DataFrame()
        user_transaction_data = self.getUserPurchaseHistory(int(user_id))
        item_list = user_transaction_data.Product.unique().tolist()
        for item in item_list:
            item_data = user_transaction_data[(user_transaction_data['Product'] == item)].copy()
            size_list = item_data.Size.unique().tolist()
            for size in size_list:
                tempdataset = item_data[(item_data['Size'] == size)].copy()
                if tempdataset.empty == True:
                    continue
                else:
                    tempdataset['Transaction_Date'] = pd.to_datetime(tempdataset.Transaction_Date)
                    tempdataset.sort_values(by=['Transaction_Date'], inplace=True, ascending=True)
                    sys_date = datetime.datetime.now().date()
                    last_purchase_date = tempdataset.Transaction_Date.iloc[-1]
                    last_purchase_date = last_purchase_date.date()
                    days_diff = (sys_date - last_purchase_date).days
                    if (days_diff > aging_criteria and len(tempdataset) == 1):
                        frequent_item = False
                        purchase_pattern_data = purchase_pattern_data.append({'User': user_id,
                                                                              'Product': item,
                                                                              'Product_Name': item_dict[item],
                                                                              'Size': size,
                                                                              'Purchase_Freq': -3,
                                                                              'Preferred_Shopping_Weekday': -3,
                                                                              'Preferred_Store': tempdataset.Store,
                                                                              'Last_Purchased': last_purchase_date,
                                                                              'Days_Left': -2,
                                                                              'Approx_Item_Price': tempdataset.Price,
                                                                              'Frequent_Item': frequent_item,
                                                                              'Reminders': inactive},
                                                                             ignore_index=True)
                        continue
                    else:
                        reminders = 0
                        tempdataset['Frequency'] = tempdataset.Transaction_Date.diff()
                        freqdata = tempdataset.Frequency.value_counts().index[0]
                        purchase_freq = freqdata.days
                        if (days_diff <= purchase_freq):
                            days_left = purchase_freq - days_diff
                            frequent_item = True
                        elif days_diff / purchase_freq <= 2:
                            days_left = -1
                            frequent_item = True
                            reminders = days_diff // purchase_freq
                        else:
                            days_left = -2
                            frequent_item = False
                            reminders = inactive
                        freq_store = tempdataset.Store.value_counts().index[0]
                        freq_shopping_day = tempdataset.WeekDay.value_counts().index[0]
                        price = tempdataset.Price.mean()
                        purchase_pattern_data = purchase_pattern_data.append({'User': user_id,
                                                                              'Product': item,
                                                                              'Product_Name': item_dict[item],
                                                                              'Size': size,
                                                                              'Purchase_Freq': purchase_freq,
                                                                              'Preferred_Shopping_Weekday': freq_shopping_day,
                                                                              'Preferred_Store': freq_store,
                                                                              'Last_Purchased': last_purchase_date,
                                                                              'Days_Left': days_left,
                                                                              'Approx_Item_Price': price,
                                                                              'Frequent_Item': frequent_item,
                                                                              'Reminders': reminders}, ignore_index=True)

        return purchase_pattern_data, user_dict[int(user_id)]

    def getUserPurchaseHistory(self, user_id):

        transaction_data = pd.read_csv("./api/data/user_purchase_history.csv")
        user_transaction_data = transaction_data[(transaction_data['User'] == user_id)].copy()
        return user_transaction_data

    def shopRecommendation(self, user_id):
        transaction_data = pd.read_csv("./api/data/user_purchase_history.csv")
        store_list = transaction_data.Store.unique().tolist()
        item_list = transaction_data.Product.unique().tolist()
        shop_recommender = pd.DataFrame(
            columns=['Product', 'Size', 'Store', 'Avg_Price', 'Latest_Price', 'Latest_Price_Updated_On'])

        for product in item_list:
            product_data = transaction_data[(transaction_data.Product == product)]
            size_list = product_data.Size.unique().tolist()
            # print(len(sizelist))
            for size in size_list:
                size_data = product_data[(product_data.Size == size)]
                store_list = size_data.Store.unique().tolist()
                for store in store_list:
                    tempdataset = size_data[(size_data['Store'] == store)]
                    tempdataset['Transaction_Date'] = pd.to_datetime(tempdataset.Transaction_Date)
                    tempdataset.sort_values(by=['Transaction_Date'], inplace=True, ascending=True)
                    last_purchased_price = tempdataset.Price.iloc[-1]
                    last_purchased_date = tempdataset.Transaction_Date.iloc[-1]
                    mean_price = tempdataset.Price.mean()
                    shop_recommender = shop_recommender.append({'Product': product,
                                                                'Size': size,
                                                                'Store': store,
                                                                'Avg_Price': mean_price,
                                                                'Latest_Price': last_purchased_price,
                                                                'Latest_Price_Updated_On': last_purchased_date.date()},
                                                               ignore_index=True)
                    shop_recommender = shop_recommender.loc[shop_recommender.groupby(['Product', 'Size'])['Latest_Price'].idxmin()]

        return shop_recommender, user_dict[int(user_id)]




if __name__ == '__main__':
    testing = RecommenderEngine()
    test, username = testing.productRecommendation(10000)
    test, username = testing.shopRecommendation(10000)