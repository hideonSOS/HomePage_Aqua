from input_page.models import AccessLog


class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        exclude = ['/static/', '/media/', '/admin/', '/favicon']
        if not any(path.startswith(ex) for ex in exclude):
            AccessLog.objects.create(page=path)
        return self.get_response(request)
