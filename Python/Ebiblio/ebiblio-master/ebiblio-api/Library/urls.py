from django.urls import path

from .views import get_book_history, get_user_history, find_in_google_api

app_name = 'library'
urlpatterns = [
    path('history/user/<int:user_id>/', get_user_history),
    path('history/book/<uuid:uuid_book>/', get_book_history),
    path('find/', find_in_google_api)
]
