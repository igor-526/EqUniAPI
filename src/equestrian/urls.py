from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from documentation.views import DocumentationPage

from .settings import ALLOW_DOCUMENTATION, DEBUG, MEDIA_ROOT, MEDIA_URL

api_v1_patterns = [
    path('auth/', include('profile_management.urls')),
    path('horses/', include('horses.urls')),
    path('gallery/', include('gallery.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_patterns)),
]

if ALLOW_DOCUMENTATION:
    urlpatterns.append(
        path("doc/", DocumentationPage.as_view(), name="documentation")
    )

if DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += static(MEDIA_URL,
                          document_root=MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
