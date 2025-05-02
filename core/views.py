from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminOrReadOnly
from .models import ExecutiveMember, Event, PersonalityOfTheWeek, Sermon, Member
from .serializers import (
    ExecutiveMemberSerializer,
    EventSerializer,
    PersonalityOfTheWeekSerializer,
    SermonSerializer,
    MemberSerializer,
)
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserSerializer



from rest_framework import generics, permissions
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class   = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/users/me/        → returns current user's details
    PATCH /api/users/me/       → update first_name, last_name, email
    """
    serializer_class   = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # always return the logged-in user
        return self.request.user



class ExecutiveMemberViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAdminOrReadOnly]
    queryset               = ExecutiveMember.objects.order_by('name')  # alphabetical
    serializer_class       = ExecutiveMemberSerializer
    filter_backends        = [filters.SearchFilter, filters.OrderingFilter]
    search_fields          = ['name', 'role']
    ordering_fields        = ['name']

class EventViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAdminOrReadOnly]
    queryset               = Event.objects.order_by('-date')  # newest first
    serializer_class       = EventSerializer
    filter_backends        = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields       = ['date', 'location']
    search_fields          = ['title', 'description']
    ordering_fields        = ['date']

class PersonalityOfTheWeekViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAdminOrReadOnly]
    queryset               = PersonalityOfTheWeek.objects.order_by('-week_date')  # recent first
    serializer_class       = PersonalityOfTheWeekSerializer
    filter_backends        = [filters.SearchFilter, filters.OrderingFilter]
    search_fields          = ['name', 'why_selected']
    ordering_fields        = ['week_date']

class SermonViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAdminOrReadOnly]
    queryset               = Sermon.objects.order_by('-date')  # newest sermons first
    serializer_class       = SermonSerializer
    filter_backends        = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields       = ['preacher', 'date']
    search_fields          = ['title', 'description']
    ordering_fields        = ['date']

class MemberViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAdminOrReadOnly]
    queryset               = Member.objects.order_by('-join_date')  # most recent members first
    serializer_class       = MemberSerializer
    filter_backends        = [filters.SearchFilter, filters.OrderingFilter]
    search_fields          = ['name', 'email', 'status']
    ordering_fields        = ['join_date', 'name']
