from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    name = models.CharField(max_length=250, blank=True, null=True)  # Store the full name
    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Allow nulls for existing rows
    title = models.CharField(max_length=255)
    description = models.TextField()
    resource_file = models.FileField(upload_to='blog/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Resource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Allow nulls for existing rows
    title = models.CharField(max_length=255)
    description = models.TextField()
    resource_file = models.FileField(upload_to='resources/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Allow null for existing rows
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    resource_file = models.FileField(upload_to='event/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

