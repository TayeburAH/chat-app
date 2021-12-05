from django.urls import path, include
from .views import *

app_name = 'account'
urlpatterns = [
    path('<user_id>/', account_view, name='view'),
    path('<user_id>/edit/', edit_account_view, name="edit"),

]
