from django.urls import path

from .views import (
    send_friend_request, view_all_friend_requests, accept_friend_request,
    remove_friend, decline_friend_request, cancel_friend_request, friends_list_view
)

app_name = 'friend'

urlpatterns = [
    path('list/<user_id>', friends_list_view, name='list'),

    # you to them
    path('friend_request/', send_friend_request, name='friend-request'),
    path('friend_request_cancel/', cancel_friend_request, name='friend-request-cancel'),
    path('friend_remove/', remove_friend, name='remove-friend'),



    # Them to you
    path('friend_requests/<user_id>/', view_all_friend_requests, name='friend-requests'), # TODO: ADD THIS LINE.
    path('friend_request_accept/<friend_request_id>/', accept_friend_request, name='friend-request-accept'),
    path('friend_request_decline/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),



]

