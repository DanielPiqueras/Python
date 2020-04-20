from django.urls import path

from .views import check_for_recovery_password, CustomLogOut, CustomAuth, change_password, get_data_token

app_name = 'login'
urlpatterns = [
    path('setLogin/', CustomAuth.as_view()),
    path('logOut/', CustomLogOut.as_view()),
    path('forgotten/', check_for_recovery_password),
    path('changePassword/<uidb64>/<token>/', change_password),
    path('token/data/', get_data_token)
]
