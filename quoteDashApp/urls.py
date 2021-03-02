from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('quotes', views.quotes),
    path('addUser', views.addUser),
	path('logout', views.logout),
	path('login', views.login),
    path('addQuote', views.addQuote),
    path('viewQuotes/<int:userid>', views.viewQuotes),
    path('myaccount/<int:userid>', views.viewAccount),
    path('editProfile/<int:userid>', views.editProfile),
    path('likeThis/<int:quoteid>', views.likeThis)
]