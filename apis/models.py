

from django.db import models
from  creditcards.models import  CardNumberField

class Users(models.Model):
    #offer = models.ManyToManyField(Offer, through='Bet')
    
    firstname= models.CharField(max_length=50)
    lastname= models.CharField(max_length=50)
    phone= models.CharField(max_length=20)
    email= models.EmailField()
    Password= models.CharField(max_length=20)
    username= models.CharField(max_length=50)


    bankaccount= CardNumberField()
    bankpassword = models.CharField(max_length=20)


    is_confirmed = models.BooleanField(default=False)
    #is_online= models.BooleanField(default=False)
    code= models.DecimalField(max_digits=6,decimal_places=0)  
    
    created= models.DateTimeField(null=True)

    def __str__(self):
        return self.username

class Offer(models.Model):
    seller= models.ForeignKey(Users, on_delete=models.CASCADE)
    #buyer= models.ForeignKey(Users, on_delete=models.CASCADE)

    offername = models.CharField(max_length=50)
    model_year= models.IntegerField()
    brand= models.CharField(max_length=50)
    startingbet= models.DateField()
    endingbet= models.DateTimeField()
    
    imgurl1= models.ImageField()
    imgurl2= models.ImageField()
    imgurl3= models.ImageField()
    imgurl4= models.ImageField()
    imgurl5= models.ImageField()
    imgurl6= models.ImageField()

    initialprice= models.DecimalField(max_digits=20, decimal_places=10)
    finalprice= models.DecimalField(max_digits=20, decimal_places=10,null=True,blank=True)


    def __str__(self):
         return self.seller.username

class Bet(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    ammount= models.DecimalField(max_digits=20, decimal_places=10)
    date= models.DateField()
    is_win= models.BooleanField(default=False)

     
class Bankaccounts(models.Model):
    
    number= CardNumberField()
    password_account= models.CharField(max_length=20)
    phone= models.CharField(max_length=20)
    firstname= models.CharField(max_length=50)
    lastname= models.CharField(max_length=50)
    ammount= models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    address= models.CharField(max_length=100)


    def __str__(self):
        return self.firstname
   

   