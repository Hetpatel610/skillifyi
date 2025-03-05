from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'name', 'bio', 'avatar']  # Add any other fields from the profile model

# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class SignupSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(write_only=True, required=False)  # New field for profile pic
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_picture']  # Add profile_picture

    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Create the associated profile if a picture is uploaded
        if profile_picture:
            Profile.objects.create(user=user, profile_picture=profile_picture)
        return user
 
from rest_framework import serializers
from .models import Resource, Blog, Event

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'resource_file', 'created_at']

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'resource_file', 'created_at']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'resource_file', 'date', 'created_at']
