from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Record, User
from .paginations import PageNumberPagination
from .permissions import IsAdminOrManager, IsAdminOrUser
from .serializers import UserRecordSerializer, RecordSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer

class RegisterView(CreateAPIView):
  serializer_class = UserCreateSerializer
  permission_classes = ()

  def create(self, request):
    serializer_class = self.get_serializer_class()
    serializer = serializer_class(data=request.data, context={'request': request, 'isRegister': True})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

class UserRecordViewSet(ModelViewSet):
  serializer_class = UserRecordSerializer
  permission_classes = [IsAuthenticated, IsAdminOrUser]

  def get_object(self):
    pk = self.kwargs['pk']
    queryset = self.get_queryset()
    obj = get_object_or_404(queryset, pk=pk)
    self.check_object_permissions(self.request, obj)
    return obj

  def get_queryset(self):
    user = get_object_or_404(User, pk=self.kwargs['uid'])
    queryset = Record.objects.all().order_by('-date', '-time')
    currentUser = self.request.user

    if (currentUser.role == 'user' and currentUser != user):
      raise PermissionDenied('You are not allowed to perform this action')

    queryset = queryset.filter(user=user)

    date_from = self.request.query_params.get('date_from', None)
    date_to = self.request.query_params.get('date_to', None)
    time_from = self.request.query_params.get('time_from', None)
    time_to = self.request.query_params.get('time_to', None)
    
    if date_from is not None:
      queryset = queryset.filter(date__gte=date_from)
    if date_to is not None:
      queryset = queryset.filter(date__lte=date_to)
    if time_from is not None:
      queryset = queryset.filter(time__gte=time_from)
    if time_to is not None:
      queryset = queryset.filter(time__lte=time_to)

    return queryset

  def perform_create(self, serializer):
    user = get_object_or_404(User, pk=self.kwargs['uid'])
    serializer.validated_data['user'] = user
    serializer.save()

class RecordViewSet(ModelViewSet):
  serializer_class = RecordSerializer
  permission_classes = [IsAuthenticated, IsAdminOrUser]

  def get_queryset(self):
    queryset = Record.objects.all().order_by('-date', '-time')

    user = self.request.user

    if user.role == 'user':
      queryset = queryset.filter(user=user)

    date_from = self.request.query_params.get('date_from', None)
    date_to = self.request.query_params.get('date_to', None)
    time_from = self.request.query_params.get('time_from', None)
    time_to = self.request.query_params.get('time_to', None)
    
    if date_from is not None:
      queryset = queryset.filter(date__gte=date_from)
    if date_to is not None:
      queryset = queryset.filter(date__lte=date_to)
    if time_from is not None:
      queryset = queryset.filter(time__gte=time_from)
    if time_to is not None:
      queryset = queryset.filter(time__lte=time_to)

    return queryset

class UserViewSet(ModelViewSet):
  serializers = {
    'POST': UserCreateSerializer,
    'PUT': UserUpdateSerializer,
    'PATCH': UserUpdateSerializer,
    'DEFAULT': UserSerializer,
  }
  permission_classes = [IsAuthenticated, IsAdminOrManager]

  def get_serializer_class(self):
    return self.serializers.get(self.request.method, self.serializers['DEFAULT'])

  def get_queryset(self):
    user = self.request.user
    queryset = User.objects.all().order_by('date_joined')

    if user.role == 'admin':
      queryset = queryset
    elif user.role == 'manager':
      queryset = queryset.filter(role__in=['manager', 'user'])
    else:
      queryset = queryset.filter(pk=user.id)

    return queryset

  @list_route(methods=['GET', 'PUT'], permission_classes=[IsAuthenticated,])
  def profile(self, request, pk=None):
    serializer_class = self.get_serializer_class()

    if request.method == 'PUT':
      serializer = serializer_class(instance=request.user, data=request.data, context={'request': request, 'isProfile': True})
      serializer.is_valid(raise_exception=True)
      serializer.save()
    else:
      serializer = serializer_class(instance=request.user)

    return Response(serializer.data)

  @list_route(methods=['GET'], permission_classes=[IsAuthenticated,], pagination_class=[])
  def all(self, request, pk=None):
    queryset = self.get_queryset()
    serializer_class = self.get_serializer_class()
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data)
