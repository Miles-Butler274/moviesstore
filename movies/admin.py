from django.contrib import admin
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.db.models import Count
from django.urls import path
from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    list_display = ('name', 'price')

class ReviewAdmin(admin.ModelAdmin):
    change_list_template = 'admin/review_changelist.html'
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'top-reviewer/',
                self.admin_site.admin_view(self.top_reviewer_view),
                name='top-reviewer',
            ),
        ]
        return custom_urls + urls

    def top_reviewer_view(self, request):
        top_reviewer = User.objects.annotate(
            total_reviews=Count('review')
        ).order_by('-total_reviews').first()

        return TemplateResponse(
            request,
            'admin/top_reviewer.html',
            { 'user': top_reviewer, }
        )


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
