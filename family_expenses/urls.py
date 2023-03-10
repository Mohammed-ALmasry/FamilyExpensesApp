"""family_expenses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from family.views import login, sample_api, get_token, Register, CreateFamily, CreateMember, FamilyMember, MaterialsViewSet,MaterialsViewSet, \
    OutlayTypeViewSet, \
    OutlayViewSet,\
    MemberViewSet,\
    FamilyExpenses,\
    UserExpenses,\
    MaterialsExpenses,\
    ServicesExpenses

from rest_framework.routers import DefaultRouter
# from tickets import views
router = DefaultRouter()
router.register(r'materials', MaterialsViewSet, basename='material')
router.register(r'outlaytypes', OutlayTypeViewSet, basename='outlaytype')
router.register(r'Outlays', OutlayViewSet, basename='Outlay')
router.register(r'members', MemberViewSet, basename='members')

urlpatterns = router.urls + [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('sampleapi/', sample_api),
    path('user-token/', get_token),
    path('register/', Register.as_view(), name="register-user"),
    path('create-family/', CreateFamily.as_view(), name="create-family"),
    path('create-member/', CreateMember.as_view(), name="create-member"),
    path('FamilyMember/', FamilyMember.as_view(), name="family_member"),
    path('Family-Expenses/',FamilyExpenses.as_view(),name="family_expenses"),
    path('user-expenses/',UserExpenses.as_view(),name="user-expenses"), 
    path('materials-expenses/',MaterialsExpenses.as_view(),name="material-expenses"), 
    path('service-expenses/',ServicesExpenses.as_view(),name="service_expenses")
    ]
