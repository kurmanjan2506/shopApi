from rest_framework import serializers
from .models import Order, OrderItem
from product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = OrderItem
        fields = ('product', 'product_title', 'quantity')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr.pop('product')
        return repr


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(write_only=True, many=True)
    status = serializers.CharField(read_only=True)
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        request = self.context['request']
        user = request.user
        total_sum = 0
        for product in products:
            # price = Product.objects.get(id=product['product']).price
            try:
                total_sum += product['quantity'] * product['product'].price
            except KeyError:
                total_sum += product['product'].price

        order = Order.objects.create(status='open', total_sum=total_sum, user=user)
        for product in products:
            try:
                OrderItem.objects.create(order=order, product=product['product'], quantity=product['quantity'])
            except KeyError:
                OrderItem.objects.create(order=order, product=product['product'])
        order.save()
        return order

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['products'] = OrderItemSerializer(instance.items.all(), many=True).data
        repr.pop('product')
        products = OrderItem.objects.filter(order=instance)
        print(products, '!!!!!!!!!!!!!!!!')
        total_price = 0
        for item in products:
            [print(x.product, x.product.title, x.product.price, x.quantity) for x in products]
            price = item.quantity * item.product.price
            total_price += price
        return repr
