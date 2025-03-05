# Import necessary modules and models
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Resource, Event, Blog
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated

def home_page(request):
    return render(request, 'users/home.html')  # Make sure 'home.html' exists in 'users/templates/users'

def about_us(request):
    return render(request, 'users/about.html')

# Profile ViewSet (for handling API requests for profiles)
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Only allow authenticated users to interact with profiles

    def get_queryset(self):
        # Optionally, filter profiles by the currently authenticated user
        return Profile.objects.filter(user=self.request.user)

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.db import IntegrityError

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Log the user in after successful signup
            login(request, user)

            # Redirect the user to the new npi (name and profile image) page
            return redirect('npi')

        except IntegrityError as e:
            if 'auth_user.username' in str(e):
                error_message = "Username already exists. Please choose a different username."
                return render(request, 'users/signup.html', {'error_message': error_message})

    return render(request, 'users/signup.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile

@login_required
def npi(request):
    if request.method == 'POST':
        user_profile = request.user.profile

        # Get the name and profile image from the form
        name = request.POST.get('name')
        profile_image = request.FILES.get('profileImage')

        # Update the profile with name and image
        if name:
            user_profile.name = name
        if profile_image:
            user_profile.avatar = profile_image

        # Save the updated profile
        user_profile.save()

        # Redirect the user to the profile page after saving
        return redirect('profile_page')

    return render(request, 'users/npi.html')

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile  # Assuming you have a Profile model linked to the User model

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_profile = request.user.profile  # Get the logged-in user's profile
        
        # Update only the name (do not update the username)
        name = request.POST.get('name')
        if name:
            user_profile.name = name  # Update the profile name

        bio = request.POST.get('bio')
        if bio:
            user_profile.bio = bio

        # Update the avatar if a new one is uploaded
        profile_image = request.FILES.get('avatar')
        if profile_image:
            user_profile.avatar = profile_image
        
        # Save the updated profile
        user_profile.save()

        return redirect('profile_page')
    
    return render(request, 'users/settings.html', {'profile': request.user.profile})

from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        logout(request)  # Django logout function
        return JsonResponse({"message": "Logout successful!"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)

from django.contrib.auth.models import User

@csrf_exempt
def delete_account(request):
    if request.method == "DELETE":
        if request.user.is_authenticated:  # Ensure user is logged in
            user = request.user
            user.delete()  # Delete user from database
            return JsonResponse({"message": "Account deleted successfully!"}, status=200)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)
    return JsonResponse({"error": "Invalid request method"}, status=400)

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')  # Redirect to the home page or dashboard
        else:
            return render(request, 'users/login.html', {'error_message': 'Invalid username or password'})
    
    return render(request, 'users/login.html')

# Resource List View
def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'users/resources.html', {'resources': resources})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Resource, Blog, Event
from .serializers import ResourceSerializer, BlogSerializer, EventSerializer

class ResourceUploadView(APIView):
    def post(self, request, *args, **kwargs):
        content_type = request.data.get('content_type')
        title = request.data.get('title')
        description = request.data.get('description')
        uploaded_file = request.FILES.get('file-upload')

        if content_type == 'resource':
            serializer = ResourceSerializer(data=request.data)
            if serializer.is_valid():
                # Explicitly set the user field to the currently logged-in user
                serializer.save(user=request.user)
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif content_type == 'blog':
            serializer = BlogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif content_type == 'event':
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.decorators import login_required
from .models import Resource, Blog, Event
from django.http import JsonResponse

@login_required
def upload_page(request):
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        uploaded_file = request.FILES.get('file-upload')

        if not all([content_type, title, description, uploaded_file]):
            return JsonResponse({'status': 'error', 'errors': 'All fields are required'}, status=400)

        # Create resource, blog, or event
        if content_type == 'resource':
            Resource.objects.create(user=request.user, title=title, description=description, resource_file=uploaded_file)
        elif content_type == 'blog':
            Blog.objects.create(user=request.user, title=title, description=description, resource_file=uploaded_file)
        elif content_type == 'event':
            Event.objects.create(user=request.user, title=title, description=description, resource_file=uploaded_file)
        else:
            return JsonResponse({'status': 'error', 'errors': 'Invalid content type'}, status=400)

        return JsonResponse({'status': 'success', 'message': 'Upload successful!'})

    return render(request, 'users/upload.html')  # Keep for GET requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_page(request):
    # Fetch the logged-in user's profile
    user = request.user
    return render(request, 'users/profile.html', {'user': user})

from django.shortcuts import render, get_object_or_404
from .models import Resource, Blog, Event
from django.core.paginator import Paginator

@login_required
def resource_list(request):
    resources = Resource.objects.all().order_by('-created_at')
    resource_objects = Resource.objects.all()  # Sare resources fetch karo
    
    paginator = Paginator(resource_objects, 5)  # Har page pe 5 resources
    page_number = request.GET.get('page')  # URL se page number lo
    page_obj = paginator.get_page(page_number)  # Page fetch karo

    return render(request, 'users/resource_list.html', {"resources": resources})

@login_required
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'users/blogs_list.html', {"blogs": blogs})

@login_required
def event_list(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'users/events_list.html', {"events": events})

@login_required
def resource_detail(request, id):
    resource = get_object_or_404(Resource, id=id)
    return render(request, 'users/resource_detail.html', {"resource": resource})

@login_required
def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'users/blog_detail.html', {"blog": blog})

@login_required
def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'users/event_detail.html', {"event": event})

from django.http import JsonResponse
from .models import Resource, Blog, Event

def get_resources(request):
    resources = Resource.objects.all().order_by('-created_at')[:5]  # Latest 5
    data = [{"title": r.title, "description": r.description, "file": r.resource_file.url if r.resource_file else ""} for r in resources]
    return JsonResponse({"resources": data})

def get_blogs(request):
    blogs = Blog.objects.all().order_by('-created_at')[:5]  # Latest 5
    data = [{"title": b.title, "description": b.description} for b in blogs]
    return JsonResponse({"blogs": data})

def get_events(request):
    events = Event.objects.all().order_by('-created_at')[:5]  # Latest 5
    data = [{"title": e.title, "description": e.description, "date": e.date.strftime("%Y-%m-%d")} for e in events]
    return JsonResponse({"events": data})

