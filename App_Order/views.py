from App_Login.models import User
from django.shortcuts import render
from . import models,serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from App_Main.models import DishModel
from django.shortcuts import render, get_object_or_404
import json
from App_Login.models import User,Staff,Customer,AdminProfile,Staff
from App_Main.models import Variants,AddOns
# Create your views here.
# class OrderModelView(viewsets.ModelViewSet):
#     queryset=models.Order.objects.all()
#     serializer_class=serializers.MyOrderSerializer
    
    
#     def update(self, request):
#         print(request.data)
    
    
class CartModelView(viewsets.ModelViewSet):
    queryset=models.Cart.objects.all()
    serializer_class=serializers.MyCartSerializer
    
    
    def create(self,request):
        user=request.data['user'] 
        user=User.objects.get(id=user)  
        customer=Customer.objects.get(user=user)
        product=request.data['product']
        dishes=DishModel.objects.filter(id=product)
        dish=dishes[0]
        cart=models.Cart.objects.get_or_create(
            user=customer,
            dish=dish,
            purchased=False
        )
        order=models.Order.objects.filter(
            user=customer,
            ordered=False,
        )
        if order.exists():
            order=order[0]
            if order.items.filter(dish=dish).exists():
                cart[0].quantity += 1
                cart[0].save()
                order.save()
            else:
                order.cart_items.add(cart[0])
                order.save()
        else:
            order=models.Order.objects.create(
                user=customer,
            ordered=False
            )
            order.cart_items.add(cart[0])
            order.save()    
        return Response({'message':'Product Added To Cart'})
    
@api_view(['GET','POST'])
def increase_dish(request,pk):
    dish = get_object_or_404(DishModel, pk=pk)
    user=get_object_or_404(User,id=request.data['id'],roles='Customer')  
    customer = get_object_or_404(Customer, user=user)
    cart=models.Cart.objects.get_or_create(dish=dish,user=customer,purchased=False)
    order=models.Order.objects.filter(user=customer,ordered=False)
    if order.exists():
        order=order[0]
        if order.items.filter(dish=dish).exists():
            cart[0].quantity+=1
            cart[0].save()
            order.save()
        else:
            order.items.add(cart[0])
            order.save()
    else:
        order=models.Order.objects.create(user=customer,ordered=False)
        order.save()
        order.items.add(cart[0])
        order.save()
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request}) 
    return Response({'order':orderserializer.data})
@api_view(['PUT','GET'])
def add_coupon(request,pk):
    user=get_object_or_404(User,id=pk,roles='Customer')  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=False)
    mycoupon=request.data['coupon']
    coupon=models.Coupon.objects.filter(code=mycoupon)
    if coupon.exists():
        coupon=coupon[0]
        if order.exists():
            order=order[0]
            order.coupon=coupon
            order.save()
        return Response({'coupon':True})        
    else:
        return Response({'coupon':'Check Your Coupon. It is invalid '})        
@api_view(['PUT','GET'])
def add_address(request,pk):
    user=get_object_or_404(User,id=pk,roles='Customer')  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=False)
    myaddress=request.data['address']    
    if order.exists():
        order=order[0]
        order.shipping_address=myaddress
        order.save()
        return Response({'status':True})        
    else:
        return Response({'status':False})        
    
@api_view(['GET','POST'])
def my_cart(request,pk):
    user=get_object_or_404(User,id=pk,roles='Customer')  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=False)
    if order.exists():
        order=order[0]
        orderserializer=serializers.MyOrderSerializer(order,context={'request': request})
        return Response({'order':orderserializer.data})
    else:
        return Response({'order':False})
@api_view(['GET','POST'])
def add_variant_addons(request,pk):
    user=get_object_or_404(User,id=pk,roles='Customer')  
    customer = get_object_or_404(Customer, user=user)
    cart=models.Cart.objects.filter(user=customer,dish=request.data['dish'],purchased=False)
    order=models.Order.objects.filter(user=customer,ordered=False)
    dish_addons=json.loads(request.data['dish_addons'])
    dish_variants=json.loads(request.data['dish_variants'])
    print(dish_addons)
    print(dish_variants)
    if cart.exists():
        cart=cart[0]
        for i in dish_addons:
            addons=AddOns.objects.filter(name=i)
            if addons:
                cart.dish_addons.add(addons[0])
                cart.save()
        for i in dish_variants:
            variants=Variants.objects.filter(variant_name=i)
            if variants:
                cart.dish_variants.add(variants[0])
                cart.save()
        
        cartserializer=serializers.MyCartSerializer(cart,context={'request': request})
        return Response({'order':cartserializer.data})
    else:
        return Response({'order':False})
    
@api_view(['GET','POST'])
def my_orders(request,pk):
    user=get_object_or_404(User,id=pk,roles='Customer')  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=True)
    if order.exists():
        orderserializer=serializers.MyOrderSerializer(order,context={'request': request},many=True)
        return Response({'order':orderserializer.data})
    else:
        return Response({'order':False})
    
@api_view(['GET','POST'])
def all_orders(request):
    order=models.Order.objects.all().exclude(ordered=False)
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request},many=True)
    return Response(orderserializer.data)
    
@api_view(['GET','POST'])
def order_by_id(request,pk):
    order=models.Order.objects.filter(id=pk)
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request},many=True)
    return Response(orderserializer.data)
    

@api_view(['GET','POST'])
def order_Assigned_to(request,pk):
    user=get_object_or_404(User,id=pk,roles='Employee')  
    staff = get_object_or_404(Staff, user=user)
    order=models.Order.objects.filter(assigned_to=staff,delivered=False)
    orderserializer=serializers.MyStaffOrderSerializer(order,context={'request': request},many=True)
    return Response(orderserializer.data)
    
@api_view(['GET','POST'])
def staff_prvious_orders(request,pk):
    user=get_object_or_404(User,id=pk,roles='Employee')  
    staff = get_object_or_404(Staff, user=user)
    order=models.Order.objects.filter(assigned_to=staff,delivered=True)
    orderserializer=serializers.MyStaffOrderSerializer(order,context={'request': request},many=True)
    return Response(orderserializer.data)
    
    
@api_view(['GET','POST','PUT'])
def order_by_id_edit(request,pk):
    user=get_object_or_404(User,email=request.data['user'],roles='Customer')  
    customer = Customer.objects.get(user=user)

    order=models.Order.objects.filter(id=pk,user=customer,ordered=True)
    
    if order:
        order=order[0]
        order.order_status=request.data['order_status']
        order.delivered=request.data['delivered']
        order.delivery_charge=request.data['delivery_charge']

        user2=get_object_or_404(User,id=request.data['assigned_to'],roles='Employee')  
        employee = Staff.objects.get(user=user2)
        order.assigned_to=employee
        order.save()
    return Response({'status':True})
    
@api_view(['GET','POST'])
def checkout(request,pk):
    user=get_object_or_404(User,id=pk,roles='Customer')  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=False)
    if order.exists():
        order=order[0]
        cart=models.Cart.objects.filter(user=customer,purchased=False)
        if cart:
            cart=cart[0]
        order.ordered=True
        cart.purchased=True
        cart.save()
        order.save()
    return Response({'status':'ok'})

@api_view(['GET','POST'])
def decrease_dish(request,pk):
    dish = get_object_or_404(DishModel, pk=pk)
    user=get_object_or_404(User,id=request.data['id'],roles='Customer')  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=False)
    if order.exists():
        order=order[0]
        if order.items.filter(dish=dish).exists():
            cart=models.Cart.objects.filter(dish=dish,user=customer,purchased=False)
            cart=cart[0]
            if cart.quantity>1:
                    cart.quantity-=1
                    cart.save()
            else:
                    order.items.remove(cart)
                    cart.delete()
                    cart.save()
                    order.save()      
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request}) 
    return Response({'order':orderserializer.data})


@api_view(['GET','POST'])
def staff_change_status(request,pk):
    user=get_object_or_404(User,id=pk,roles='Employee')  
    staff = get_object_or_404(Staff, user=user)
    order=models.Order.objects.filter(id=request.data['order_id'],assigned_to=staff,delivered=False)
    if order:
        myorder=order[0]
        myorder.order_status=request.data['order_status']
        myorder.delivered=request.data['delivered']
        myorder.save()
        return Response({'response':'true'})
    else:
        return Response({'response':'false'})