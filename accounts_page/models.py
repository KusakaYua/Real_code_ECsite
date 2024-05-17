from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core_page.models import Cart

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    cart = models.OneToOneField(to=Cart, on_delete=models.CASCADE, related_name='cart_user', blank=True, null=True)
    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"

"""
CustomUserManager:

ユーザー達の管理:
CustomUserManagerは、ユーザーやスーパーユーザーの作成、更新、削除など、複数のユーザーに関する操作を管理します。
管理者がユーザーを作成するときや、ユーザーのパスワードをリセットするとき、スーパーユーザーを作成するときなどに使用されます。
主に管理者向けの操作をサポートし、個々のユーザーの情報ではなく、ユーザー全体の管理に関わります。
CustomUser:

個人のユーザー情報の管理:
CustomUserは、個々のユーザーの属性を定義します。ユーザー名、メールアドレス、アクティブ状態など、ユーザーの個人情報を表します。
個々のユーザーのプロフィールページや、個人が自分のアカウント情報を管理する場合に使用されます。
このクラスは、ユーザーが自分のアカウント情報を表示・変更するためのインターフェースを提供します。
つまり、CustomUserManagerは複数のユーザーの管理を行い、CustomUserは個々のユーザーの情報を表します。
"""