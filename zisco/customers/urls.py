from django.urls import path, include

from .views import (
    Login, Register, DashboardIndex, Logout,
    Request, ReqIndex
)

app_name = "customers"

dash_urls = [
    path("", DashboardIndex.as_view(), name="dashboard"),
    path("request/", Request.as_view(), name="request"),
    path("requests/", ReqIndex.as_view(), name="requests"),
]

urlpatterns = [
    path("", include(dash_urls)),



    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("register/", Register.as_view(), name="register"),
]
