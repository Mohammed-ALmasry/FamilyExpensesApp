import email

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
)
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework import mixins, generics, viewsets
from rest_framework.views import APIView

from .models import CustomeUser, family, Material,outlay,outlayType
from .serializers import CustomUserSerializer, MaterialSerializer, outlayTypeSerializer, outlaySerializer, CustomMemberSerializer
from django.db.models import Sum

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def get_token(request):
    username = request.data.get("username")
    print("The usename is", username)
    user = CustomeUser.objects.get(username=username)
    if user:
        token = Token.objects.get(user=user.id)
        data = {
            "token": token.key
        }
    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    is_expired, token = token_expire_handler(token)
    try:
        family_name = family.objects.get(user_id=user.id)
        return Response({
            'user_id': user.id,
            'user_type': user.user_type,
            'family_name': family_name.name,
            'token': token.key,
            'expires_in': expires_in(token),},
            status=HTTP_200_OK)
    except:
        pass
    return Response({
        'user_id': user.id,
        'user_type': user.user_type,
        'family_name': "",
        'token': token.key,
        'expires_in': expires_in(token),},
        status=HTTP_200_OK)


# this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time


# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)


class Register(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        first_name = self.request.data["first_name"]
        last_name = self.request.data["last_name"]
        username = self.request.data["username"]
        user_type = self.request.data["user_type"]
        password = self.request.data["password"]

        user = CustomeUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_head=True,
            user_type=user_type
        )
        user.set_password(password)
        user.save()
        family.objects.create(name=user.last_name,user_id=user)
        return JsonResponse(status=200,data={})


class CreateFamily(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user_id = self.request.POST.get("user_id")
        user = CustomeUser.objects.get(id=user_id)
        name = self.request.POST.get("name")
        family.objects.create(user_id=user, name=name)
        return Response()


class CreateMember(GenericAPIView):
    def post(self, request, *args, **kwargs):
        first_name = self.request.data["first_name"]
        last_name = self.request.data["last_name"]
        username = self.request.data["username"]
        user_type = self.request.data["user_type"]
        password = self.request.data["password"]
        user = CustomeUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_head=False,
            user_type=user_type
        )
        user.set_password(password)
        user.save()
        family.objects.create(name=last_name, user_id=user)
        return JsonResponse(status=200,data={})


class FamilyMember(GenericAPIView):

    def post(self, request, *args, **kwargs):
        users_list = []
        # user_id = self.request.POST.get("user_id")
        user_id = self.request.data["user_id"]
        user = CustomeUser.objects.get(id=user_id)
        if user.is_head == True:
            family_obj = family.objects.get(user_id=user.id)
            users = family.objects.filter(name=family_obj.name).exclude(user_id=user.id)
            for user in users:
                user = CustomeUser.objects.get(id=user.user_id.id)
                users_list.append(user)
            serializer_user = CustomUserSerializer(users_list, many=True)

            data = {
                "family_name": family_obj.name,
                "members_list": serializer_user.data,
            }
        return JsonResponse(status=200, data=data)


class MaterialsViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer 

    def get_queryset(self): 
        materials = Material.objects.filter(user_id__last_name=self.request.user.last_name)
        return materials

class MemberViewSet(viewsets.ModelViewSet):
    queryset = CustomeUser.objects.all()
    serializer_class = CustomMemberSerializer

class OutlayTypeViewSet(viewsets.ModelViewSet):
    queryset = outlayType.objects.all()
    serializer_class = outlayTypeSerializer

    def get_queryset(self):
        queryset = outlayType.objects.filter(user_id__last_name=self.request.user.last_name)
        return queryset

class OutlayViewSet(viewsets.ModelViewSet):
    queryset = outlay.objects.all()
    serializer_class = outlaySerializer 

    def get_queryset(self): 
        queryset = outlay.objects.filter(user_id__last_name=self.request.user.last_name)  
        return queryset


class FamilyExpenses(GenericAPIView):

    def post(self,request,*args,**kwargs):  
        user_id = self.request.data.get("user_id")   
        month = self.request.data.get("month",None) 
        year = self.request.data.get("year",None) 
        
        total = 0 
        user= CustomeUser.objects.get(id=user_id) 
        filters = {
            "user_id__last_name":user.last_name,
        } 
        if month != None: 
            filters = { "date__month":month,
                    "user_id__last_name":user.last_name }  
        if year != None:
            filters = {"date__year":year,
                    "user_id__last_name":user.last_name}
        

        family_expenses = outlay.objects.filter(**filters)
        for expense in family_expenses: 
            total +=expense.price
        
        serializer = outlaySerializer(data=family_expenses,many=True) 
        serializer.is_valid() 
        data = {
            "Total_Expenses":total,
            "Expenses":serializer.data
        }

        return JsonResponse(status=200,data=data,safe=False)

class UserExpenses(GenericAPIView):
    
    def post(self,request,*args,**kwargs):
        
        user_id = self.request.data.get("user_id")  
        total = 0
        expenses = outlay.objects.filter(user_id=user_id) 
        for expense in expenses:
            total +=expense.price

        serializer = outlaySerializer(data=expenses,many=True) 
        serializer.is_valid() 
        data = {
            "Total_Expenses":total,
            "User_Expenses":serializer.data
        }
        return JsonResponse(status=200,data=data,safe=False)
        
class MaterialsExpenses(GenericAPIView):

    def post(self,request,*args,**kwargs):
        material_id = self.request.data.get("material_id") 
        total = 0
        expenses = outlay.objects.filter(user_id__last_name=self.request.user.last_name,material_id=material_id) 

        for expense in expenses: 
            total +=expense.price
        serializer = outlaySerializer(data=expenses,many=True) 
        serializer.is_valid() 
        data = {
            "Total_Expenses":total,
            "Material_Expenses":serializer.data
        }
        return JsonResponse(status=200,data=data,safe=False)
        
class ServicesExpenses(GenericAPIView):

    def get(self,request,*args,**kwargs):
        total = 0
        expenses = outlay.objects.filter(user_id__last_name=self.request.user.last_name,material_id__is_service=True)
        for expense in expenses: 
            total +=expense.price
        serializer = outlaySerializer(data=expenses,many=True) 
        serializer.is_valid() 
        data = {
            "Total_Expenses":total,
            "Services_Expenses":serializer.data
        }
        return JsonResponse(status=200,data=data,safe=False)
                
        

