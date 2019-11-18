from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .recommendation_helper import RecommenderEngine
from .recommendation_helper import AddProduct
from .sys_constant import ignored, today
@csrf_exempt
@api_view(['POST'])
def addItem(request):

    if request.data['user_id'] == '' or 'product_id' not in request.POST or request.data['product_id'] == '' or request.data['size'] == '' or request.data['price'] == ''\
             or request.data['store'] == '' or request.data['transaction_date'] == '' or request.data['weekday'] == '':
        return Response({"message": "All fields are mandatory!"})
    else:
        additem = AddProduct()
        additem.addUserPurchase(request)
        return Response({"message": "Product Added Successfully!"})

@csrf_exempt
@api_view(['POST'])
def buyToday(request):

    if 'user_id' not in request.POST or request.data['user_id'] == '':
        return Response({"message": "invalid_user_id", "data": request.data['user_id']})
    else:
        recommend = RecommenderEngine()
        user_id = request.data['user_id']
        recommendations, username = recommend.productRecommendation(user_id)
        recommendations = recommendations[(recommendations.Days_Left == today)]

        return Response({"data": recommendations, 'username': username})

@csrf_exempt
@api_view(['POST'])
def buyLater(request):

    if 'user_id' not in request.POST or request.data['user_id'] == '':
        return Response({"message": "invalid_user_id", "data": request.data['user_id']})
    else:
        recommend = RecommenderEngine()
        user_id = request.data['user_id']
        recommendations, username = recommend.productRecommendation(user_id)
        recommendations = recommendations[(recommendations.Days_Left > today)]

        return Response({"data": recommendations, 'username': username})

@csrf_exempt
@api_view(['POST'])
def ignoredRecommendations(request):

    if 'user_id' not in request.POST or request.data['user_id'] == '':
        return Response({"message": "invalid_user_id", "data": request.data['user_id']})
    else:
        recommend = RecommenderEngine()
        user_id = request.data['user_id']
        recommendations, username = recommend.productRecommendation(user_id)
        recommendations = recommendations[(recommendations.Days_Left == ignored)]

        return Response({"data": recommendations, 'username': username})

@csrf_exempt
@api_view(['POST'])
def bestBuys(request):

    if 'user_id' not in request.POST or request.data['user_id'] == '':
        return Response({"message": "invalid_user_id", "data": request.data['user_id']})
    else:
        recommend = RecommenderEngine()
        user_id = request.data['user_id']
        recommendations, username = recommend.shopRecommendation(user_id)
        return Response({"data": recommendations, 'username': username})

@csrf_exempt
@api_view(['POST'])
def to_be_added_by_Jiajin(request):

    if 'user_id' not in request.POST or request.data['user_id'] == '':
        return Response({"message": "invalid_user_id", "data": request.data['user_id']})
    else:
        recommend = RecommenderEngine()
        user_id = request.data['user_id']
        recommendations, username = recommend.shopRecommendation(user_id)
        return Response({"data": recommendations, 'username': username})