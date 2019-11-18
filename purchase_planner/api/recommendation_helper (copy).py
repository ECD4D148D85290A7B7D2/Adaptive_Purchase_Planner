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

#from APP.models import Purchases
import datetime
import pandas as pd


class RecommenderEngine(object):

    def productRecommendation(self, user_id):

        user_purchase_data = pd.DataFrame(list(Purchases.objects.filter(user_id=user_id).values()))
        user_purchase_data = user_purchase_data.drop('id', axis=1)
        print(user_purchase_data.columns)
        user_purchase_data['purchase_Date'] = pd.to_datetime(user_purchase_data.purchase_date)
        user_purchase_data['day_of_week'] = user_purchase_data['purchase_Date'].dt.weekday_name

        itemlist = user_purchase_data.item.unique().tolist()
        recommen_data = pd.DataFrame(
            columns=['user_id', 'item', 'purchase_freq', 'day_freq', 'store_freq', 'last_purchased', 'days_left',
                     'approx_price'])

        for item in itemlist:
            temp_dataset = user_purchase_data[(user_purchase_data['item'] == item)]
            freq_day_of_week = temp_dataset.day_of_week.value_counts().index[0]
            temp_dataset['PurchaseDate_dt_diff'] = temp_dataset.purchase_Date.diff()
            freq_data = temp_dataset.PurchaseDate_dt_diff.value_counts().index[0] # mode
            purchase_freq = freq_data.days
            last_purchase_date = temp_dataset.purchase_Date.iloc[-1]
            freq_store = temp_dataset.store.value_counts().index[0] # mode
            sys_date = sys_date = datetime.datetime.now().date()
            last_purchase_date = last_purchase_date.date()
            days_diff = (sys_date - last_purchase_date).days
            approx_price = temp_dataset.price.mean()
            if days_diff < purchase_freq:
                days_left = purchase_freq - days_diff
            else:
                days_left = 'Already Out of Stock'
            recommen_data = recommen_data.append({'user_id': user_id,
                                                  'item': item,
                                                  'purchase_freq': purchase_freq,
                                                  'day_freq': freq_day_of_week,
                                                  'store_freq': freq_store,
                                                  'last_purchased': last_purchase_date,
                                                  'days_left': days_left,
                                                  'approx_price': approx_price}, ignore_index=True)


        return recommen_data.to_json(orient='index', date_format='iso')


if __name__ == '__main__':
    obj = Recommender()
    obj.recommendItems()
