from rest_framework import generics, filters, permissions
from .models import JobPosting, Application
from .serializers import JobPostingSerializer, ApplicationSerializer

class JobListCreateView(generics.ListCreateAPIView):
    queryset = JobPosting.objects.all().order_by('-created_at')
    serializer_class = JobPostingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','location','company']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class JobRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer

class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).order_by('-applied_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
