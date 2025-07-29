from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import NewUser
from .serializers import UserSelfSerializer


class UserInfoRetrieveAPIView(RetrieveAPIView):
    model = NewUser
    serializer_class = UserSelfSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NewUser.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            user_id = self.kwargs.get('pk')
            if user_id is None:
                instance = request.user
            else:
                instance = NewUser.objects.get(pk=kwargs['pk'])
        except NewUser.DoesNotExist:
            return Response(data={"detail": "Пользователь не найден"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(
            instance, many=False, context={'request': request})
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)
