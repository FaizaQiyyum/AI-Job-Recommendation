from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api_views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jobs/', api_views.JobListCreateView.as_view(), name='api_jobs'),
    path('jobs/<int:pk>/', api_views.JobRetrieveUpdateDestroyView.as_view(), name='api_job_detail'),
    path('applications/', api_views.ApplicationListCreateView.as_view(), name='api_applications'),
]
