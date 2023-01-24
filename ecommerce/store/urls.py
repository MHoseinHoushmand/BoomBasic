from django.urls import path
from . import views

urlpatterns = [
    path('', views.store , name="store"),
    path('cart/', views.cart , name="cart"),
    path('checkout/', views.checkout , name="checkout"),
    path('login/', views.loginPage , name="login"),
    path('register/', views.registerPage , name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('addorder/<str:pk>/', views.addOrder, name="add_order"),
    path('deleteorder/<str:pk>/', views.deleteOrder, name="delete_order"),
    #path('addAddress/', views.addShoppingAddress, name="add_shopping_address")
]