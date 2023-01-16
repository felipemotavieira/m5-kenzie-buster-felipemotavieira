from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsQualifiedToGetUser
from .serializers import UserSerializer
from .models import User

# Create your views here.
class RegisterView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsQualifiedToGetUser]

    def get(self, request: Request, user_id: int) -> Response:
        user_obj = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user_obj)

        serializer = UserSerializer(user_obj)

        return Response(serializer.data, status.HTTP_200_OK)
    