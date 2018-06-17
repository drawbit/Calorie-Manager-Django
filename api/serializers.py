from django.db.models import Sum
from rest_framework import serializers
from .models import Record, User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'first_name', 'last_name', 'role', 'expected_cal', 'date_joined')
    extra_kwargs = {
      'expected_cal': {
        'min_value': 1,
      }
    }

class UserCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'first_name', 'last_name', 'role', 'expected_cal', 'password')
    extra_kwargs = { 
      'password': { 
        'write_only': True 
      },
      'expected_cal': {
        'min_value': 1,
      }
    }

  def create(self, validated_data):
    user = super(UserCreateSerializer, self).create(validated_data)
    user.set_password(validated_data.get('password'))
    user.save()
    return user

  def validate_role(self, value):
    user = self.context.get('request').user
    isRegister = self.context.get('isRegister', None)

    if isRegister:
      raise serializers.ValidationError('User can not set his role.')

    if user.role == 'manager' and value == 'admin':
      raise serializers.ValidationError('User manager can not set admin role.')
    elif user.role == 'user':
      raise serializers.ValidationError('Regular user can not set his role.')
    return value

class UserUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'first_name', 'last_name', 'role', 'expected_cal', 'password', 'date_joined')
    read_only_fields = ('id', 'username', 'date_joined')
    extra_kwargs = {
      'password': {
        'write_only': True,
        'required': False,
      },
      'expected_cal': {
        'min_value': 1,
      }
    }

  def update(self, instance, validated_data):
    user = super(UserUpdateSerializer, self).update(self.instance, validated_data)
    if 'password' in validated_data:
      user.set_password(validated_data['password'])
    user.save()
    return user

  def validate_role(self, value):
    user = self.context.get('request').user
    isProfile = self.context.get('isProfile', None)

    if isProfile:
      raise serializers.ValidationError('User can not change his role')

    if user.role == 'manager' and value == 'admin':
      raise serializers.ValidationError('User manager can not set admin role.')
    return value

class RecordSerializer(serializers.ModelSerializer):
  username = serializers.SerializerMethodField()
  exceeded = serializers.SerializerMethodField()

  class Meta:
    model = Record
    fields = '__all__'
    extra_kwargs = {
      'calorie': {
        'min_value': 1,
      }
    }

  def get_username(self, obj):
    return obj.user.username

  def get_exceeded(self, obj):
    expected_cal = obj.user.expected_cal
    date = obj.date
    total_cal = Record.objects.filter(date=date, user=obj.user).aggregate(Sum('calorie'))['calorie__sum']
    return total_cal > expected_cal

class UserRecordSerializer(serializers.ModelSerializer):
  exceeded = serializers.SerializerMethodField()

  class Meta:
    model = Record
    exclude = ('user',)
    extra_kwargs = {
      'calorie': {
        'min_value': 1,
      }
    }

  def get_exceeded(self, obj):
    expected_cal = obj.user.expected_cal
    date = obj.date
    total_cal = Record.objects.filter(date=date, user=obj.user).aggregate(Sum('calorie'))['calorie__sum']
    return total_cal > expected_cal
