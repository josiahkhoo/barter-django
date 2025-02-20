import jwt
import uuid
from django_countries.fields import CountryField
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from barter import settings
from .utils import UserStatus

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=15, unique=True)
    datetime_created = models.DateTimeField(
        _('datetime created'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)
    date_of_birth = models.DateTimeField(
        _('date of birth'), null=True, blank=True)
    country = CountryField(null=True, blank=True)
    bio = models.CharField(
        _('bio'), max_length=180, blank=True, null=True)
    status = models.IntegerField(choices=UserStatus.choices(), default=0)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    datetime_last_logout = models.DateTimeField(
        _('datetime last logout'), default=timezone.now)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    outgoing_friends = models.ManyToManyField(
        'User', blank=True, related_name='incoming_friends')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'date_of_birth', 'country']

    def __str__(self):
        return str("[USER] %s" % (self.email))

    @property
    def token(self):
        """
        Allows us to get a user's token by calling 'user.token' instead of 'user.generate_jwt_token().

        The '@property' decorator above makes this possible. 'token' is called a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry date set to 60 days in the future.
        """
        dt = datetime.now() + timedelta(days=settings.TOKEN_EXPIRE_DAYS)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def get_incoming_friend_requests(self):
        incoming_friends = self.incoming_friends.all()
        outgoing_friends = self.outgoing_friends.all()
        friend_requests = list(filter(
            lambda x: x not in outgoing_friends, incoming_friends
        ))
        return friend_requests

    def get_outgoing_friend_requests(self):
        incoming_friends = self.incoming_friends.all()
        outgoing_friends = self.outgoing_friends.all()
        friend_requests = list(filter(
            lambda x: x not in incoming_friends, outgoing_friends
        ))
        return friend_requests

    def get_friends(self):
        incoming_friends = self.incoming_friends.all()
        outgoing_friends = self.outgoing_friends.all()
        friend_requests = list(filter(
            lambda x: x in outgoing_friends, incoming_friends
        ))
        return friend_requests

    def add_friend(self, other_user):
        if other_user == self:
            raise Exception("Friend is yourself")
        self.outgoing_friends.add(other_user)
        self.save()
        return self

    def decline_friend(self, other_user):
        other_user.outgoing_friends.remove(self)
        return True
