from django.contrib import admin
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.db.models import Sum, Count
from django.urls import path
from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    list_display = ('name', 'price')
    change_list_template = "admin/movie_changelist.html"
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'movie-stats/',
                self.admin_site.admin_view(self.movie_stats_view),
                name = 'movie-stats'
            ),
        ]
        return custom_urls + urls
    def movie_stats_view(self, request):
        most_purchased = Movie.objects.annotate(
            total_sales=Sum('item__quantity')
        ).order_by('-total_sales').first()

        most_reviewed = Movie.objects.annotate(
            review_count=Count('review')
        ).order_by('-review_count').first()

        context = dict(
            self.admin_site.each_context(request),
            most_purchased=most_purchased,
            most_reviewed=most_reviewed,
        )
        return TemplateResponse(request, "admin/movie_stats.html", context)

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
