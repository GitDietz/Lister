from django.contrib import admin

from .models import InvitationKey


class InviteModelAdmin(admin.ModelAdmin):
    list_display = ['invited_email', 'invited_user', 'from_user_id']

    class Meta:
        model = InvitationKey


admin.site.register(InvitationKey, InviteModelAdmin)

