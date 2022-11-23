from django.urls import path
from goodsapp import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('category/<cid>/', views.IndexView.as_view()),
    path('category/<cid>/page/<num>/', views.IndexView.as_view()),
    path('goodsdetails/<goodsid>/', views.DetailView.as_view()),

]