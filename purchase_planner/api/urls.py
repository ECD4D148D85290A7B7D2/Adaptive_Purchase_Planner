from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'api/v1/additem/', views.addItem),
    url(r'api/v1/buytoday/', views.buyToday),
    url(r'api/v1/buylater/', views.buyLater),
    url(r'api/v1/ignored/', views.ignoredRecommendations),
    url(r'api/v1/bestbuys/', views.bestBuys),
    url(r'api/v1/TOBEADDEDBYJIAJIN/', views.to_be_added_by_Jiajin),
]
