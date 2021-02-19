from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.timezone import now
from apps.mtauth.authentications import generate_jwt, JWTAuthentication
from apps.mtauth.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, mixins
from apps.meituan.models import Merchant, GoodsCategory, Goods
from apps.meituan.serializers import MerchantSerializer, GoodsCategorySerializer, GoodsSerializer
from rest_framework.pagination import PageNumberPagination
import shortuuid
import os
from django.conf import settings
from rest_framework.decorators import action


# rewrite rest framework Pagination response.
# to get extra data (for example: num_pages)
class MerchantPagination(PageNumberPagination):
    page_size = 12
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


# self defined view, to control overall authentication and authorization
class CmsBaseView(object):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class LoginView(APIView):
    def post(self, request):
        # authenticate user info
        serializer = AuthTokenSerializer(data=request.data)
        # if it passed or valid, user is considered to logged in successfully
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = now()
            user.save()
            token = generate_jwt(user)
            user_serializer = UserSerializer(instance=user)
            return Response({"token": token, "user": user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "用户名或密码错误！"}, status=status.HTTP_401_UNAUTHORIZED)


class MerchantViewSet(CmsBaseView, viewsets.ModelViewSet):
    queryset = Merchant.objects.order_by("-create_time").all()
    serializer_class = MerchantSerializer
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    # permission classes have already defined in CmsBaseView

    # authentication_classes = [JWTAuthentication]
    # authentication classes have been defined in settings.py as global setting.
    pagination_class = MerchantPagination


# Create, Update, Destroy, Retrieve
class CategoryViewSet(
    CmsBaseView,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.goods_list.count() > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # list
    # /cms/category/merchant/<int:merchant_id>
    @action(['GET'], detail=False, url_path="merchant/(?P<merchant_id>\d+)")
    def merchant_category(self, request, merchant_id=None):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        categories = queryset.filter(merchant=merchant_id)
        serializer = serializer_class(categories,many=True)
        return Response(serializer.data)


# Create, Update, Destroy, Retrieve
class GoodsViewSet(
    CmsBaseView,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    # List
    # /cms/goods/category/<int:category_id>
    @action(['GET'], detail=False, url_path="category/(?P<category_id>\d+)")
    def category_goods(self, request, category_id=None):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        goods_items = queryset.filter(category=category_id)
        serializer = serializer_class(goods_items, many=True)
        return Response(serializer.data)


class PictureUploadView(CmsBaseView, APIView):
    def save_file(self, file):
        suffix = os.path.splitext(file.name)[-1]
        filename = shortuuid.uuid() + suffix
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        with open(filepath, 'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)
        return self.request.build_absolute_uri(settings.MEDIA_URL + filename)

    def post(self, request):
        # print(request.data.get('file'))
        file = request.data.get('file')
        file_url = self.save_file(file)
        return Response({"picture": file_url})
