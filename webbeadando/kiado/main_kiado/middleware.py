# main_kiado/middleware.py

class AdminSessionMiddleware:
    """
    Middleware az admin felülethez külön session cookie beállításához.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Admin felület esetén külön session cookie használata
        if request.path.startswith('/admin/'):
            request.session_cookie_name = 'admin_sessionid'
        else:
            request.session_cookie_name = 'user_sessionid'

        response = self.get_response(request)
        return response
