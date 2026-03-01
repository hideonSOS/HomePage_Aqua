from input_page.models import AccessLog

CATEGORY_MAP = [
    ('/blog/',       'ブログ'),
    ('/gaidline/',   '番組説明'),
    ('/room/',       '住之江ゼミナール'),
    ('/artist/',     '出演者イラスト'),
    ('/history/',    '沿革'),
    ('/input_page/', '開発者ページ'),
    ('/top_page/',   'トップページ'),
]


class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        category = self._get_category(request.path)
        if category:
            AccessLog.objects.create(page=category)
        return self.get_response(request)

    def _get_category(self, path):
        if path == '/':
            return 'ホーム'
        for prefix, name in CATEGORY_MAP:
            if path.startswith(prefix):
                return name
        return None
