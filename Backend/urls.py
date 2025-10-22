from django.urls import path
from .views import *

urlpatterns = [
    path('index/',IndexPage,name='index'),
    path('register/',SingupView.as_view(),name='register'),
    path('login/',LoginUser,name='login'),
    path('logout/',LogoutUser,name='logout'),
    path('collections/<str:name>',ProductCollections,name='collections'),
    path('product/<str:name>/<str:product>',ProductView,name='product'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('cart/',CartView.as_view(),name='cart'),
    path('addcart/<int:pid>',AddCart.as_view(),name='addcart'),
    path('deletecart/<int:id>',DeleteCart.as_view(),name='deletecart'),
    path('favourite/',FavouritView.as_view(),name='favourite'),
    path('togglefavourite/<int:pid>',ToggleFavourite.as_view(),name='togglefavourite'),
    path('payment/<str:all>',PaymentView.as_view(),name='payment'),
    path('success/',SuccessView.as_view(),name='success'),
]