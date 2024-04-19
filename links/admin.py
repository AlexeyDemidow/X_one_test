from django.contrib import admin

from .models import UserLink, UserLinkCollection


class UserLinkAdmin(admin.ModelAdmin):
    """
    User link model view in admin panel
    """
    class Meta:
        model = UserLink

    list_display = ['user', 'title', 'link_type', 'description'] + ['id']
    list_filter = ['user', 'link_type']


class UserLinkCollectionAdmin(admin.ModelAdmin):
    """
    User link collection model view in admin panel
    """
    class Meta:
        model = UserLinkCollection

    list_display = ['user', 'title', 'description'] + ['id']
    list_filter = ['user']


admin.site.register(UserLink, UserLinkAdmin)
admin.site.register(UserLinkCollection, UserLinkCollectionAdmin)
