# routers.py
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import path
from .registry import build_viewset_routes, build_api_routes
from .auto_import import import_all_view_modules
import re

def split_camel_case(name):
    name = re.sub(r'(APIView|ViewSet|View)$', '', name)
    name_snake = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name_snake


class CustomAPIRootView(APIView):
    router = None

    def get(self, request, *args, **kwargs):
        result = {}
        # روابط ViewSets المسجلة في self.registry
        for prefix, viewset, _ in self.router.registry:
            result[prefix] = request.build_absolute_uri(f"{prefix}/")

        # روابط APIViews المسجلة يدويًا
        for prefix, _ in self.router.api_view_paths:
            result[prefix] = request.build_absolute_uri(f"{prefix}/")

        return Response(result)


class MiniRouter(DefaultRouter):
    def __init__(self):
        self.api_view_paths = []
        super().__init__()

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = []

        for route_type, prefix, cls in build_api_routes():
            if route_type == 'path' and isinstance(cls, type):
                # تحديد اسم الـ prefix (إما من الديكوريتر أو توليد تلقائي)
                prefix_name = getattr(cls, '_custom_prefix', split_camel_case(cls.__name__))
                self.api_view_paths.append((prefix_name, cls))
                extra_urls.append(path(f"{prefix_name}/", cls.as_view(), name=prefix_name))

        return urls + extra_urls

    def register_exposed(self):
        import_all_view_modules()  # ← تحميل جميع ملفات views أولاً

        # تسجيل ViewSets التي تم الكشف عنها
        for route_type, prefix, cls in build_viewset_routes():
            if route_type == 'router':
                self.register(prefix, cls)

    def get_api_root_view(self, api_urls=None):
        view = type(
            'CustomRootView',
            (CustomAPIRootView,),
            {'router': self}
        )
        return view.as_view()
