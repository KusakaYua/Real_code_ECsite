from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView,ListView, UpdateView
from django.views.generic.base import TemplateView, View #RedirectView
# Create your views here.

import stripe

from .forms import SearchForm
from .models import Item, CartItem, Order, Category
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()

class OnlyYouMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return (user.id == self.kwargs['pk']) or (user.is_superuser)

class HomeView(ListView):
    template_name = "core/home.html"
    model = Item
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm
        context["categories"] = Category.objects.all()
        return context
    
    def get_queryset(self):
        items = super().get_queryset()
        q_category = self.request.GET.get('category')
        if q_category is not None:
            items = items.filter(category=q_category)
        return items

class ItemView(DetailView):
    template_name = "core/item.html"
    model = Item

    def get_success_url(self):
        user_pk = self.request.user.id
        return reverse_lazy('cart', kwargs={'pk': user_pk})

    def post(self, *args, **kwargs):
        item_pk = self.request.POST.get("item_pk")
        quantity = int(self.request.POST.get("quantity"))
        item = Item.objects.get(id=item_pk)
        cart_item = CartItem(item=item, quantity=quantity)
        user = self.request.user
        user.cart.add_cart_item(cart_item)
        return redirect(self.get_success_url())

class CartView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = "core/cart.html"
    model = User
    context_object_name = "cart"

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        return user.cart
    
class DeleteCartItemView(LoginRequiredMixin, OnlyYouMixin, DeleteView):
    model = User

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        cart_item_pk = self.request.POST['cart_item_pk']
        cart_item = user.cart.cart_items.get(id=cart_item_pk)
        return cart_item

    def get_success_url(self):
        user_pk = self.request.user.id
        return reverse_lazy('cart', kwargs={'pk': user_pk})
    

class CartUpdateView(LoginRequiredMixin, UpdateView):
    model = CartItem
    fields = ['quantity']
    template_name = "cart_update.html"

    def form_valid(self, form):
        # 必要に応じて追加の処理をここに書く
        return super().form_valid(form)

    def get_success_url(self):
        user_pk = self.request.user.id
        return reverse_lazy('cart', kwargs={'pk': user_pk})


class OrderView(View):
    def post(self, *args, **kwargs):
        order_user = self.request.user
        order_cart = order_user.cart
        order_obj = Order.objects.create(
            user=order_user,
            order_price = order_cart.total_price,
        )
        for cart_item in order_cart.cart_items.all():
            order_obj.order_items.add(cart_item)
        order_cart.cart_items.clear()

        line_items = []
        for order_item in order_obj.order_items.all():
            line_item = {
                'price_data':{
                    'currency': 'jpy',
                    'unit_amount': order_item.item.price,
                    'product_data':{
                        'name': order_item.item.name,
                    }
                },
                'quantity':  order_item.quantity
            }
            line_items.append(line_item)

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items = line_items,
                mode='payment',
                phone_number_collection={'enabled':True},
                shipping_address_collection={'allowed_countries':['JP']},
                success_url=settings.MYSITE_DOMAIN + '/success/',
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url)
            

class SuccessView(TemplateView):
    template_name = "core/success.html"