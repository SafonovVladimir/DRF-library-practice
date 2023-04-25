from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from payment.models import Payment

from payment.serializers import (
    PaymentSerializer,
    PaymentListSerializer
)


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
