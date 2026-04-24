from rest_framework import serializers
from .models import User, JobPosting, Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'skills', 'experience', 'location']

class JobPostingSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = JobPosting
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    # show job title in responses for clarity
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'applied_at']  # exclude user!

    def create(self, validated_data):
        # attach the current logged-in user automatically
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)
