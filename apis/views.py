
import base64
import smtplib
from venv import create
from django.core.files.base import ContentFile
from random import randint
from datetime import datetime
import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from . models import Bankaccounts, Offer, Users, Bet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import *
from django.core.mail import send_mail
from datetime import date
from django.db.models import Max ,Count

def toJSON(p):
    return json.loads(json.dumps(p, default=lambda o: o.dict))

















@api_view(['POST'])
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)


    username=body['username']
    password=body['password']

    try:
        p=Users.objects.get(username=username,Password=password,is_confirmed=True)
        mywallet = Bankaccounts.objects.get(number=p.bankaccount)
        bankaccount = mywallet.number
        ammount = mywallet.ammount
        created = p.created
        created = created.strftime("%Y")

        return JsonResponse({'result':'ok',
                             'username':username,
                             'password':password,
                             'ammount':ammount,
                             'bankaccount':bankaccount,
                            'email':p.email,
                            'firstname':p.firstname,
                            'lastnane':p.lastname,
                            'phone':p.phone,
                            'member_since':created
                            })

    except:

        return JsonResponse({'result':'invalid'})

@api_view(['POST'])
def signup(request):
      body_unicode = request.body.decode('utf-8')
      body = json.loads(body_unicode)
      firstname= body['firstname']
      lastname= body['lastname']
      email= body['email']
      bankaccount= body['bankaccount']
      bankpassword= body['bankpassword']
      username=body['username']
      password=body['password']
      phone=body['phone']

      try:
          #u= Users.objects.get(username=username,bankaccount=bankaccount)
          if not  Users.objects.all().filter(username=username,bankaccount=bankaccount).exists():
            code = randint(10**(6-1),(10**6)-1)
            new_user= Users()
            new_user.firstname= firstname
            new_user.lastname= lastname
            new_user.email=email
            new_user.bankaccount=bankaccount
            new_user.bankpassword= bankpassword
            new_user.username= username
            new_user.Password=password
            new_user.phone= phone
            new_user.code=code
            new_user.is_confirmed=False

            new_user.created=datetime.now()
            # print(datetime.now())
            new_user.save()
            send_mail(
            'Confirm to Sign up in W_BID',
            'Hey Dude, this is yor code    '+str(code),
            'wbid66@gmail.com',
            [email],
            fail_silently=False,
                     )
            return JsonResponse({'result':'ok'
            ,'username':username
            ,'password':password

                                })
          else:
               return JsonResponse({'result':'invalid'
               ,'message':'User is already exists'
                                  })


      except:



          return JsonResponse({'result':'invalid'})

@api_view(['POST'])
def confirm(request):
     body_unicode = request.body.decode('utf-8')
     body = json.loads(body_unicode)
     code=body['code']
     username= body['username']

     try:
      if Users.objects.all().filter(username=username,code=code).exists():

          u = Users.objects.get(username=username,code=code)
          u.is_confirmed=True
          u.save()
          return JsonResponse({'result':'ok'})

      else:
          return JsonResponse({'result':'invalid','message':'not confirmed'})

     except:
         return JsonResponse({'result':'invalid'})

@api_view(['POST'])
def profile(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email= body['email']

    try:
       u=Users.objects.get(email=email)
       created = u.created
       created = created.strftime("%Y")


       return JsonResponse({'email':email,
       'Number':u.phone,
       'Member_since':created,
       'firstname':u.firstname,
       'lastname':u.lastname
                           })

    except:
        return JsonResponse({'result':'invalid'})

@api_view(['POST'])
def wallet(request):
     body_unicode = request.body.decode('utf-8')
     body = json.loads(body_unicode)
     username=body['username']
     try:

         u= Users.objects.get(username=username)
         mywallet = Bankaccounts.objects.get(number=u.bankaccount, password_account=u.bankpassword)
         bankaccount = mywallet.number
         ammount = mywallet.ammount
         return JsonResponse({
              'result':'ok'
             ,'bankaccount':bankaccount
             ,'ammount':ammount
                             })
     except:
         return JsonResponse({'result':'invalid'})

@api_view(['POST'])
def add_offer(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    offername = body['productname']
    brand = body['brand']
    yearmodel = body['yearmodel']
    initial_price = body['minimum_price']
    startingbet= body['auction_start_time']
    endingbet= body['auction_end_time']
    username = body['username']
    imgurl1=body['imgurl1']
    imgurl1=ContentFile(base64.b64decode(imgurl1),'name')
    imgurl2=body['imgurl2']
    imgurl2=ContentFile(base64.b64decode(imgurl2),'name')
    imgurl3=body['imgurl3']
    imgurl3=ContentFile(base64.b64decode(imgurl3),'name')
    imgurl4=body['imgurl4']
    imgurl4=ContentFile(base64.b64decode(imgurl4),'name')
    imgurl5=body['imgurl5']
    imgurl5=ContentFile(base64.b64decode(imgurl5),'name')
    imgurl6=body['imgurl6']
    imgurl6=ContentFile(base64.b64decode(imgurl6),'name')

    try:
        new_offer= Offer()
        new_offer.offername = offername
        new_offer.brand = brand
        new_offer.model_year = yearmodel
        new_offer.startingbet = startingbet
        new_offer.endingbet = endingbet
        new_offer.initialprice = initial_price
        new_offer.imgurl1 = imgurl1
        new_offer.imgurl2 = imgurl2
        new_offer.imgurl3 = imgurl3
        new_offer.imgurl4 = imgurl4
        new_offer.imgurl5 = imgurl5
        new_offer.imgurl6 = imgurl6
        new_offer.seller = Users.objects.get(username=username)
        new_offer.save()
        return JsonResponse({'result':'ok'})


    except:

        return JsonResponse({'result':'invalid'})



@api_view(['POST'])
def see_more(request):
     body_unicode = request.body.decode('utf-8')
     body = json.loads(body_unicode)
     offername = body['offername']
     try:
         myoffer = Offer.objects.get(offername=offername)
        #  seller =myoffer.seller.firstname +' '+ myoffer.seller.lastname
         numberOfBiding = Bet.objects.filter(offer=myoffer).count()
         topBidValue = Bet.objects.filter(offer=myoffer).aggregate(Max('ammount'))
        #  numberOfParticipants = Bet.objects.filter(offer=myoffer).annotate( Count('user'),distinct=True)
         

        #  cursor = connection.cursor()
        #  cursor.execute("SELECT max(ammount) FROM apis_num ")
        #  nop = cursor.fetchone()

        #  print(numberOfParticipants.num)
         return JsonResponse({'result':'ok'
                              ,'nameOfProduct':myoffer.offername
                              ,'numberOfBiding':numberOfBiding
                              ,'topBidValue':topBidValue['ammount__max']
         })
     except:
         return JsonResponse({'result':'invalid'})

@api_view(['GET'])
def happening_now(request):
    #now = datetime.now()
    #todayy = now.strftime("%Y-%m-%d")
    
    try:
         today = date.today()
         array = Offer.objects.all()
         res=[]
 
         for arr in array:
            if arr.startingbet >=today:
                 print(arr.startingbet)
                 x = {
                'offername':arr.offername,
                'year':arr.model_year,
                'brand':arr.brand,
                'initialprice':arr.initialprice,
                'seller_profile':arr.seller.firstname +' '+arr.seller.lastname
                     }
                 res.append(x)
          
         return JsonResponse({'result':'ok','data':res})
    except:
             return JsonResponse({'result':'No offer for Bidding'})

@api_view(['POST'])
def add_to_bid(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['username']
    ammount = body['ammount']
    offername = body['offername']


    try:
        user  = Users.objects.get(username=username)
        offer = Offer.objects.get(offername=offername)
        if offer.seller == user:
            return JsonResponse({'result':'invalid','message':'your cannot bid on this offer '})
        new_bet = Bet()

        new_bet.user = user
        new_bet.offer = offer
        new_bet.ammount = ammount
        now = datetime.now()
        new_bet.date = now.strftime("%Y-%m-%d %H:%M:%S")
        new_bet.save()
        return JsonResponse({'result':'ok',
                             'ammount':ammount
                           })
    except:
         return JsonResponse({'result':'invalid',
                              'message':'Sorry, offer is ended'
                            })



@api_view(['POST'])
def forget_password(request):
      body_unicode = request.body.decode('utf-8')
      body = json.loads(body_unicode)
      email = body['email']
      newpass = body['password']
      try:

        user = Users.objects.get(email=email, is_confirmed=True)
        code = user.code
        user.password = newpass
        user.is_confirmed = False
        send_mail(
            'Confirm to change your Password',
            'Hey Dude, this is yor code    '+str(code),
            'wbid66@gmail.com',
            [email],
            fail_silently=False,
        )

        return JsonResponse({'result':'ok'})

      except:
          return JsonResponse({'result':'invalid',
                                'message':'you have not any account on your email'})
@api_view(['POST'])
def confirm_password(request):
      body_unicode = request.body.decode('utf-8')
      body = json.loads(body_unicode)
      email = body['email']
      code  = body['code']
      try:
         user = Users.objects.get(email=email,code=code)
         user.is_confiremed=True
         return JsonResponse({'result':'ok'})
      except:
          return JsonResponse({'result':'invalid',
                                'message':'your code is not valid Please Try again'})



@api_view(['POST'])
def payment(request):
      body_unicode = request.body.decode('utf-8')
      body = json.loads(body_unicode)
      username = body['username']
      try:
        user = Users.objects.get(username=username)
        myBets = Bet.objects.filter(user=user)
        res =[]
        for bet in myBets:
            if bet.is_win == True:
                sellerName = bet.offer.seller.firstname + ' '+ bet.offer.seller.lastname
                x = {
                    'Name':bet.offer.offername,
                    'price':bet.offer.finalprice,
                    'Date':bet.offer.endingbet,
                    'seller':sellerName
                    }
                res.append(x)
        return JsonResponse({'result':'ok','data':res})
      except:
         return JsonResponse({'result':'invalid'})


@api_view(['POST'])
def payout(request):
     body_unicode = request.body.decode('utf-8')
     body = json.loads(body_unicode)
     username = body['username']

     try:
        user = Users.objects.get(username=username)
        myOffers = Offer.objects.filter(seller=user)
        res=[]
        for bet in Bet.objects.all():
            if bet.is_win == True and bet.offer in myOffers and bet.user != user:

                    x = {
                        'Name':bet.offer.offername,
                        'price':bet.offer.finalprice,
                        'Date':bet.offer.endingbet,
                        'buyer':bet.user.firstname +' '+bet.user.lastname
                        }
                    res.append(x)
        return JsonResponse({'result':'ok','data':res})
     except:
         return JsonResponse({'result':'invalid'})
