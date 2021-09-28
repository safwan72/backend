from django.views.decorators.csrf import requires_csrf_token
from rest_framework import serializers
from . import models
from App_Login.serializers import UserSerializer,CustomerProfileSerializer,StaffProfileSerializer,CustomCustomerSerializer
from App_Main.serializers import VariantSerializer,AddOnSerializer,StaffDishModelSerializer

class MyCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon
        fields = "__all__"
        depth=1
        

class MyCartSerializer(serializers.ModelSerializer):
    user=CustomerProfileSerializer(required=False)
    dish_total=serializers.SerializerMethodField()
    dish_addons=AddOnSerializer(required=False,many=True)
    dish_variants=VariantSerializer(required=False,many=True)
    class Meta:
        model = models.Cart
        fields = "__all__"
        depth=1
        
    def get_dish_total(self, obj):
        return obj.dish_total


class StaffCartSerializer(serializers.ModelSerializer):
    dish_total=serializers.SerializerMethodField()
    dish=StaffDishModelSerializer()
    dish_addons=AddOnSerializer(required=False,many=True)
    dish_variants=VariantSerializer(required=False,many=True)
    class Meta:
        model = models.Cart
        fields = ("dish","quantity","quantity","dish_addons","dish_variants","dish_total",)
        depth=1
        
    def get_dish_total(self, obj):
        return obj.dish_total



class MyOrderSerializer(serializers.ModelSerializer):
    user=CustomerProfileSerializer(required=False)
    assigned_to=StaffProfileSerializer(required=False)
    items=MyCartSerializer(many=True,required=False)
    total_price=serializers.SerializerMethodField()
    total_price_after_discount=serializers.SerializerMethodField()
    coupon=MyCouponSerializer(required=False)
    class Meta:
        model = models.Order
        fields = "__all__"
        depth=1
    def get_total_price(self, obj):
        return obj.total_price
    def get_total_price_after_discount(self, obj):
        return obj.total_price_after_discount


class MyStaffOrderSerializer(serializers.ModelSerializer):
    user=CustomCustomerSerializer(required=False)
    items=StaffCartSerializer(many=True,required=False)
    assigned_to=StaffProfileSerializer(required=False)
    total_price=serializers.SerializerMethodField()
    total_price_after_discount=serializers.SerializerMethodField()
    coupon=MyCouponSerializer(required=False)
    class Meta:
        model = models.Order
        fields=("id","items","user","assigned_to",'total_price','total_price_after_discount',
        'coupon','shipping_address','delivery_charge','order_status',"start_date",'ref_code','delivered',)
        depth=1
    def get_total_price(self, obj):
        return obj.total_price
    def get_total_price_after_discount(self, obj):
        return obj.total_price_after_discount

