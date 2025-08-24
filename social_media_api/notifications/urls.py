from django.urls import path
from .views import NotificationListView, LikeView, UnlikeView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('posts/<int:pk>/like/', LikeView.as_view(), name='like'),
    path('posts/<int:pk>/unlike/', UnlikeView.as_view(), name='unlike'),
]
