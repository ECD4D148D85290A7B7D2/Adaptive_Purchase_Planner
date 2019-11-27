import pandas as pd
import numpy as np
import os

# class User:
#     def __init__(self, id: str, sex: str, name: str, yob: int, household: int, products_yes: list = None, products_no: list = None):
#         super().__init__()
#         self.id = id
#         self.sex = sex
#         self.name = name
#         self.yob = yob
#         self.household = household
#         self.products_yes = products_yes
#         self.products_no = products_no
    
#     id: str
#     sex: str
#     name: str
#     yob: int
#     household: int
#     products_yes: list
#     products_no: list

usermodelfilepath = 'data/user-model.csv'

def get_usermodel_df(force=False):
    if(os.path.isfile(usermodelfilepath)):
        if(force):
            dfUsers = create_usermodel_df()
            dfModel = read_usermodel_df()
            dfdiff = ~dfUsers.id.isin(dfModel.id)
            dfModel.concat(dfUsers[dfdiff], inplace=True)
            save_usermodel_df(dfModel)
    else:
        dfUsers = create_usermodel_df()
        save_usermodel_df(dfUsers)
    
    return read_usermodel_df()


def create_usermodel_df():
    dfUsers = pd.read_csv('data/gen-data-user.csv')
    dfUsers['products_yes'] = 'None'
    dfUsers['products_no'] = 'None'
    return dfUsers


def read_usermodel_df():
    return pd.read_csv(usermodelfilepath, sep='|')


def save_usermodel_df(df):
    df.to_csv(usermodelfilepath, index=False, sep='|')
    
def get_usermodel(userid):
    users = get_usermodel_df()
    user = users[users.id == int(userid)].to_dict('records')
    if(len(user) > 0): 
        returnthing = user[0]
        returnthing['products_no'] =  csvCleanNoneNan(returnthing['products_no'])
        returnthing['products_yes'] =  csvCleanNoneNan(returnthing['products_yes'])
        return returnthing
    else:
        return None
    
def csvCleanNoneNan(val):
    return str(val).replace("None", "").replace("nan", "").split(",")
    
def add_nono_item(userid, product):
    addremove_item(userid, 'products_no', product, remove=False)

def remove_nono_item(userid, product):
    addremove_item(userid, 'products_no', product, remove=True)


def addremove_item(userid, column, items, remove=False):
    users = get_usermodel_df()
    ix = users[users.id == int(userid)].first_valid_index()
    argval = ''
    
    oldval = set(users.get_value(ix, column).split(','))
    if(type(items) is str):
        argval = set()
        argval.add(items)
    else:
        argval = set(items)
    
    newval = set()
    if(remove):
        newval = oldval.difference(argval)
    else:
        newval = oldval.union(argval)
    
    newval.discard('')
    newval.discard('None')
    newval = ','.join(newval)
    
    users.set_value(ix, column, newval)
    
    save_usermodel_df(users)
