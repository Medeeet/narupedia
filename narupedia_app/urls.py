from django.urls import path, include
from .views import *

urlpatterns = [
    path('auth/', AuthApiView.as_view()),
    path('reg/', RegistrationApiView.as_view()),
    path('profile/', UserProfilelView.as_view()),
    path('articles/', ArticleListCreateView.as_view()),
    path('articles/ordering/', ArticleListView.as_view()),
    path('articles/search/', ArticleListCreateView.as_view()),
    path('articles/<int:pk>/', ArticleDetailView.as_view()),
    path('techniques/', TechniqueListView.as_view()),
    path('villages/', VillageListView.as_view()),
    path('characters/', CharacterListView.as_view()),
]
