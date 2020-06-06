from django import forms
from django.contrib.auth.forms import (UserCreationForm,
                                       UserChangeForm,
                                       SetPasswordForm,
                                       PasswordChangeForm)
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'username',
                  'country', 'date_of_birth', 'password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'country', 'bio')


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['new_password2']


class CustomPasswordSetForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['new_password2']
