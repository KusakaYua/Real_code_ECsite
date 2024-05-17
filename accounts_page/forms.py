from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from core_page.models import Cart

User = get_user_model()

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def save(self):
        user = super().save(commit=False)
        user.cart = Cart.objects.create()
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username",)