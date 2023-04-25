from django.urls import include, path
from rest_framework import routers

from .views import BorrowingViewSet

router = routers.SimpleRouter()
router.register("borrowing", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "borrowing"
