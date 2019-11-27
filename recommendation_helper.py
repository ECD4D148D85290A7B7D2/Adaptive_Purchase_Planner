import numpy as np
import random
import datetime
import pandas as pd
from sys_constant import aging_criteria, inactive, item_dict, user_dict
from sklearn.linear_model import LinearRegression
#import xgboost as xgb
from feature_engine.categorical_encoders import OneHotCategoricalEncoder
from sklearn.model_selection import train_test_split

class AddProduct(object):

    def addUserPurchase(self, request):

        transaction_data = pd.read_csv("data/gen-data-shop.csv")
        # monday=502, tuesday=503, wed=504
        purchase_day = 504
        transaction_data = transaction_data.append({'User': request.args.get('user_id'),
                                                              'PurchaseDay': purchase_day,
                                                              'Store': request.args.get('store'),
                                                              'Product': request.args.get('product_id'),
                                                              'Size': request.args.get('size'),
                                                              'Price': 2.434343,}, ignore_index=True)
        transaction_data.to_csv('data/gen-data-shop.csv', index=False, header=True)
        #exec(open("run_data_preparation.py").read())


class RecommenderEngine(object):

    def productRecommendation(self, user_id):
        """
        1. Filters data by user id first
        2. item_list = any item ever purchase by user (df of transactions)
        3. size_list = any sizes ever purchased per item for items present in item list
        """

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
                    #sys_date = datetime.datetime.now().date()
                    sys_date = datetime.datetime.strptime('2019-11-27','%Y-%m-%d').date()
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
                        freqdata = tempdataset.Frequency.value_counts().index[0] # gets mode
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
                                                                              'Approx_Item_Price': round(price,2),
                                                                              'Frequent_Item': frequent_item,
                                                                              'Reminders': reminders}, ignore_index=True)

        return purchase_pattern_data, user_dict[int(user_id)]

    def getUserPurchaseHistory(self, user_id):

        transaction_data = pd.read_csv("data/user_purchase_history.csv")
        user_transaction_data = transaction_data[(transaction_data['User'] == user_id)].copy()
        return user_transaction_data

    def shopRecommendation(self, user_id):
        transaction_data = pd.read_csv("data/user_purchase_history.csv")
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
                    shop_recommender = shop_recommender.append({'Product': item_dict[int(product)],
                                                                'Size': size,
                                                                'Store': store,
                                                                'Avg_Price': round(mean_price,2),
                                                                'Latest_Price': last_purchased_price,
                                                                'Latest_Price_Updated_On': last_purchased_date.date()},
                                                               ignore_index=True)
                    shop_recommender = shop_recommender.loc[shop_recommender.groupby(['Product', 'Size'])['Latest_Price'].idxmin()]

        return shop_recommender, user_dict[int(user_id)]



class UserModel(object):

    def update(self, request):
        user_removed_recommendations = pd.read_csv("data/user_removed_recommendations.csv")
        user_removed_recommendations = user_removed_recommendations.append({'User': request.args.get('user_id'),
                                                               'Product': request.args.get('product_id'),
                                                               'Size': request.args.get('size'),},
                                                             ignore_index=True)
        user_removed_recommendations.to_csv('data/user_removed_recommendations.csv', index=False, header=True)

    def view(self,user_id):
        user_details = pd.read_csv("data/gen-data-user.csv")
        user_details = user_details[(user_details['id'] == int(user_id))]
        user_details_model = pd.DataFrame()
        user_details_model = user_details_model.append({'user_id': user_id,
                                      'Name': user_details['Name'],
                                      'Gender': user_details['Sex'],
                                      'Age': 2019 - int(user_details['YOB']),
                                      'HouseHold':user_details['Household']}, ignore_index=True)
        user_purchase_model = pd.DataFrame()
        recomEngine = RecommenderEngine()
        user_purchase_data = recomEngine.getUserPurchaseHistory(int(user_id))
        user_purchase_model = self.trainUserPurchaseModel(user_purchase_data)
        return user_details_model, user_purchase_model

    def appplyUserControl(self,user_id,recommendations):

        user_removed_recommendations = pd.read_csv("data/user_removed_recommendations.csv")
        user_removed_recommendations = user_removed_recommendations[(user_removed_recommendations['User'] == int(user_id))].copy()
        ignored_products_list = user_removed_recommendations.Product.unique().tolist()
        for product in ignored_products_list:
            recommendations = recommendations[(recommendations.Product != product)]
        return recommendations

    def trainUserPurchaseModel(self,user_purchase_data):
        productlist = user_purchase_data.Product.unique().tolist()
        traindata = pd.DataFrame()
        for product in productlist:
            productdata = user_purchase_data[(user_purchase_data.Product == product)]
            sizelist = productdata.Size.unique().tolist()
            for size in sizelist:
                tempdata =  productdata[(productdata.Size == size)]
                tempdata['Transaction_Date'] = pd.to_datetime(tempdata.Transaction_Date)
                tempdata = tempdata.sort_values(by=['Transaction_Date'], ascending=True)
                tempdata['Frequency'] = tempdata.Transaction_Date.diff()
                traindata = traindata.append(tempdata)
        traindata.drop(['User', 'Store', 'Transaction_Date', 'Price','WeekDay'], axis = 1, inplace=True)
        traindata = traindata.dropna()
        traindata.Product = traindata.Product.astype(str)
        target = traindata.Frequency.dt.days
        traindata.drop(['Frequency'], axis = 1, inplace=True)
        X_train, X_test, y_train, y_test = train_test_split(traindata, target, test_size=0.1,
                                                    random_state=0)
        ohe = OneHotCategoricalEncoder(top_categories=None,
                                       variables=['Product', 'Size'],
                                       drop_last=True)
        ohe.fit(X_train, y_train)
        X_train = ohe.transform(X_train)
        X_test = ohe.transform(X_test)

        regressor = LinearRegression()
        regressor.fit(X_train, np.log(y_train))
        #xgb_model = xgb.XGBRegressor()
        #eval_set = [(X_test, np.log(y_test))]
        #xgb_model.fit(X_train, np.log(y_train), eval_set=eval_set, verbose=False)

        user_purchase_model = pd.DataFrame()
        user_testdata = pd.DataFrame()
        user_testdata['Product'] = user_purchase_data.Product
        user_testdata['Size'] = user_purchase_data.Size
        user_testdata.Product = user_testdata.Product.astype(str)
        testdata = ohe.transform(user_testdata)
        pred = regressor.predict(testdata)
        pred = np.exp(pred)
        user_purchase_model = user_testdata.copy()
        user_purchase_model["Learned Frequencies"] = np.around(pred)
        #user_purchase_model = user_purchase_model.groupby(['Product', 'Size', 'Learned Frequencies'])
        user_purchase_model = user_purchase_model.drop_duplicates()
        userproductlist = user_purchase_model.Product.unique().tolist()
        for product in userproductlist:
            user_purchase_model.Product = user_purchase_model.Product.replace(product,item_dict[int(product)])
        return user_purchase_model




if __name__ == '__main__':
    testing = UserModel()
    #_,user_purchase_model = testing.view(10002)

    #test, username = testing.productRecommendation(10000)
    #test, username = testing.shopRecommendation(10000)