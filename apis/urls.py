import imp
from django.urls import path
from . import views


urlpatterns = [
    path('login',views.login, name='login'),
    path('signup',views.signup,name='signup'),
    path('confirm',views.confirm,name='confirm'),
    path('profile',views.profile,name='profile'),
    path('wallet',views.wallet,name='wallet'),
    path('see_more',views.see_more,name='see_more'),
    path('happening_now',views.happening_now,name='happening_now'),
    path('add_offer',views.add_offer,name='add_offer'),
    path('add_to_bid',views.add_to_bid,name='add_to_bid'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('confirm_password',views.confirm_password,name='confirm_password'),
    path('payment',views.payment,name='payment'),
    path('payout',views.payout,name='payout')
]