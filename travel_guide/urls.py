"""
URL configuration for travel_guide project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.destinations.views import (
    home_view, 
    destination_detail_view,
    register_view,
    login_view,
    logout_view,
    profile_view,
    toggle_bookmark_view,
    toggle_visited_view,
    add_destination_view,
    add_poi_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_view, name="home"),
    path(
        "destinations/<slug:slug>/",
        destination_detail_view,
        name="destination_detail"
    ),
    
    # Authentication URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name="profile"), 
    path('destination/<int:destination_id>/bookmark/', toggle_bookmark_view, name='toggle_bookmark'),
    path('destination/<int:destination_id>/visited/', toggle_visited_view, name='toggle_visited'),
    path('destinations/add/', add_destination_view, name='add_destination'),
    path('destinations/<int:destination_id>/add-poi/', add_poi_view, name='add_poi')
]

# Σερβίρω τα media files στο local development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)