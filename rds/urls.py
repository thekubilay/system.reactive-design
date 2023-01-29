from django.conf import settings

from django.contrib import admin
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import path, include, re_path
from entry.views import IndexTemplateView

urlpatterns = [
  path('admin/', admin.site.urls),
  path('accounts/', include("django.contrib.auth.urls")),
  path('accounts/', include('allauth.urls')),
  path('api-auth/', include("rest_framework.urls")),
  path('api/rest_auth/', include("rest_auth.urls")),
  path('api/rest_auth/registration', include("rest_auth.registration.urls")),
  path('api/', include("accounts.apis.urls")),
  path('api/', include("teams.apis.urls")),
  path('api/', include("projects.apis.urls")),
]

urlpatterns += [
                 re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                 re_path(r'^.*$', IndexTemplateView.as_view(), name="entry-point"),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
