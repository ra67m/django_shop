from django.urls import path
from orderapp import views

urlpatterns=[
    path('',views.order_view),
    path('toOrder/',views.toOrder),
]