from django.contrib import admin
from .models import Category, Destination, PointsOfInterest

# End-points για τα μοντέλα του models.py
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    # Το slug γεμίζει αυτόματα από το name 
    prepopulated_fields = {"slug": ("name",)}
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "created_at")
    list_filter = ("country", "is_featured")
    search_fields =("title", "country")
    prepopulated_fields = {"slug" : ("title",)}
@admin.register(PointsOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ("title", "destination", "price_range", "created_at")
    list_filter = ("destination", "price_range", "categories")
    search_fields = ("title", "description", "address")