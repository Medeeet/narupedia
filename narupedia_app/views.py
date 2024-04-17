from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views import View
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article, UserProfile, Character, Village, Technique
from .serializers import ArticleSerializer, UserProfileSerializer, RegistrationSerializer, CharacterSerializer, \
    VillageSerializer, TechniqueSerializer


class RegistrationApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            user_profile, created = UserProfile.objects.get_or_create(user=user)

            user_profile.bio = request.data.get('bio', '')
            user_profile.location = request.data.get('location', '')
            user_profile.save()

            login(request, user)
            response_data = {
                'message': 'Registration successful!',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'bio': user_profile.bio,
                    'location': user_profile.location,
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            data = {'message': 'Welcome!'}
            return Response(data, HTTP_200_OK)
        else:
            data = {'message': 'Username or/and Password is not valid!'}
            return Response(data, HTTP_403_FORBIDDEN)


class UserProfilelView(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_profile = request.user.userprofile
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user_profile = request.user.userprofile
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleListView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        order_by = request.query_params.get('ordering', 'created_at')
        articles = Article.objects.all().order_by(order_by)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleListCreateView(APIView):
    # permission_classes = [IsAuthenticated, ]
    def get(self, request):
        search_query = request.query_params.get('search', '')
        articles = Article.objects.filter(title__icontains=search_query)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    # permission_classes = [IsAuthenticated, ]
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return None

    def get(self, request, pk):
        article = self.get_object(pk)
        if article is not None:
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        article = self.get_object(pk)
        if article is not None:
            serializer = ArticleSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        article = self.get_object(pk)
        if article is not None:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CharacterListView(APIView):
    def get(self, request):
        characters = Character.objects.all()
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)


class VillageListView(APIView):
    def get(self, request):
        villages = Village.objects.all()
        serializer = VillageSerializer(villages, many=True)
        return Response(serializer.data)


class TechniqueListView(APIView):
    def get(self, request):
        techniques = Technique.objects.all()
        serializer = TechniqueSerializer(techniques, many=True)
        return Response(serializer.data)
