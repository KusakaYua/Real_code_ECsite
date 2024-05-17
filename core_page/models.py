from django.conf import settings
from django.db import models

# Create your models here.
User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = '商品カテゴリ'
        verbose_name_plural = '商品カテゴリ'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="item_images/", blank=True, null=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name

class CartItem(models.Model):
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = 'カートアイテム'
        verbose_name_plural = 'カートアイテム'
    
    def __str__(self):
        return f"{self.quantity}個の{self.item.name}"

    @property
    def total_price(self):
        return self.item.price * self.quantity


class Cart(models.Model):
    cart_items = models.ManyToManyField(to=CartItem, blank=True)

    class Meta:
        verbose_name = 'カート'
        verbose_name_plural = 'カート'
    
    def __str__(self):
        # CustomUserモデルのcartフィールドに related_name='cart_user' と指定したことで
        # 以下のように self.cart_user でユーザーオブジェクトを呼び出すことが可能になります
        return f"{self.cart_user.username}のカート"

    def add_cart_item(self, new_cart_item):
        if new_cart_item.item in [cart_item.item for cart_item in self.cart_items.all()]:
            original_cart_item = self.cart_items.get(item_id=new_cart_item.item.id)
            original_cart_item.quantity += new_cart_item.quantity
            original_cart_item.save()
        else:
            new_cart_item.save()
            self.cart_items.add(new_cart_item)

    @property
    def total_price(self):
        return sum([cart_item.total_price for cart_item in self.cart_items.all()])
    
class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(to=CartItem, blank=True)
    order_price = models.PositiveIntegerField()
    ordered_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '注文'
        verbose_name_plural = '注文'
    
    def __str__(self):
        return f"{self.user.username}様の注文（{self.ordered_date}）"