from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExecutiveMemberViewSet,
    EventViewSet,
    PersonalityOfTheWeekViewSet,
    SermonViewSet,
    MemberViewSet,
)

router = DefaultRouter()
router.register(r'executives', ExecutiveMemberViewSet)
router.register(r'events', EventViewSet)
router.register(r'personalities', PersonalityOfTheWeekViewSet)
router.register(r'sermons', SermonViewSet)
router.register(r'members', MemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
