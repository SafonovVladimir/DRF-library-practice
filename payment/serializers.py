from rest_framework import serializers

# from borrowing.serializers import BorrowingSerializer
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        read_only_fields = ("id", "session_url", "session_id",)
        fields = (
            "id",
            "status",
            "type",
            "session_url",
            "session_id",
            "borrowing",
            "amount",
        )


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        read_only_fields = ("id", "session_url", "session_id",)
        fields = (
            "id",
            "status",
            "type",
            "session_url",
            "session_id",
            "borrowing",
            "amount",
        )
