from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import LoginUserSerializer

from utils.hlepers import viewException
from utils.serializers import PaginationSerializer


class PostsViewSet(ViewSet):
    """
    Posts viewset for CRUD operations
    """

    permission_classes = [IsAuthenticated, AllowAny]
    authentication_classes = [TokenAuthentication]
    pagination_class = PaginationSerializer

    @viewException
    def get_articles_by_id(self, _request, post_id):
        pass

    @viewException
    def get_articles_list(self, request):
        pass

    @viewException
    def create_article(self, request):
        pass

    @viewException
    def update_article(self, request):
        pass

    @viewException
    def comment_article(self, request):
        pass
