from django.dispatch.dispatcher import receiver
from django.shortcuts import render
from . import models, serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view

# Create your views here.

class UserControlSerializerView(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.AdminUserSerializer



class AuthSerializerView(generics.CreateAPIView, generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class AdminProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = models.AdminProfile.objects.all()
    serializer_class = serializers.MyAdminProfileSerializer
    lookup_field = "user__id"
    def put(self, request, *args, **kwargs):
        user=models.User.objects.get(id=kwargs['user__id'])
        admin=models.AdminProfile.objects.filter(user=user)
        if admin:
            admin=admin[0]
            admin.full_name=request.data['full_name']
            admin.address=request.data['address']
            admin.phone=request.data['phone']
            if request.data['profile_pic']!='null':
                print('Uploaded Profile Picture') 
                admin.profile_pic=request.FILES['profile_pic']
            admin.save()
            adminserializer=serializers.MyAdminProfileSerializer(admin,context={'request': request})
        return Response(adminserializer.data)

    

class CustomerProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
    lookup_field = "user__id"
    def put(self, request, *args, **kwargs):
        user=models.User.objects.get(id=kwargs['user__id'])
        customer=models.Customer.objects.filter(user=user)
        if customer:
            customer=customer[0]
            customer.full_name=request.data['full_name']
            customer.address=request.data['address']
            customer.phone=request.data['phone']
            if request.data['profile_pic']!='null':
                print('Uploaded Profile Picture') 
                customer.profile_pic=request.FILES['profile_pic']
            customer.save()
            customerserializer=serializers.CustomerProfileSerializer(customer,context={'request': request})
        return Response(customerserializer.data)


class StaffProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffProfileSerializer
    lookup_field = "user__id"

    def put(self, request, *args, **kwargs):
        user=models.User.objects.get(id=kwargs['user__id'])
        staff=models.Staff.objects.filter(user=user)
        if staff:
            staff=staff[0]
            staff.full_name=request.data['full_name']
            staff.address=request.data['address']
            staff.phone=request.data['phone']
            if request.data['profile_pic']!='null':
                print('Uploaded Profile Picture') 
                staff.profile_pic=request.FILES['profile_pic']
            staff.save()
            staffserializer=serializers.StaffProfileSerializer(staff,context={'request': request})
        return Response(staffserializer.data)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer

@api_view(['GET'])
def all_staffs(request):
    staff=models.Staff.objects.all()
    staffserializer=serializers.StaffProfileSerializer(staff,context={'request': request},many=True)
    return Response(staffserializer.data)
    
STAFF_CODE=['#eer4rg435',"#ashjd1213","#ashjd1245","#jkl9d1245"]

@api_view(['GET','POST'])
def staff_confirmation(request,pk):
    staff=models.Staff.objects.filter(user__id=pk)
    code=request.data['code']
    if staff:
        staff=staff[0]
        if code in STAFF_CODE:
            staff.staff_code=code
            staff.is_verified=True
            staff.save()
            return Response({'msg':'Confirmed'})
    else:
        return Response({'msg':'Failed to Confirm.Try Again'})