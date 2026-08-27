from django.contrib import admin
from django.utils.html import format_html

from restaurant_site.admin import admin_site

from .models import Category, MenuItem


@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MenuItem, site=admin_site)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_featured', 'image_preview')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    readonly_fields = ('image_preview',)
    fields = (
        'name', 'description', 'price', 'category', 'is_featured',
        'image', 'image_preview',
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:60px;max-width:60px;'
                'object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"
    image_preview.short_description = "Preview"
