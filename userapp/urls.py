from django.urls import path
from userapp import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('center/', views.CenterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('loadCode/', views.LoadCodeView.as_view()),
    path('checkCode/', views.CheckCodeView.as_view()),
    path('logout/', views.Logout.as_view()),
    path('address/', views.AddressView.as_view()),
    path('loadAddr/', views.loadAddr),
]