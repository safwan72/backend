from django.shortcuts import render
import json
from . import models,serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser,IsAuthenticated,BasePermission
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5
    
class DayTimeView(generics.ListCreateAPIView):
    queryset=models.DayTime.objects.all()
    serializer_class=serializers.DayTimeSerializer
    # permission_classes=(IsAdminUser,IsAuthenticated,)
    def create(self, request,*args,**kwargs):
        name=None
        if request.data['name']!='':
            name=request.data['name']
        if name!=None:
            daytime=models.DayTime.objects.create(
                name=name
            )
            daytimeserializer=serializers.DayTimeSerializer(daytime)
            return Response({'daytime':daytimeserializer.data})
        else:
            return Response({'daytime':'False'})
    

@api_view(['GET'])
def CategoryViewFunctionDishes(request,pk):
        dishesarr=[]
        category=models.Category.objects.get(id=pk)
        dishes=models.DishModel.objects.filter(dish_category=category).all()
        if dishes:
            for dish in dishes:
                dishesarr.append(dish)
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(dishesarr, request)
        serializer = serializers.DishModelSerializer(result_page, many=True,context={'request':request})
        # dishserializer=serializers.DishModelSerializer(dishesarr,many=True,context={'request':request})
        return paginator.get_paginated_response(serializer.data)
        # return paginator.get_paginated_response(serializer.data)


class CategoryCreateView(generics.ListCreateAPIView):
    queryset=models.Category.objects.all()
    serializer_class=serializers.CategorySerializer
    def create(self, request,*args,**kwargs):
        if request.data['picture'] and request.data['name']!='':
            name=request.data['name']
            picture=request.data['picture']
            isactive=True if request.data['isActive']=='true'  else False
        if name!=None and request.data['picture']:
            category=models.Category.objects.create(
                name=name,picture=picture,isActive=isactive
            )
            categoryserializer=serializers.CategorySerializer(category)
            return Response({'category':categoryserializer.data})
        else:
            return Response({'category':'False'})
        
class VariantCreateView(generics.ListCreateAPIView):
    queryset=models.Variants.objects.all()
    serializer_class=serializers.VariantSerializer
    def create(self, request,*args,**kwargs):
        variant_name=None
        if request.data['variant_name']!='':
            variant_name=request.data['variant_name']
            price=request.data['price']
        if variant_name!=None:
            variant=models.Variants.objects.create(
                variant_name=variant_name,price=price
            )
            variantserializer=serializers.VariantSerializer(variant)
            return Response({'variants':variantserializer.data})
        else:
            return Response({'variants':'False'})
        
class AddonCreateView(generics.ListCreateAPIView):
    queryset=models.AddOns.objects.all()
    serializer_class=serializers.AddOnSerializer
    def create(self, request,*args,**kwargs):
        name=None
        if request.data['name']!='':
            name=request.data['name']
            price=request.data['price']
        if name!=None:
            addon=models.AddOns.objects.create(
                name=name,price=price
            )
            addonserializer=serializers.AddOnSerializer(addon)
            return Response({'addon':addonserializer.data})
        else:
            return Response({'addon':'False'})
    
@api_view(['GET'])
def DishViewFunction(request,pk):  
    dish=models.DishModel.objects.filter(id=pk)
    if dish:
        dishserializer=serializers.DishModelSerializer(dish,many=True,context={'request': request})        
    return Response(dishserializer.data)
@api_view(['GET'])
def AllDishViewFunction(request):
    dish=models.DishModel.objects.all()
    dishserializer=serializers.DishModelSerializer(dish,many=True,context={'request': request})        
    return Response(dishserializer.data)



class DishModelView(viewsets.ModelViewSet):
    queryset=models.DishModel.objects.all()
    serializer_class=serializers.DishModelSerializer
    pagination_class =StandardResultsSetPagination
    
    
    def create(self, request):
        dish_daytime=json.loads(request.data['dish_daytime'])

        dish_category=json.loads(request.data['dish_category'])
        availability=True if request.data['availability']=='true' else False
        featured=True if request.data['featured']=='true' else False
        
        dish_new,created=models.DishModel.objects.get_or_create(
            dish_name=request.data['dish_name'],
            dish_picture=request.data['dish_picture'],
            price=request.data['price'],
            discount=request.data['discount'],
            availability=availability,
            featured=featured,
            dish_description=request.data['dish_description'],
                        dish_vat=request.data['dish_vat'],
            dish_tax=request.data['dish_tax'],
        )
        for i in dish_category:
            category=models.Category.objects.filter(name=i)
            if category:
                dish_new.dish_category.add(category[0])
                dish_new.save()
        
        for i in dish_daytime:
            daytime=models.DayTime.objects.filter(name=i)
            if daytime:
                dish_new.dish_daytime.add(daytime[0])
                dish_new.save()
        dish_new.save()
        return Response({'message':'Added'})        
    
@api_view(['GET'])
def DayTimeViewFunction(request):
    daytimeobj=models.DayTime.objects.all()
    daytimeobjserializer=serializers.DayTimeSerializer(daytimeobj,many=True,context={'request': request})        
    return Response({'daytimes':daytimeobjserializer.data})

@api_view(['GET'])
def FeaturedDishesView(request):
    dish=models.DishModel.objects.filter(featured=True)
    dishserializer=serializers.DishModelSerializer(dish,many=True,context={'request': request})        
    return Response(dishserializer.data)

@api_view(['GET'])
def DayTimeViewFunctionDishes(request,pk):
        dishesarr=[]
        category=models.DayTime.objects.get(id=pk)
        dishes=models.DishModel.objects.filter(dish_daytime=category).all()
        if dishes:
            for dish in dishes:
                dishesarr.append(dish)
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(dishesarr, request)
        serializer = serializers.DishModelSerializer(result_page, many=True,context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    
class DayTimeView(generics.ListCreateAPIView):
    queryset=models.DayTime.objects.all()
    serializer_class=serializers.DayTimeSerializer
    def create(self, request,*args,**kwargs):
        name=None
        if request.data['name']!='':
            name=request.data['name']
        if name!=None:
            daytime=models.DayTime.objects.create(
                name=name
            )
            daytimeserializer=serializers.DayTimeSerializer(daytime)
            return Response({'daytime':daytimeserializer.data})
        else:
            return Response({'daytime':'False'})
    
    