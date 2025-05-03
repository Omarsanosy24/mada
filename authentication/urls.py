from django.urls import path, include
from .views import *

app_name = "auth"
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('profile/', UserInfoView.as_view(), name="profile"),
    path('get_url_patterns/', GeneratePresignedUrl.as_view(), name="search"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),

    # path('verify/', UserVerifyView.as_view(), name="verify"),
    # path('users/', GetUserForDepartment.as_view(), name="users"),

    # path('login_super/', LoginAPIView.as_view(), name="login_super"),

]
