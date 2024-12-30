
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include('students.urls')),
    path('', include('landing.urls')),  # Central landing page
    path('admins/', include('admins.urls')),
    path('teacher/', include('teachers.urls')),
    path('student/', include('students.urls')),


]
