from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('address', views.AddressViewSet, basename='address')

app_name = 'smscode'
urlpatterns = [
    path('smscode', views.SMSCodeView.as_view(), name='smscode'),
    path('login', views.LoginView.as_view(), name='login'),
    path('merchants', views.MerchantView.as_view(), name='merchants'),
    path('merchant/<int:pk>', views.MerchantView.as_view(), name='merchant_detail'),
    path('merchants/search', views.MerchantSearchView.as_view(), name='search'),
    path('category/merchant/<int:merchant_id>', views.CategoryView.as_view(), name='categories'),
    path('submitorder', views.CreateOrderView.as_view(), name='submitorder')
] + router.urls