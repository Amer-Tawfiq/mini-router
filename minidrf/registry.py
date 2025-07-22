from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
import inflect

EXPOSED_MODELS  = []
EXPOSED_CLASSES  = []
p = inflect.engine()
def expose_model(cls):
    EXPOSED_MODELS.append(cls)
    return cls 

def expose_api(cls=None, *, prefix=None):
    def wrapper(inner_cls):
        inner_cls._custom_prefix = prefix
        EXPOSED_CLASSES.append(inner_cls)
        return inner_cls
    return wrapper(cls) if cls else wrapper

# إنشاء المسارات من EXPOSED_MODELS
def build_viewset_routes():
    routes  = []
    for exposed in EXPOSED_MODELS:
        model = getattr(exposed,'model',None)
        serializer = getattr(exposed,'serializer',None)
        name = p.plural(exposed.__name__.lower().replace("viewset", "").replace("view", "").replace("APIView",""))
        if model and serializer:
            viewset_class = type(
                f"{model.__name__}ViewSet",
                (ModelViewSet,),
                {
                    'queryset': model.objects.all(),
                    'serializer_class': serializer
                }
            )
            routes .append(('router', name, viewset_class))
    return routes 



# إنشاء المسارات من EXPOSED_CLASSES (APIView أو ViewSet)
def build_api_routes():
    routes = []
    for cls in EXPOSED_CLASSES:
        name = p.plural(cls.__name__.lower().replace("viewset", "").replace("view", "").replace("APIView",""))
        if issubclass(cls, ViewSetMixin):
            routes.append(('router', name, cls))
        elif issubclass(cls, APIView) or any(hasattr(cls, m) for m in ['get', 'post', 'put', 'delete']):
            routes.append(('path', name, cls))
    return routes