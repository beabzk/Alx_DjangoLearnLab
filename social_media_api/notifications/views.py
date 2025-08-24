from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification, Like
from .serializers import NotificationSerializer
from posts.models import Post

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.all()

class LikeView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if not created:
                return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "Post liked."})
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

class UnlikeView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"success": "Post unliked."})
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        except Like.DoesNotExist:
            return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
