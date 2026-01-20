from .api_rate_limiter import api_rate_limit

class APIRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Apply only to API routes
        if request.path.startswith("/api/"):
            response = api_rate_limit(request)
            if response:
                return response

        return self.get_response(request)
