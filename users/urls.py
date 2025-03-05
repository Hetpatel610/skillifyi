from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, resource_list 
from django.urls import path, include
from . import views

# Set up router for Profile API
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

# Define URL patterns
urlpatterns = [
    # Include ProfileViewSet API URLs
    path('api/', include(router.urls)),  # Profiles API route

    # Resource list and upload routes
    path('resources/', resource_list, name='resource_list'),  # URL for listing resources
]

# urls.py
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import ResourceUploadView, get_resources, get_blogs, get_events

urlpatterns = [
    path('home/', views.home_page, name='home_page'),  # Ensure you have this pattern for the home page
    path('api/resource-upload/', ResourceUploadView.as_view(), name='resource-upload'),
    path('upload/', views.upload_page, name='upload_page'),
    path('signup/', views.signup, name='signup'),  # URL for Sign-Up
    path('npi/', views.npi, name='npi'),
    path('login/', views.login_view, name='login'),  # URL for Login
    path('profile/', views.profile_page, name='profile_page'),  # Profile page
    path('update-profile/', views.update_profile, name='update_profile'),  # Settings page for updating profile
    path('aboutus/', views.about_us, name='about_us'),
    path('resources/', views.resource_list, name="resource_list"),
    path('blogs/', views.blog_list, name="blog_list"),
    path('events/', views.event_list, name="event_list"),
    path('resources/<int:id>/', views.resource_detail, name="resource_detail"),
    path('blogs/<int:id>/', views.blog_detail, name="blog_detail"),
    path('events/<int:id>/', views.event_detail, name="event_detail"),
    path('api/resources/', get_resources, name="api_resources"),
    path('api/blogs/', get_blogs, name="api_blogs"),
    path('api/events/', get_events, name="api_events"),
    path("api/logout/", views.logout_user, name="logout"),
    path("api/delete-account/", views.delete_account, name="delete-account"),
]
