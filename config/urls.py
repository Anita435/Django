from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views import defaults as default_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('api/', include('user_api.urls', namespace='user_api')),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='dashboard/logout.html'), name='logout'),

]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),

        path("500/", default_views.server_error),
    ]

    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
