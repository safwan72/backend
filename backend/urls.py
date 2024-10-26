from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_swagger.views import get_swagger_view
from django.views.static import serve
schema_view = get_swagger_view(title='Restaurant API')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/',include('App_Login.urls')),
        path('api/main/',include('App_Main.urls')),
        path('api/order/',include('App_Order.urls')),
        url('swagger/',schema_view),
            url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
        
]
urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
