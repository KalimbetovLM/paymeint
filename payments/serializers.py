from rest_framework.serializers import ModelSerializer
from payments.models import Order

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        exclude = ["created_at","status"]

        