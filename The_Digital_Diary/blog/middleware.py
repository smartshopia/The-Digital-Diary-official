class RedirectToPreviousPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            if request.path == '/login/' and 'next' in request.GET:
                request.session['redirect_after_login'] = request.GET['next']
        elif request.path == '/logout/':
            if 'redirect_after_login' in request.session:
                response['Location'] = request.session['redirect_after_login']
                del request.session['redirect_after_login']
        return response
