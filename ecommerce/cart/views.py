from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Product

from cart.models import Cart, Account, Order

from cart.serializers import CartSerializer

from cart.serializers import OrderSerializer


# Create your views here.

# @login_required
# def cartview(request):
#     total=0
#     u=request.user
#     cart=Cart.objects.filter(user=u)
#     for i in cart:
#         total+=i.quantity*i.product.price
#     return render(request,'cartview.html',{'c':cart,'total':total})


class Cartview(APIView):

        permission_classes = [IsAuthenticated,]

        def get(self, request):

            u=self.request.user

            cart=Cart.objects.filter(user=u)
            c=CartSerializer(cart,many=True)

            return Response(c.data)



# @login_required
# def addtocart(request,n):
#     p=Product.objects.get(name=n)
#     u=request.user
#     try:
#         cart=Cart.objects.get(user=u,product=p)
#         if(p.stock > 0):
#             cart.quantity+=1
#             cart.save()
#             p.stock -= 1
#             p.save()
#
#     except:
#         if(p.stock>0):
#             cart=Cart.objects.create(product=p,user=u,quantity=1)
#             cart.save()
#             p.stock-=1
#             p.save()
#
#     return redirect('cart:cartview')

class Addtocart(APIView):
    permission_classes=[IsAuthenticated,]
    def get(self,request,pk):
        p = Product.objects.get(pk=pk)
        u=self.request.user
        try:
            cart=Cart.objects.get(user=u,product=p)
            if(p.stock > 0):
                    cart.quantity+=1
                    cart.save()
                    p.stock -= 1
                    p.save()

        except:
            if(p.stock>0):
                    cart=Cart.objects.create(product=p,user=u,quantity=1)
                    cart.save()
                    p.stock-=1
                    p.save()

            return Response(status=status.HTTP_201_CREATED)



# @login_required
# def removecart(request,n):
#     p = Product.objects.get(name=n)
#     u = request.user
#     try:
#         cart = Cart.objects.get(user=u, product=p)
#         if (cart.quantity >1):
#             cart.quantity -= 1
#             cart.save()
#             p.stock +=1
#             p.save()
#         else:
#             cart.delete()
#             p.stock += 1
#             p.save()
#     except:
#         pass
#     return cartview(request)

class Removecart(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self,request,pk):

        p = Product.objects.get(pk=pk)
        u = self.request.user
        try:
            cart = Cart.objects.get(user=u, product=p)
            if (cart.quantity >1):
                cart.quantity -= 1
                cart.save()
                p.stock +=1
                p.save()
            else:
                cart.delete()
                p.stock += 1
                p.save()
        except:
            pass
        return Response(status=status.HTTP_200_OK)


# @login_required
# def full_remove(request,n):
#     p = Product.objects.get(name=n)
#     u = request.user
#     try:
#         cart = Cart.objects.get(user=u, product=p)
#
#         cart.delete()
#         p.stock += cart.quantity
#         p.save()
#     except:
#         pass
#     return cartview(request)


class full_remove(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request,pk):
        p = Product.objects.get(pk=pk)
        u = request.user
        try:
            cart = Cart.objects.get(user=u, product=p)

            cart.delete()
            p.stock += cart.quantity
            p.save()
        except:
            pass
        return Response(status=status.HTTP_200_OK)


# @login_required
# def orderform(request):
#     if request.method=="POST":
#         a=request.POST['a']
#         p = request.POST['p']
#         n = request.POST['n']
#         u=request.user
#         cart=Cart.objects.filter(user=u)
#         total=0
#         for i in cart:
#             total+=i.quantity*i.product.price
#         try:
#             ac=Account.objects.get(acctnum=n)#to retrive the acctobject
#             if ac.amount>= total:
#                 ac.amount=ac.amount-total
#                 ac.save()
#                 for i in cart:
#                     o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
#                     o.save()
#                 cart.delete()
#                 msg="your order placed successfully"
#                 return render(request,"orderdetail.html",{'msg':msg})
#
#             else:
#                 msg="insufficient amount,you can't place order"
#                 return render(request, "orderdetail.html", {'msg': msg})
#         except:
#             pass
#
#     return render(request,'orderform.html')


class orderform(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        a = request.data.get('address')
        p = request.data.get('phone')
        n = request.data.get('acctnum')

        u = self.request.user

        cart = Cart.objects.filter(user=u)

        total = 0
        for i in cart:
            total += i.quantity * i.product.price

        try:
            num = int(n)
            ac = Account.objects.get(acctnum=num)

            if (ac.amount >= total):
                ac.amount = ac.amount - total
                ac.save()
                for i in cart:
                    o = Order.objects.create(user=u, product=i.product, address=a, phone=p, no_of_items=i.quantity,
                                             order_status="paid")
                    o.save()
                cart.delete()

                return Response({"msg": "Created"}, status=status.HTTP_201_CREATED)
            else:

                return Response({"msg": "Insufficient"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            pass

# @login_required
# def orderview(request):
#     u=request.user
#     o=Order.objects.filter(user=u)
#
#     return render(request,'orderview.html',{'o':o,'u':u})

class orderview(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        u=self.request.user
        order= Order.objects.filter(user=u)
        c = OrderSerializer(order, many=True)
        return Response(c.data)