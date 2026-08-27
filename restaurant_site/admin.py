from django.contrib.admin import AdminSite


class RestaurantAdminSite(AdminSite):
    site_header = "Restaurant Name Admin"
    site_title = "Restaurant Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        from menu.models import Category, MenuItem
        from pages.models import ContactMessage

        extra_context = extra_context or {}
        extra_context.update({
            'category_count': Category.objects.count(),
            'menu_item_count': MenuItem.objects.count(),
            'featured_item_count': MenuItem.objects.filter(is_featured=True).count(),
            'unread_message_count': ContactMessage.objects.filter(is_read=False).count(),
        })
        return super().index(request, extra_context)


admin_site = RestaurantAdminSite()
