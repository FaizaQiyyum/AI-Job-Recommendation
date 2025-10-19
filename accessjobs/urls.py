from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views  # import your custom views

urlpatterns = [
    # ✅ Keep Django’s real admin panel accessible
    path('superadmin/', admin.site.urls),

    # ✅ Include your front-end app’s routes
    path('', include('core.urls')),

    # ✅ API routes (if you have them)
    path('api/', include('core.api_urls')),

    # ✅ Custom Password Reset URLs (5-digit code system)
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('password-reset/', views.forgot_password, name='password_reset'),
]

# ✅ Media setup for dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
