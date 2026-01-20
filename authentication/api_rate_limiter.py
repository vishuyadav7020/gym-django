from django.core.cache import cache
from django.http import JsonResponse

API_LIMIT = 50       # requests
API_WINDOW = 60        # seconds


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def api_rate_limit(request):
    ip = get_client_ip(request)
    key = f"rate_limit:api:{ip}"

    count = cache.get(key, 0)
    if count >= API_LIMIT:
        return JsonResponse(
            {
                "error": "Too many requests",
                "message": "Please try again later"
            },
            status=429
        )
    
    if count == 0:
        cache.set(key, 1, timeout=API_WINDOW)
    else:
        cache.incr(key)

    return None
