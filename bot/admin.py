from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import FAQ, Info

class FAQAdmin(admin.ModelAdmin):
    list_display = ["id", "question"]
    list_display_links = ["id", "question"]


class InfoAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]

    def has_add_permission(self, request) -> bool:
        return False
    
    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def get_fieldsets(
        self,
        request,
        obj: Info | None = None
    ) -> list[tuple[str | None, dict[str, any]]]:  # type: ignore
        if obj is None:
            return self.get_fieldsets(request=request, obj=obj)

        if obj.slug == "location":
            return [
                ("Ma'lumotlar", {
                    "fields": ("name", "location_url"),
                })
            ]

        elif obj.slug == "call_center":
            return [
                ("Ma'lumotlar", {
                    "fields": ("name", "text"),
                })
            ]

        return self.get_fieldsets(request=request, obj=obj)

admin.site.site_title = "Gumanitar yordam"
admin.site.index_title = "Gumanitar yordam"

admin.site.register(FAQ, FAQAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
