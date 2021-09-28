from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register('adminuser',views.UserControlSerializerView,basename='adminuser'),
urlpatterns = [
    path("newuser/", views.AuthSerializerView.as_view(), name="newuser"),
    path(
        "adminuserupdate/<int:user__id>/",
        views.AdminProfileUpdateView.as_view(),
        name="adminuserupdate",
    ),
        path(
        "customerupdate/<int:user__id>/",
        views.CustomerProfileUpdateView.as_view(),
        name="customerupdate",
    ),
        path(
        "staffupdate/<int:user__id>/",
        views.StaffProfileUpdateView.as_view(),
        name="staffupdate",
    ),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path("all_staffs/", views.all_staffs, name="all_staffs"),
                path("staff_confirmation/<int:pk>/", views.staff_confirmation, name="staff_confirmation"),
] + router.urls
