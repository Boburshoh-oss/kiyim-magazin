from django.urls import path
from .views import register, login, logout, activate, dashboard,forgotpassword,resetpassword_validate,resetPassword

urlpatterns = [
    path("register/",register,name="register"),
    path("login/",login,name="login"),
    path("logout/",logout,name="logout"),
    path("dashboard/",dashboard,name="dashboard"),
    path("",dashboard,name="dashboard"),
    path("forgotpassword",forgotpassword,name="forgotpassword"),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
    path('resetPassword/',resetPassword,name='resetPassword'),
    path('resetpassword_validate/<uidb64>/<token>/',resetpassword_validate,name='resetpassword_validate'),
]
