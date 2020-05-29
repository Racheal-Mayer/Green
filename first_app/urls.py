from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('about', views.about),
    path('blog', views.blog),
    path('shop', views.shop),
    path('adduser', views.adduser),
    path('login', views.login),
    path('post_message', views.post_message),	
    path('post_comment/<messageid>', views.post_comment),  
    path('destroy', views.destroy),
    path('checkout', views.checkout),
    path('additem', views.additem),
    path('deleteit/<int:itemId>', views.deleteItem),
    path('delete/<int:messageid>', views.deleteMessage),
    path('deletecm/<int:postid>', views.deleteComment),
]