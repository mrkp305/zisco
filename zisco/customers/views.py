from django.shortcuts import render, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url

from django_hosts.resolvers import reverse_lazy

from zisco.users.forms import UserCreationForm
from zisco.users.models import (
    Customer,
)
from zisco.products.models import Product

from .forms import AuthenticationForm, CustomerForm
from .models import (
    Req, ReqItem
)


class Login(auth_views.LoginView):
    authentication_form = AuthenticationForm
    template_name = "customers/login.html"

    def get_success_url(self):
        return reverse_lazy("customers:dashboard", host="customers")


class Register(View):
    template_name = "customers/register.html"

    def get(self, request, *args, **kwargs):
        ctx = dict()
        ctx.update({
            "customer_form": CustomerForm(),
            "auth_form": UserCreationForm()
        })
        return HttpResponse(
            render(request, self.template_name, ctx)
        )

    def post(self, request, *args, **kwargs):
        cf = CustomerForm(request.POST)
        uc = UserCreationForm(request.POST)

        if not cf.is_valid() or not uc.is_valid():
            ctx = dict()
            ctx.update({
                "customer_form": cf,
                "auth_form": uc
            })
            return HttpResponse(render(request, self.template_name, ctx))

        else:
            c = cf.save()
            u = uc.save()
            c.user = u
            c.save()
            return HttpResponseRedirect(
                reverse_lazy("customers:login", host="customers")
            )


class Logout(auth_views.LogoutView):
    LOGOUT_REDIRECT_URL = reverse_lazy(
        'customers:login', host="customers"
    )

    def get_next_page(self):
        if self.next_page is not None:
            next_page = resolve_url(self.next_page)
        elif self.LOGOUT_REDIRECT_URL:
            next_page = resolve_url(self.LOGOUT_REDIRECT_URL)
        else:
            next_page = self.next_page

        if self.redirect_field_name in self.request.POST or self.redirect_field_name in self.request.GET:
            next_page = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name)
            )
            url_is_safe = is_safe_url(
                url=next_page,
                allowed_hosts=self.get_success_url_allowed_hosts(),
                require_https=self.request.is_secure(),
            )
            # Security check -- Ensure the user-originating redirection URL is
            # safe.
            if not url_is_safe:
                next_page = self.request.path

        return next_page


class Base(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, "profile")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "customer": self.request.user.profile
        })
        return ctx

    def get_login_url(self):
        return reverse_lazy(
            "customers:login", host="customers"
        )


class DashboardIndex(Base, generic.TemplateView):
    template_name = "customers/dashboard.html"


class Request(Base, generic.ListView):
    model = Product
    template_name = "customers/request.html"
    context_object_name = "products"

    def post(self, request, *args, **kwargs):
        data = request.POST.get('data', None)
        data = eval(data)
        req = None
        if len(data) > 0:
            req = Req.objects.create(customer=self.request.user.profile, )

        if req:
            for i in data:
                p, u = i.get("id", None), i.get("units", None)

                if p and u:
                    try:
                        req.items.create(
                            product_id=p,
                            qty=u,
                        )
                    except:
                        pass

        return self.get(request, *args, **kwargs)


class ReqIndex(Base, generic.ListView):
    template_name = "customers/requests.html"

    def get_queryset(self):
        return self.request.user.profile.requests.all()
