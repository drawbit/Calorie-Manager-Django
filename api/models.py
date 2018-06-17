from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
  def _create_user(self, username, password, **kwargs):
    kwargs.setdefault('is_active', True)
    kwargs.setdefault('is_staff', True)

    if not username:
      raise ValueError('The given username must be set')

    user = self.model(username=username, **kwargs)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, username, password, **kwargs):
    kwargs.setdefault('is_superuser', False)
    return self._create_user(username, password, **kwargs)

  def create_superuser(self, username, password, **kwargs):
    kwargs.setdefault('is_superuser', True)
    kwargs.setdefault('role', 'admin')

    return self._create_user(username, password, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
  ROLE_CHOICES = (
    (u'admin', u'Admin'),
    (u'manager', u'Manager'),
    (u'user', u'User'),
  )

  username = models.CharField(max_length=50, unique=True)
  email = models.EmailField(max_length=50)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  expected_cal = models.IntegerField(default=1000, help_text='Expected number of calories per day')
  role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user', help_text='User Role')
  is_superuser = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(auto_now_add=True)

  objects = UserManager()

  USERNAME_FIELD = 'username'

  def get_short_name(self):
    return self.first_name

  def get_full_name(self):
    return "%s %s" % (self.first_name, self.last_name)

  def get_username(self):
    return self.username

  def __str__(self):
    return self.username

class Record(models.Model):
  user = models.ForeignKey(User, related_name='records')
  date = models.DateField(help_text='Record Date')
  time = models.TimeField(help_text='Record Time')
  text = models.CharField(max_length=200, help_text='Record Text')
  calorie = models.IntegerField(help_text='Num of calories')
