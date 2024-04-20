from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from pprint import pprint
from payme.methods.generate_link import GeneratePayLink
from payments.models import Order
from payments.serializers import OrderSerializer

from django import views
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

class CreateOrderView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        pay_link = GeneratePayLink(
            order_id=serializer.data['id'],
            amount=serializer.data['amount'],
            callback_url=settings.PAYME['PAYME_CALL_BACK_URL'],
        ).generate_link()

        data = {
            "link": pay_link,
            "order": serializer.data
        }
        return Response(status=status.HTTP_201_CREATED, data=data)    


class NgrokSkipBrowserWarningMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['ngrok-skip-browser-warning'] = '1'
        return response

