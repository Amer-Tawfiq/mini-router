# mini-router 🔀

مكتبة MiniRouter مخصصة لـ Django REST Framework لتبسيط إدارة مسارات الـ APIs.


---
# MiniDRF 🚀

**MiniDRF** is a lightweight extension for Django REST Framework (DRF) that allows automatic registration of your API views and viewsets without writing repetitive `urls.py` code.

## ✅ Features

- 🔍 **Auto-discovery** of your API classes.
- 🚦 Supports both `APIView` and `ViewSet`.
- 🏷️ Custom prefix support via decorator.
- 🌱 Minimal configuration, quick start.
- 📂 Works seamlessly across multiple Django apps.
- 🧩 Plug-and-play with DRF's `DefaultRouter`.
- تسجيل تلقائي لجميع ViewSet و APIView بدون كتابة `urlpatterns` يدويًا.
- دعم API Root View مخصص يعرض روابط كل API تلقائيًا.
- تقسيم المسارات حسب النوع (path / router).


---

## ⚙️ التثبيت

```bash
pip install git+https://github.com/Amer-Tawfiq/mini-router.git


# example
# urls app father
from minidrf.router import MiniRouter
router = MiniRouter()
router.register_exposed()

urlpatterns = [
    path("api/", include(router.urls)),
]

# view
from minidrf import expose_model,expose_api
@expose_api(prefix="products")
class ProductAPIView(ModelViewSet):
   def list(self, request):
        return Response({"msg": "custom report"})
