from django.contrib import admin
from .models import Order, Item

from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.contrib.auth.models import User

class OrderAdmin(admin.ModelAdmin):
    change_list_template = "admin/order_changelist.html"
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'top-customer/',
                self.admin_site.admin_view(self.top_customer_view),
                name='top-customer',
            ),
        ]
        return custom_urls + urls

    def top_customer_view(self, request):

        top_user = (
            User.objects
                .annotate(
                    total_movies=Coalesce(
                        Sum('order__item__quantity'),
                        Value(0)
                    )
                )
                .order_by('-total_movies')
                .first()
        )

        context = dict(
            self.admin_site.each_context(request),
            top_user=top_user,
        )

        return TemplateResponse(
            request,
            "admin/top_customer.html",
            context,
        )

admin.site.register(Order, OrderAdmin)
admin.site.register(Item)