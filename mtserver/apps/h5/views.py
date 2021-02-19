from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from utils.CCPSDK import CCPRestSDK
import random
from .throttles import SMSCodeRateThrottle
from django.core.cache import cache
from .serializers import LoginSerializer
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from apps.mtauth.serializers import UserSerializer
from apps.mtauth import authentications
from apps.meituan.serializers import MerchantSerializer, GoodsCategorySerializer, AddressSerializer, \
    CreateOrderSerializer
from apps.meituan.models import Merchant, GoodsCategory, UserAddress, Order, Goods
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, permissions, viewsets, status
from rest_framework.decorators import action
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from django.conf import settings
import os

User = get_user_model()


class SMSCodeView(APIView):
    throttle_classes = [SMSCodeRateThrottle]

    def __init__(self, *args, **kwargs):
        super(SMSCodeView, self).__init__(*args, **kwargs)
        self.auth_token = 'fbde2950e6914dd0a9fe134eb6f8cb7e'
        self.account_sid = '8aaf0708732220a601745f8614c706e6'
        self.app_id = '8aaf0708732220a601745f8615a606ed'
        self.number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def generate_smscode(self):
        return ''.join(random.choices(self.number_list, k=4))

    def get(self, request):
        telephone = request.GET.get('tel')
        if telephone:
            # rest = CCPRestSDK.REST(self.account_sid, self.auth_token, self.app_id)
            code = self.generate_smscode()
            # set telephone and smscode to memcache
            cache.set(telephone, code, 60 * 5)
            print(code)
            return Response()
            # result = rest.sendTemplateSMS(telephone, [code, '5'], '1')
            # if result['statusCode'] == '000000':
            #     return Response()
            # else:
            #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def generate_number(self):
        number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return ''.join(random.choices(number_list, k=6))

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            telephone = serializer.validated_data.get('telephone')
            try:
                user = User.objects.get(telephone=telephone)
                user.last_login = now()
                user.save()
            except:
                username = "美团用户" + self.generate_number()
                password = ''
                user = User.objects.create(username=username, password=password, telephone=telephone, last_login=now())

            serializer = UserSerializer(user)
            token = authentications.generate_jwt(user, 7)
            return Response({'token': token, 'user': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": dict(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


class MerchantPagination(PageNumberPagination):
    page_size = 8
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class MerchantView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Merchant.objects.order_by("create_time").all()
    serializer_class = MerchantSerializer
    pagination_class = MerchantPagination

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request)
        else:
            return self.list(request)


class MerchantSearchView(generics.ListAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'categories__name', 'categories__goods_list__name']


class CategoryView(APIView):
    def get(self, request, merchant_id=None):
        queryset = GoodsCategory.objects.all()
        categories = queryset.filter(merchant=merchant_id)
        serializer = GoodsCategorySerializer(categories, many=True)
        return Response(serializer.data)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.all()

    def perform_create(self, serializer):
        is_default = serializer.validated_data.get('is_default')
        if is_default:
            self.request.user.addresses.update(is_default=False)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        is_default = serializer.validated_data.get('is_default')
        if is_default:
            self.request.user.addresses.update(is_default=False)
        serializer.save()

    # 单独定义一个action get方法，来返回默认地址
    @action(['GET'], detail=False, url_path='default')
    def default_address(self, request):
        try:
            address = self.request.user.addresses.get(is_default=True)
        except:
            address = self.request.user.addresses.first()
        serializer = self.serializer_class(instance=address)
        return Response(serializer.data)


def ali_pay():
    app_private_key = open(os.path.join(settings.BASE_DIR, 'keys', 'app_private_key.txt'), 'r').read()
    alipay_public_key = open(os.path.join(settings.BASE_DIR, 'keys', 'alipay_public_key.txt'), 'r').read()
    alipay_client_config = AlipayClientConfig(sandbox_debug=True)
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2021000116661519'
    alipay_client_config.app_private_key = app_private_key
    alipay_client_config.alipay_public_key = alipay_public_key
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
    return client


def generate_ali_pay_url(order):
    client = ali_pay()
    model = AlipayTradePagePayModel()
    # 订单id
    model.out_trade_no = order.pk
    # 订单总价格
    model.total_amount = 88.00
    # 商品标题
    model.subject = "测试订单"
    # 商品详情
    model.body = "肯德基订餐"
    # 商品码
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    # 实例化一个请求对象
    request = AlipayTradePagePayRequest(biz_model=model)
    # get请求，用户支付成功后返回的页面地址
    request.return_url = None
    # post请求，用户支付成功后通知商户的请求地址
    request.notify_url = None
    # 利用阿里支付对象发一个获得页面的请求，参数是request
    response = client.page_execute(request, http_method="GET")
    print("alipay.trade.app.pay response:" + response)
    return response


class CreateOrderView(APIView):
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            address_id = serializer.validated_data.get('address_id')
            goods_id_list = serializer.validated_data.get('goods_id_list')
            address = UserAddress.objects.get(pk=address_id)
            goods_list = Goods.objects.filter(pk__in=goods_id_list)
            goods_count = 0
            total_price = 0
            for goods in goods_list:
                goods_count += 1
                total_price += goods.price
            order = Order.objects.create(
                address=address,
                goods_count=goods_count,
                total_price=total_price,
                user=request.user,
            )
            order.goods_list.set(goods_list)
            order.save()
            pay_url = generate_ali_pay_url(order)
            return Response(pay_url)
        else:
            return Response({"message": dict(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
