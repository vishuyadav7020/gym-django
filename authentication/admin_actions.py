from django.core.cache import cache
from django.contrib import messages

def reset_login_cache(modeladmin, request, queryset):
    cache.delete("global_login_attempts")
    cache.delete("global_login_lock")

    messages.success(
        request,
        "Login attempt cache has been reset successfully."
    )

reset_login_cache.short_description = "Reset login attempt cache (Redis)"
