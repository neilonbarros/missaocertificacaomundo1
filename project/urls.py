# from django.contrib import admin

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import include, path

handler404 = "app.components.errors.custom_page_not_found_view"
handler500 = "app.components.errors.custom_error_view"
handler403 = "app.components.errors.custom_permission_denied_view"
handler400 = "app.components.errors.custom_bad_request_view"

urlpatterns = [
    # path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path("", include("app.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
