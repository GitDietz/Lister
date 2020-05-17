from django.contrib import admin

from .models import InvitationKey


class InviteModelAdmin(admin.ModelAdmin):
    list_display = ['invited_email', 'invite_to_group', 'from_user']

    class Meta:
        model = InvitationKey


admin.site.register(InvitationKey, InviteModelAdmin)

