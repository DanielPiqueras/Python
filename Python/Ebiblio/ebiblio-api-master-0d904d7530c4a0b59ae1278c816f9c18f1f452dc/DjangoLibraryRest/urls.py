"""DjangoLibraryRest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import handler404, handler500
from rest_framework import routers

from Login import views as login_views
from Library import views as books_views

router = routers.DefaultRouter()
router.register('login/users', login_views.UserViewSet)
router.register('library/history', books_views.HistoryViewSet)
router.register('library/books', books_views.BookViewSet)

handler500 = 'Login.views.server_error'
handler404 = 'Login.views.bad_request'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('library/', include('Library.urls')),
    path('login/', include('Login.urls')),
    path('', include(router.urls)),
]
