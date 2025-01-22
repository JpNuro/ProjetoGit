from django.contrib import admin
from django.utils.html import format_html
from .models import NewsSource, NewsCategory, News, FinancialIndicator, APILog

# Register your models here.

@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'url')

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'news_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def news_count(self, obj):
        return obj.news_set.count()
    news_count.short_description = 'Number of News'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_at', 'is_published', 'source_link')
    list_filter = ('is_published', 'category', 'source', 'author')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)

    def source_link(self, obj):
        return format_html('<a href="{}" target="_blank">View Source</a>', obj.source_url)
    source_link.short_description = 'Source'

@admin.register(FinancialIndicator)
class FinancialIndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'current_value', 'change_display', 'last_updated')
    search_fields = ('name', 'symbol')
    ordering = ('name',)

    def change_display(self, obj):
        color = 'green' if obj.change_value >= 0 else 'red'
        return format_html(
            '<span style="color: {}">{}% ({})</span>',
            color,
            obj.change_percentage,
            obj.change_value
        )
    change_display.short_description = 'Change'

@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'status_code', 'timestamp', 'error_message')
    list_filter = ('status_code', 'endpoint')
    search_fields = ('endpoint', 'error_message')
    readonly_fields = ('endpoint', 'request_data', 'response_data', 'status_code', 'timestamp', 'error_message')
    ordering = ('-timestamp',)
