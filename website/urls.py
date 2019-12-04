from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('accounts/', include('allauth.urls')),
	path('admin/', admin.site.urls),
	path('', include('project_blood_legion.django.urls')),
]
