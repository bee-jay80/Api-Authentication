# from django.shortcuts import render
# from rest_framework.views import APIView

# class RegisterView(APIView):
#     def post(self, request):
#         pass

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer, RegisterSerializer, LoginSerializer, OrganisationCreateSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            organisation = Organisation.objects.create(name=f"{user.firstName}'s Organisation", description='')
            organisation.users.add(user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Registration unsuccessful',
            'statusCode': 400
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            if user.check_password(serializer.validated_data['password']):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 'success',
                    'message': 'Login successful',
                    'data': {
                        'accessToken': str(refresh.access_token),
                        'user': UserSerializer(user).data
                    }
                }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad request',
            'message': 'Authentication failed',
            'statusCode': 401
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        if user == request.user:
            return Response({
                'status': 'success',
                'message': 'User retrieved successfully',
                'data': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Forbidden',
            'message': 'You do not have permission to access this user',
            'statusCode': 403
        }, status=status.HTTP_403_FORBIDDEN)

class OrganisationView(APIView):
    def get(self, request):
        organisations = request.user.organisations.all()
        return Response({
            'status': 'success',
            'message': 'Organisations retrieved successfully',
            'data': OrganisationSerializer(organisations, many=True).data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganisationCreateSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.users.add(request.user)
            return Response({
                'tatus': 'uccess',
                'essage': 'Organisation created successfully',
                'data': OrganisationSerializer(organisation).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'tatus': 'Bad Request',
            'essage': 'Client error',
            'tatusCode': 400
        }, status=status.HTTP_400_BAD_REQUEST)

class OrganisationDetailView(APIView):
    def get(self, request, pk):
        organisation = Organisation.objects.get(pk=pk)
        if request.user in organisation.users.all():
            return Response({
                'tatus': 'uccess',
                'essage': 'Organisation retrieved successfully',
                'data': OrganisationSerializer(organisation).data
            }, status=status.HTTP_200_OK)
        return Response({
            'tatus': 'Forbidden',
            'essage': 'You do not have permission to access this organisation',
            'tatusCode': 403
        }, status=status.HTTP_403_FORBIDDEN)

class AddUserToOrganisationView(APIView):
    def post(self, request, pk):
        organisation = Organisation.objects.get(pk=pk)
        if request.user in organisation.users.all():
            user_id = request.data.get('userId')
            user = User.objects.get(pk=user_id)
            organisation.users.add(user)
            return Response({
                'tatus': 'uccess',
                'essage': 'User added to organisation successfully'
            }, status=status.HTTP_200_OK)
        return Response({
            'tatus': 'Forbidden',
            'essage': 'You do not have permission to access this organisation',
            'tatusCode': 403
        }, status=status.HTTP_403_FORBIDDEN)