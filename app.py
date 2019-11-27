from flask import Flask, request, make_response
from flask_cors import CORS
from datetime import datetime
import re
from flask import jsonify

import user_things as ut
from recommendation_helper import RecommenderEngine
from recommendation_helper import AddProduct , UserModel
from sys_constant import ignored, today
from stereotype import Stereo

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "API for Adaptive Applications by Team James!"


# Weird URI to prevent accidental
@app.route("/regen/<name>")
def hello_there(name):
    returnVal = "Skipped!"
    if(name == "bond"):
        exec(open("run_data_preparation.py").read())
        return "Regenerated!"

    return returnVal


# @api_view(['POST'])
@app.route("/purchase", methods=['POST'])
def addItem():
    if 'user_id' not in request.args:
        return {"message": "All fields are mandatory!"}
    else:
        additem = AddProduct()
        additem.addUserPurchase(request)
        return {"message": "Product Added Successfully!"}


# @csrf_exempt
# @api_view(['POST'])
@app.route("/recommendations/today", methods=['GET'])
def buyToday():

    filterParam = 'user_id'
    if filterParam not in request.args or request.args[filterParam] == '':
        return {"message": "invalid_user_id", "data": request.args[filterParam]}
    else:
        recommend = RecommenderEngine()
        user_id = request.args[filterParam]
        recommendations, username = recommend.productRecommendation(user_id)
        recommendations = recommendations[(recommendations.Days_Left == today)]
        userControl = UserModel()
        recommendations = userControl.appplyUserControl(user_id, recommendations)
        return {"data": recommendations.to_dict('records'), 'username': username}

# @api_view(['POST'])
@app.route("/recommendations/later", methods=['GET'])
def buyLater():

    filterParam = 'user_id'
    if filterParam not in request.args or request.args[filterParam] == '':
        return {"message": "invalid_user_id", "data": request.args[filterParam]}
    else:
        recommend = RecommenderEngine()
        user_id = request.args[filterParam]
        recommendations, username = recommend.productRecommendation(user_id)
        recommendations = recommendations[(recommendations.Days_Left > today)]
        userControl = UserModel()
        recommendations = userControl.appplyUserControl(user_id,recommendations)

        return {"data": recommendations.to_dict('records'), 'username': username}

# @csrf_exempt
# @api_view(['POST'])
@app.route("/recommendations/ignored", methods=['GET'])
def ignoredRecommendations():

    filterParam = 'user_id'
    if filterParam not in request.args or request.args[filterParam] == '':
        return {"message": "invalid_user_id", "data": request.args[filterParam]}
    else:
        recommend = RecommenderEngine()
        user_id = request.args[filterParam]
        recommendations, username = recommend.productRecommendation(user_id)
        recommendations = recommendations[(recommendations.Days_Left == ignored)]
        userControl = UserModel()
        recommendations = userControl.appplyUserControl(user_id,recommendations)

        return {"data": recommendations.to_dict('records'), 'username': username}

# @csrf_exempt
# @api_view(['POST'])
@app.route("/recommendations/shop", methods=['GET'])
def bestBuys():

    filterParam = 'user_id'
    if filterParam not in request.args or request.args[filterParam] == '':
        return {"message": "invalid_user_id", "data": request.args[filterParam]}
    else:
        recommend = RecommenderEngine()
        user_id = request.args[filterParam]
        recommendations, username = recommend.shopRecommendation(user_id)
        return {"data": recommendations.to_dict('records'), 'username': username}

# @csrf_exempt
# @api_view(['POST'])
@app.route("/recommendations/stereo/predict", methods=['GET'])
def stereotypePredict():
    if request.args['user_id'] == '':
        return {"message": "invalid_user_id", "data": request.args['user_id']}
    else:
        user_id = int(request.args['user_id'])
        s = Stereo()
        try:
            s.loadModel()
        except:
            return jsonify({"code":1,"data":"please build model first"})
        res = s.predict(user_id)
        #return Response(res)
        return jsonify(res)

@app.route("/recommendations/stereo/build", methods=['GET'])
def stereotypeBuild():
    s = Stereo()
    res = s.trainModel()
    #return Response(res)
    return jsonify(res)

@app.route("/usermodel/view", methods=['GET'])
def getUserModel():

    filterParam = 'user_id'
    if filterParam not in request.args or request.args[filterParam] == '':
        return {"message": "invalid_user_id", "data": request.args[filterParam]}
    else:
        userModel = UserModel()
        recommend = RecommenderEngine()
        user_id = request.args[filterParam]
        recommendations, username = recommend.productRecommendation(user_id)
        recommendations.drop(['Approx_Item_Price', 'Days_Left', 'Last_Purchased', 'Product', 'Frequent_Item','Reminders','User','Preferred_Shopping_Weekday','Preferred_Store'], axis = 1, inplace=True)
        user_details_model, user_purchase_model = userModel.view(user_id)
        return {"userPurchaseModelAlgorithmic": recommendations.to_dict('records'),
                "usermodel":user_details_model.to_json(orient='records'),
                "userPurchaseModelML":user_purchase_model.to_dict('records')}

@app.route("/usermodel/update", methods=['POST'])
def updateUserModel():

    if 'user_id' not in request.args or 'product_id' not in request.args or 'size' not in request.args:
        return {"message": "All fields are mandatory!"}
    else:
        userModel = UserModel()
        userModel.update(request)
        return {"message": "User Model Updated Successfully!"}


#if __name__ == '__main__':
#    app.run(debug=True)