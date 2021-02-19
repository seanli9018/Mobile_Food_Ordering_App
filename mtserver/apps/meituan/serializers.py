from apps.meituan.models import Merchant, GoodsCategory, Goods, UserAddress
from rest_framework import serializers


class MerchantSerializer(serializers.ModelSerializer):
    up_send = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)

    class Meta:
        model = Merchant
        # exclude = ['up_send']
        fields = '__all__'

    # def validate_up_send(self, value):
    #     if isinstance(value, str):
    #         print(value)
    #         raise serializers.ValidationError("Its a string")
    #     return value

    # def create(self, validated_data):
    #     up_send = validated_data.get('up_send')
    #     merchant = Merchant.objects.create(**validated_data, up_send=up_send)
    #     return merchant


class GoodsSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    class Meta:
        model = Goods
        exclude = ['category']

    def validate_category_id(self, value):
        if not GoodsCategory.objects.filter(pk=value).exists():
            raise serializers.ValidationError("This category is not exists")
        return value

    def create(self, validated_data):
        category_id = validated_data.get('category_id')
        category = GoodsCategory.objects.get(pk=category_id)
        goods = Goods.objects.create(**validated_data, category=category)
        return goods


class GoodsCategorySerializer(serializers.ModelSerializer):
    # merchant = MerchantSerializer(read_only=True)
    merchant_id = serializers.IntegerField()
    goods_list = GoodsSerializer(read_only=True, many=True)

    class Meta:
        model = GoodsCategory
        exclude = ['merchant']

    def validate_merchant_id(self, value):
        if not Merchant.objects.filter(pk=value).exists():
            raise serializers.ValidationError("The merchant is not exists")
        return value

    def create(self, validated_data):
        merchant_id = validated_data.get('merchant_id')
        merchant = Merchant.objects.get(pk=merchant_id)
        category = GoodsCategory.objects.create(**validated_data, merchant=merchant)
        return category


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        exclude = ['user']


class CreateOrderSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    goods_id_list = serializers.ListField(min_length=1)