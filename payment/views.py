import stripe
from django.shortcuts import redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from borrowing.models import Borrowing
from library_config import settings
from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentListSerializer
)

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

FRONTEND_CHECKOUT_SUCCESS_URL = settings.CHECKOUT_SUCCESS_URL
FRONTEND_CHECKOUT_FAILED_URL = settings.CHECKOUT_FAILED_URL


class PaymentPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 20


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.prefetch_related("borrowing")
    serializer_class = PaymentSerializer

    def get_queryset(self):
        """Retrieve the payments with filters of user status"""
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter()

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        return PaymentSerializer

    @action(
        methods=["GET"],
        detail=True,
        url_path="pay",
    )
    def make_session(self, request, pk=None):
        user = self.request.user
        email = user.email
        payment_borr = Borrowing.objects.get(user_id=user.id)
        payment = Payment.objects.get(borrowing_id=payment_borr.id)
        print(email, payment_borr, payment)
        if payment.session_url != "not generated yet":
            return redirect(payment.session_url, code=303)

        customer_data = stripe.Customer.list(email=email).data
        if len(customer_data) == 0:
            customer = stripe.Customer.create(
                email=email)
        else:
            customer = customer_data[0]

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': (f"Payment #{payment.id} "
                                     f"(borrowing #{payment.borrowing.id})"),
                        },
                        'unit_amount': payment.amount * 100,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=FRONTEND_CHECKOUT_SUCCESS_URL,
                cancel_url=FRONTEND_CHECKOUT_FAILED_URL,
                customer=customer["id"]
            )
            payment.session_id = checkout_session.id
            payment.session_url = checkout_session.url
            return redirect(payment.session_url, code=303)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


"""

    @action(
            methods=["POST"],
            detail=True,
            url_path="webhook",
        )
    def webhook_received(self, request):

        request_data = json.loads(request.data)

        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=webhook_secret)
                data = event['data']
            except Exception as e:
                return e
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event['type']
        else:
            data = request_data['data']
            event_type = request_data['type']
        data_object = data['object']

        print('event ' + event_type)

        if event_type == 'some.event':
            print('🔔Webhook received!')

        return Response(status=status.HTTP_200_OK)
"""
