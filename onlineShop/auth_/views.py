import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from auth_.models import User
from auth_.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserSignup(viewsets.ViewSet):
    @action(methods=['POST'], detail=False)
    def signup(self, request):
        if request.method == 'POST':
            user_data = request.data
            new_user = User.objects.create(email=user_data['email'], full_name=user_data['full_name'],
                                           address=user_data['address'], phone=user_data['phone'])
            new_user.set_password(user_data['password'])
            new_user.save()
            serializer = UserSerializer(new_user)
            logger.debug(f'New user signed up, ID: {serializer.instance}')
            logger.info(f'New user signed up, ID: {serializer.instance}')
            return Response(serializer.data)







    # @action(methods=['POST'], detail=False, permissions=(IsAdminUser,))
    # def create_manager(self, request):
    #     if request.method == 'POST':
    #         user_data = request.data
    #         new_user = User.objects.create_superuser(email=user_data['email'], full_name=user_data['full_name'],password=user_data['password'],
    #                                                  address=user_data['address'], phone=user_data['phone'])
    #         new_user.save()
    #         serializer = UserSerializer(new_user)
    #         logger.debug(f'New manager is created, ID: {serializer.instance}')
    #         logger.info(f'New manager is created, ID: {serializer.instance}')
    #         return Response(serializer.data)


