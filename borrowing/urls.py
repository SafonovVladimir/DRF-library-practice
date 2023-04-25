from django.urls import include, path
from rest_framework import routers

from .views import BorrowingViewSet, check_overdue_borrowings

router = routers.SimpleRouter()
router.register("borrowing", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "borrowings/check_overdue/",
        check_overdue_borrowings,
        name="check_overdue_borrowings"
    ),
]

app_name = "borrowing"
