from django.contrib import admin
from .models import Users, Offer, Bet, Bankaccounts
# Register your models here.
admin.site.register(Users)
admin.site.register(Offer)
admin.site.register(Bet)
admin.site.register(Bankaccounts)
